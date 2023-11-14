"""Remove Polish Characters from Movie Ratings Dataset, Rostkowski Wiktor, Jan Szenborn, 2023

Instructions:
1. Run the script:
   - Open a terminal and navigate to the script's directory.
   - Execute the following command to remove Polish characters and create a new dataset:
     ```
     pip install unidecode
     python recodeJson.py
     ```
   - The script will process the input file ('polskiPlik.json'), remove Polish characters, and save the modified dataset to 'output.json'.
"""

import json
from unidecode import unidecode


def remove_polish_characters(input_str):
    return unidecode(input_str)


def remove_polish_from_dict(input_dict):
    return {remove_polish_characters(key): {remove_polish_characters(movie): rating for movie, rating in value.items()}
            for key, value in input_dict.items()}


if __name__ == '__main__':
    input_file = 'polskiPlik.json'
    output_file = 'output.json'

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    data_without_polish = remove_polish_from_dict(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_without_polish, f, ensure_ascii=False, indent=4)

    print(f"Polish characters removed and saved to {output_file}")
