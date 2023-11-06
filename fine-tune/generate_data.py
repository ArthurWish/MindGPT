import pandas as pd
import json

# Load the Excel file
file_path = './Codebase.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows to understand the structure of the file
# print(data.head())

# Define a function to format the data as specified in the JSON structure
def format_json(row):
    return {
        "messages": [
            {"role": "system", "content": "You are a Scratch programming expert."},
            {"role": "user", "content": row['prompt']},
            {"role": "assistant", "content": row['completion']}
        ]
    }

# Apply the formatting function to each row in the DataFrame
formatted_data = data.apply(format_json, axis=1)

# Convert the Series of JSON objects into a list
json_list = formatted_data.tolist()

# Display the first few formatted JSON objects for verification
# print(json_list[:5])
with open('./code.jsonl', 'w', encoding='utf-8') as file:
    for json_object in json_list:
        file.write(json.dumps(json_object, ensure_ascii=False) + '\n')