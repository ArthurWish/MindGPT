import os
import json
import re
import openai
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv("OPENAI_API_KEY")
# Replace with the actual path to your file
path = '/media/sda1/cyn-workspace/generative_mm/fine-tune/code.jsonl'

# with open(path, 'r') as file:
#     for line in file:
#         record = json.loads(line)
#         print(record)
"""
# List 10 fine-tuning jobs
openai.FineTuningJob.list(limit=10)

# Retrieve the state of a fine-tune
openai.FineTuningJob.retrieve("ftjob-abc123")
"""
# Upload the file to OpenAI


def get_trainfile_id():
    res = openai.File.create(
        file=open(path, "rb"),
        purpose='fine-tune'
    )
    print(res)
    return res["id"]


# file_id = get_trainfile_id()


def fine_tune(training_file):
    print(training_file)
    res = openai.FineTuningJob.create(
        training_file=training_file, model="gpt-3.5-turbo")
    print(res)
    return res


# mode_id = fine_tune(file_id)


def test_model(mode_id):
    # completion = openai.ChatCompletion.create(
    #     model="gpt-4-0613",
    #     messages=[
    #         {"role": "system",
    #             "content": "You are a Scratch programming expert."},
    #         {"role": "user", "content": "When the car collides with an obstacle, the total score is reduced by 1 and the speed is reduced by 5."}
    #     ]
    # )
    # print(completion.choices[0].message)
    # Get output from fine-tuned model
    # ft:gpt-3.5-turbo:my-org:custom_suffix:id
    completion = openai.ChatCompletion.create(
        model=mode_id,
        messages=[
            {"role": "system",
                "content": "You are a Scratch programming expert."},
            {"role": "user", "content": "When the car collides with an obstacle, the total score is reduced by 1 and the speed is reduced by 5."}
        ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message
    # content = openai.File.download("file-abc123")
    # print(content)
# test_model("ft:gpt-3.5-turbo-0613:personal::8H4ae3zZ")

if __name__ == "__main__":
    # print(openai.FineTuningJob.list(limit=10)) 
    # content = openai.File.download("file-i4HPhQsphoWrEpij68dSkUG8")
    # print(content)
    # encoded_string = test_model("ft:gpt-3.5-turbo-0613:personal::8H4ae3zZ")["content"]
    # manual_decoded_string = encoded_string.replace("\u201c", "“")
    final_string = '"when [car] touches [obstacle]","change [Score] by [-1]","set [Speed] to [([Speed]) - (5)]" '
    print(final_string)
    
    extracted_list = re.findall(r'\"(.*?)\"', final_string)
    print(type(extracted_list))