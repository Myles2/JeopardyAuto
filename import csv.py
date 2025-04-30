import csv
import json
import os
import random

def load_questions_from_csv(csv_filename):
    questions = []
    with open(csv_filename, newline='', encoding='utf-8-sig', errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # Ensure the point value is valid (non-empty and an integer)
            try:
                point_value = int(row[0]) if row[0].strip() else None
            except ValueError:
                continue  # Skip rows where point value is invalid
            
            # Only process rows with a valid point value
            if point_value is not None:
                questions.append({
                    "value": point_value,
                    "clue": row[1],
                    "solution": row[2]
                })
    return questions

def generate_game_json(categories_folder, output_filename):
    # Initialize lists to hold the categories for both rounds
    single_categories = []
    double_categories = []

    # Get a list of all CSV files in the folder
    all_files = [f for f in os.listdir(categories_folder) if f.endswith('.csv')]

    # Choose only 6 random CSV files (i.e., 6 categories) for the single round
    selected_files_single = random.sample(all_files, 6)

    # Loop through the selected files for the single round
    for filename in selected_files_single:
        category_name = os.path.splitext(filename)[0]  # Use filename (without extension) as the category name
        questions = load_questions_from_csv(os.path.join(categories_folder, filename))

        # Sort questions by value (ascending order)
        questions.sort(key=lambda x: x["value"])

        # Initialize lists for single jeopardy clues
        category_clues_single = []

        # Ensure exactly one question for each point value (100, 200, 300, 400, 500) in single jeopardy
        point_values_single = [100, 200, 300, 400, 500]

        # Select one question for each point value for the single round
        for point_value in point_values_single:
            question = next((q for q in questions if q["value"] == point_value), None)
            if question:
                category_clues_single.append(question)

        # Add category to single jeopardy list
        single_categories.append({
            "category": category_name,
            "clues": category_clues_single
        })

    # Choose 6 random CSV files (i.e., 6 categories) for the double round
    selected_files_double = random.sample(all_files, 6)

    # Loop through the selected files for the double round
    for filename in selected_files_double:
        category_name = os.path.splitext(filename)[0]  # Use filename (without extension) as the category name
        questions = load_questions_from_csv(os.path.join(categories_folder, filename))

        # Sort questions by value (ascending order)
        questions.sort(key=lambda x: x["value"])

        # Initialize lists for double jeopardy clues
        category_clues_double = []

        # Ensure exactly one question for each point value (200, 400, 600, 800, 1000) in double jeopardy
        point_values_double = [200, 400, 600, 800, 1000]

        # Shuffle questions randomly to create new random questions for double jeopardy
        random.shuffle(questions)

        # Select questions for double jeopardy and double the values (200, 400, 600, 800, 1000)
        for point_value in point_values_double:
            question = next((q for q in questions if q["value"] == point_value // 2), None)
            if question:
                # Create a new question for double jeopardy with doubled point value
                doubled_question = question.copy()
                doubled_question["value"] = point_value
                category_clues_double.append(doubled_question)

        # Add category to double jeopardy list
        double_categories.append({
            "category": category_name,
            "clues": category_clues_double
        })

        # Create the final jeopardy clue (pick one random clue from all categories with a value of 300 or above)
    all_clues = [clue for category in single_categories for clue in category["clues"]]
    all_clues.extend([clue for category in double_categories for clue in category["clues"]])

    # Filter clues to include only those with a value of 300 or above
    valid_final_clues = [clue for clue in all_clues if clue["value"] in [300, 400]]

    # Choose a random final clue from the valid ones
    final_clue = random.choice(valid_final_clues) if valid_final_clues else None

    # Construct the game dictionary
    game_data = {
        "game": {
            "single": single_categories,
            "double": double_categories,
            "final": {
                "category": "Final Question",
                "clue": final_clue["clue"] if final_clue else "No valid clue available",
                "solution": final_clue["solution"] if final_clue else "No valid solution available"
            }
        }
    }


    # Write the JSON data to a file
    with open(output_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(game_data, jsonfile, indent=4)

# Specify the folder where your CSV files are located and the output JSON filename
categories_folder = 'categories'  # Folder containing your CSV files
output_filename = 'ZionJeopardy.json'  # Name of the output JSON file

# Generate the game JSON and save to file
generate_game_json(categories_folder, output_filename)

