import json
from enum import Enum

from openai import OpenAI


class OpenAIModel(Enum):
    GPT_4O = 0
    GPT_4O_MINI = 1
    GPT_4 = 2

    # Returns the formatted name of the model, ready for the API
    # e.g. GPT_4O' -> 'gpt-4o'
    def __str__(self):
        return self.name.replace("_", "-").lower()


# Client wrapper for OpenAI client
class OpenAIWrapper:
    def __init__(self, key, model):
        self._client = OpenAI(api_key = key)
        self.set_active_model(model)

    # Returns OpenAI client object
    def get_client(self):
        return self._client

    # Returns the API-ready string of the active model
    def get_active_model(self):
        return str(self._model)

    # Updates the active model
    def set_active_model(self, model):
        if not(model or model is OpenAIModel):
            print("[ERROR] Cannot set_active_model to object " + str(model))
            exit(1)

        self._model = model
        print("[INFO] Updated client model to type '" + self.get_active_model() + "'")


# Returns the response of the LLM
def unwrap_response(response_object):
    if len(response_object.choices) < 1:
        print("[ERROR] OpenAI LLM responded with no responses.")
        exit(1)
    elif len(response_object.choices) > 1:
        print("[WARN] OpenAI LLM responded with too many responses, defaulting to first response")

    print("RESPONSE FROM OPENAI: " + response_object.choices[0].message.content)

    return response_object.choices[0].message.content
    

"""
Example usage

client = OpenAIWrapper("secret-key-here", OpenAIModel.GPT_4O_MINI)
chat_completion = client.get_client().chat.completions.create(
    model=client.get_active_model(),
    messages=[
        {"role": "system", "content":"You are designed to summarise educational transcripts into concise transcripts, so remove any sentences. But you MUST still use their words, hence only drop sentences."},
        {"role": "user", "content": ""A boat is a vessel designed for traveling across water, and while it may seem like a simple thing that just floats, the science behind how it works is both fascinating and multifaceted. It all starts with the concept of buoyancy, which is the force that keeps a boat afloat. Buoyancy is a principle that was first described by the ancient Greek scientist Archimedes. The basic idea is that an object submerged in a fluid experiences an upward force equal to the weight of the fluid displaced by the object. In the case of a boat, when it is placed in water, the boat pushes down on the water, displacing a certain volume of it. If the weight of the water displaced by the boat is greater than or equal to the weight of the boat itself, the boat will float. This is why a boat, even though it might seem heavy, can stay on the surface of the water without sinking.""}])

print(unwrap_response(chat_completion))
"""


# returns a summarised transcript
def summarise_transcript(client, transcript):
    chat_completion = client.get_client().chat.completions.create(
        model=client.get_active_model(),
        messages=[
            {"role": "system",
             "content": "You are designed to summarise educational transcripts. But you MUST still use their wording. Give me each summarised sentence on a different, and split into chapters of about five sentences long, titled as <Chapter 1>, <Chapter 2> and so on."},
            {"role": "user",
             "content": transcript.get_transcript()}
        ]
    )

    return unwrap_response(chat_completion)



# returns the topic of the video
def summarise_to_topic(client, transcript):
    chat_completion = client.get_client().chat.completions.create(
        model=client.get_active_model(),
        messages=[
            {"role": "system",
             "content": "Name this video, based on the transcript I give you. Finish the sentence 'Here is a brain bite on'...Just reply in 1-4 words"},
            {"role": "user",
             "content": transcript}
        ]
    )

    return unwrap_response(chat_completion)[len("Here is a brain bite on "):].replace(".", "")


# returns a json object with chapter questions in format:
"""
[
  {
    "question": "What happens in the final assembly line in Chapter 4?",
    "answer": [
      "Components like wings, landing gear, and engines are installed",
      "The aircraft is painted",
      "The plane is tested for speed",
      "correctAnswer": 0
    ]
  },
  {
    "question": "What did the author learn from their visit to Airbus in Chapter 5?",
    "answer": [
      "The complexity of airplane manufacturing",
      "How to design an aircraft",
      "How to fly an A350",
      "correctAnswer": 0
    ]
  }
]
"""
def generate_questions(client, shortened_transcript):
    chat_completion = client.get_client().chat.completions.create(
        model=client.get_active_model(),
        messages=[
            {"role": "system",
             "content": 'Take the following text, and for each chapter write a question and a VERY SHORT list of THREE multiple choice answers. For each question and answer format it in json please, in the format of a list, with objects {"question":QUESTION_HERE, "answer":["answer1", "answer2"], "correctAnswer":index}'},
            {"role": "user",
             "content": shortened_transcript}
        ]
    )

    response = unwrap_response(chat_completion)
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        response = response[:(len(response) - 3)]
    print(response)

    return json.loads(response)
