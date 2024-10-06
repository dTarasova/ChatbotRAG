import json
import os


FILEPATH = "results.json"

import re
# from spellchecker import SpellChecker

# Initialize the spell checker
# spell = SpellChecker()

# List of common articles to ignore
ARTICLES = {'a', 'an', 'the'}

def normalize(text):
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower()).strip()
    
    # Correct typos
    # corrected_words = [spell.correction(word) for word in text.split()]
    corrected_words = [word for word in text.split()]
    
    # Remove articles
    filtered_words = [word for word in corrected_words if word not in ARTICLES]
    
    return ' '.join(filtered_words)



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