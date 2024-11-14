import json
import re

def process_log_file(input_file, output_file):
    # Regular expression to match the JSON log entries in the text file
    log_entry_pattern = r'\{.*?\}'
    
    # Initialize counters for question numbers
    question_number = 0

    # Open the input text file and output LaTeX file with utf-8 encoding
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # Read all lines from the input file
        file_content = infile.read()
        
        # Find all JSON log entries using regex
        log_entries = re.findall(log_entry_pattern, file_content, re.DOTALL)
        
        for entry in log_entries:
            try:
                # Parse each JSON log entry
                log_data = json.loads(entry)

                # Extract necessary fields from the JSON log
                question = log_data.get("question", "N/A")
                correct_model = log_data.get("user_choice", {}).get("correct_model", "N/A")
                preferred_model = log_data.get("user_choice", {}).get("preferred_model", "N/A")
                choice_explanation = log_data.get("user_choice", {}).get("choice_explanation", "N/A")

                # Increment the question number
                question_number += 1

                # Write the extracted data to the LaTeX output file
                outfile.write(f"\\subsection{{Question number {question_number}}}\n")
                outfile.write(f"\\textbf{{Question: }} {question} \\newline\n")
                outfile.write(f"\\textbf{{Result of Correctness: }} {correct_model} \\newline\n")
                outfile.write(f"\\textbf{{Result of Preference: }} {preferred_model} \\newline\n")
                outfile.write(f"\\textbf{{Reasoning: }} {choice_explanation} \\newline\n\n")

            except json.JSONDecodeError:
                print(f"Error parsing log entry: {entry}")
                continue

    print(f"Processing complete. LaTeX code saved to {output_file}")

# Example usage
input_file = 'log_entries.txt'  # Replace with your input .txt file path
output_file = 'output.tex'      # Replace
