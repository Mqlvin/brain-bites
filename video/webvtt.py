import os

class WebVTTUtil:
    @staticmethod
    def is_whitespace(string):
        # Check if a string is empty, either None, "", "  ", "\n" etc.
        return not string or string.isspace()

    @staticmethod
    def iter_blocks(string):
        block = ""
        # Iterate line by line through a file
        for line in string.split("\n"):
            blank_line = WebVTTUtil.is_whitespace(line)
            blank_block = WebVTTUtil.is_whitespace(block)
            # Check if an empty line has been reached
            if blank_line and not blank_block:
                # Yield the completed block and reset it
                yield block
                block = ""
            elif not blank_line:
                # If the line has data, add it to the block
                block += line + os.linesep

    @staticmethod
    def iter_keys_values(string, line_sep=os.linesep):
        # Iterate over each line in the block
        for line in string.split(line_sep):
            # Split at colon
            key_value = line.split(":")
            if WebVTTUtil.is_whitespace(line):
                # Ignore whitespaces
                continue
            if len(key_value) != 2:
                # If there are more than or less than 2 values, something went wrong
                raise RuntimeError(f"Could not retrieve key-value pair from: {key_value}")
            yield key_value[0].strip(), key_value[1].strip()

    @staticmethod
    def iter_tags(string):
        block = ""
        tag_depth = 0
        new_tag_depth = 0
        depth_changed = False
        for char in string:
            # Where a tag is something like <c> </c> etc
            if char == "<":
                # Start of a tag
                depth_changed = True
                new_tag_depth = tag_depth + 1
            elif char == ">":
                # End of a tag
                depth_changed = True
                new_tag_depth = tag_depth - 1
            else:
                block += char

            if depth_changed:
                if block != "":
                    yield block, tag_depth
                depth_changed = False
                block = ""
                tag_depth = new_tag_depth
        # If depth is constant e.g. no tags, make sure that something is still yielded
        yield block, tag_depth

class WebVTTTiming:
    @staticmethod
    def is_timestamp(string):
        # Check if string is in format HH:MM:SS.SSS
        split = string.split(":")
        return len(split) == 3

    def __init__(self, timing_string):
        if not WebVTTTiming.is_timestamp(timing_string):
            raise RuntimeError(f"Could not parse a timestamp from: {timing_string}")
        timing_split = timing_string.split(":")
        # Split string into 3 parts, ordered as hours, minutes, seconds
        hours_str = timing_split[0]
        minutes_str = timing_split[1]
        seconds_str = timing_split[2]
        self.__hours = int(hours_str)
        self.__minutes = int(minutes_str)
        self.__seconds = float(seconds_str)

    def seconds(self):
        # The timestamp converted to seconds
        return float(self.__hours * 3600) + float(self.__minutes * 60) + self.__seconds

    def __format_seconds(self):
        # For some reason doing {float:02.3f} doesn't work? It doesn't add leading zeros. Had to make my own
        seconds_str = f"{self.__seconds:.3f}"
        if len(seconds_str) == 5:
            seconds_str = "0" + seconds_str
        return seconds_str

    def __format_time(self):
        # Format to HH:MM:SS.SSS
        return f"{self.__hours:02d}:{self.__minutes:02d}:{self.__format_seconds()}"

    def __str__(self):
        return self.__format_time()

    def __repr__(self):
        return f"<WebVTTTiming {self.__format_time()}>"

class WebVTT:
    def __init__(self, file_path):
        self.__header = {}
        self.__cues = []
        self.__transcript = ""

        with open(file_path) as file:
            file_data = file.read()

        count = 0
        for block in WebVTTUtil.iter_blocks(file_data):
            if count == 0:
                # First block is always the file header
                self.__parse_header(block)
            else:
                # Rest is always transcript
                self.__parse_cue(block)
            count += 1

        self.__parse_transcript()

    def __parse_header(self, block):
        block_lines = block.split(os.linesep)
        if block_lines[0] == "WEBVTT":
            # Ignore the first line that just says WEBVTT
            block = os.linesep.join(block_lines[1:])
        for key, value in WebVTTUtil.iter_keys_values(block):
            # Add header contents to a dict
            self.__header[key] = value

    def __parse_cue(self, block):
        if not WebVTTCue.is_cue(block) and len(self.__cues) > 0:
            # If a random piece is found without a time stamp, append it to the previous cue
            self.__cues[-1].add_block(block)
        else:
            # If a timestamp is the first line, make a new cue
            self.__cues.append(WebVTTCue(block))

    def __parse_transcript(self):
        buffer_word = ""
        previous_word = ""
        for cue in self.__cues:
            if not cue.has_words():
                # If the cue is not made of single words, ignore it
                continue
            for word, timestamp in cue.iter_timed_words():
                if word == previous_word:
                    # Sometimes a word is repeated so it stays on screen, ignore these duplicates
                    previous_word = ""
                else:
                    self.__transcript += word
                # Buffer word keeps track of the last word
                buffer_word = word
            previous_word = buffer_word
            self.__transcript += "\n"

    def iter_words(self):
        for cue in self.__cues:
            for word, timestamp in cue.iter_timed_words():
                yield word, timestamp

    def get_transcript(self):
        return self.__transcript

class WebVTTCue:
    @staticmethod
    def is_cue(block):
        # Check if it takes the format 'Timestamp --> Timestamp setting:value'
        lines = block.split(os.linesep)
        timing = lines[0].split(" ")
        if len(timing) >= 3:
            return timing[1] == "-->"
        else:
            return False

    @staticmethod
    def num_words(cue):
        # Find the number of distinct words seperated by spaces
        cue = cue.strip()
        return len(cue.split(" "))

    def __init__(self, block):
        self.__start_time = None
        self.__end_time = None
        self.__cues = []
        self.__settings = {}

        count = 0
        for line in block.split(os.linesep):
            if count == 0:
                # First line should always be the timing
                self.__parse_timing(line)
            else:
                self.__parse_cue(line)
            count += 1

    def __parse_timing(self, line):
        line_split = line.split(" ")
        if len(line_split) < 3:
            raise RuntimeError(f"Could not parse timing from: {line}")
        # Timing is in format 'Timestamp --> Timestamp' so we need first and third item in the split string
        self.__start_time = WebVTTTiming(line_split[0])
        self.__end_time = WebVTTTiming(line_split[2])
        if len(line_split) > 3:
            settings = " ".join(line_split[3:])
            for key, value in WebVTTUtil.iter_keys_values(settings, line_sep=" "):
                self.__settings[key] = value

    def __parse_cue(self, line):
        timestamp = self.__start_time
        for tag, tag_depth in WebVTTUtil.iter_tags(line):
            if tag_depth == 1:
                # Inside a tag such as <c> </c>
                if WebVTTTiming.is_timestamp(tag):
                    timestamp = WebVTTTiming(tag)
            elif tag_depth == 0:
                # Outside a tag, reading the actual text
                if not WebVTTUtil.is_whitespace(tag):
                    self.__append_cue(tag, timestamp)

    def __append_cue(self, cue, timestamp):
        self.__cues.append((cue, timestamp))

    def add_block(self, block):
        # Add additional data to an existing, timestamped cue
        for line in block.split(os.linesep):
            self.__parse_cue(line)

    def has_words(self):
        # Return True if there are words in the cue
        for cue, timestamp in self.__cues:
            if WebVTTCue.num_words(cue) >= 1 and not WebVTTUtil.is_whitespace(cue):
                return True
        return False

    def iter_words(self):
        # Get all the cues that are a single word long
        for cue, timestamp in self.iter_timed_words():
            yield cue

    def iter_timed_words(self):
        # Get each cue that has only one word, and return the cue and timestamp
        for cue, timestamp in self.__cues:
            if WebVTTCue.num_words(cue) == 1:
                yield cue, timestamp

    def get_start_time(self):
        return self.__start_time

    def __repr__(self):
        if len(self.__cues) > 0:
            cue = self.__cues[0]
        else:
            cue = "<none>"
        return f"<WebVTTCue {cue}>"
