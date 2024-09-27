import json
import os


FILEPATH = "results.json"

# Load the results from results.json
def load_results():
    if not os.path.exists(FILEPATH):
        with open(FILEPATH, 'w') as f:
            json.dump([], f)  # Create an empty array to start with
    with open(FILEPATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return data


def load_questions() -> list[str]:
    with open('evaluation_questions.txt', 'r') as f:
        questions_gathered = [line.strip() for line in f.readlines()]
    return questions_gathered