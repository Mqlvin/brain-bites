# Compare two words, and score their similarity from 0.0 to 1.0, where 1.0 is identical
def compare_words(word_a, word_b):
    len_a = len(word_a) + 1
    len_b = len(word_b) + 1
    # Create a matrix to store the difference between each letter
    matrix = [[0 for __ in range(len_b)] for _ in range(len_a)]

    # Precompute some of the differences, e.g. the first letter of one word is never gonna match the rest of the letters
    for i in range(1, len_a):
        matrix[i][0] = i
    for j in range(1, len_b):
        matrix[0][j] = j

    # Loop over the unchecked letters
    for j in range(1, len_b):
        for i in range(1, len_a):
            # Calculate basically how hard it is to convert from one word to the other word
            if word_a[i-1] == word_b[j-1]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            deletion_cost  = matrix[i-1][j] + 1
            insertion_cost = matrix[i][j-1] + 1
            substitution_cost = matrix[i-1][j-1] + substitution_cost
            cost = min(substitution_cost, deletion_cost, insertion_cost)
            matrix[i][j] = cost

    # The cost to convert the word is stored in the bottom right of the matrix
    min_changes = matrix[len_a - 1][len_b - 1]
    return 1 - (min_changes / max(len_a - 1, len_b - 1))

# Find the location of the closest piece of text in a larger text
def find_subtext(text, search_text):
    words = text.split()
    search_words = search_text.split()

    num_words = len(words)
    num_search_words = len(search_words)

    # If looking for something larger than the text, gotta be impossible
    if num_words < num_search_words:
        return None

    max_score = 0
    max_index = 0
    # Loop through in chunks the same length as what we are looking for
    for i in range(num_words - num_search_words + 1):
        sub_list = words[i:i + num_search_words]
        total_score = 0
        # For each word in both phrases
        for j in range(num_search_words):
            # Compute how similar the phrases are
            sub_word = sub_list[j]
            check_word = search_words[j]
            raw_score = compare_words(sub_word, check_word)
            score = raw_score / num_search_words
            total_score += score
        # Keep track of how similar this phrase is
        if total_score > max_score:
            max_score = total_score
            max_index = i

    # Return the word index where it matches
    return max_index, max_index + num_search_words
