import base64
import io
import re
from flask import Flask, jsonify, request, make_response
import os
from flask_cors import CORS, cross_origin
import json
from PIL import Image
import requests
from prompt import *
from gpt import *
from image import generate_controlnet, generate_draw
from prompt_base import *
app = Flask(__name__)
CORS(app, resources=r"/*", supports_credentials=True, origins='*')
os.makedirs('./static', exist_ok=True)
os.makedirs('./static/images', exist_ok=True)

object_memory = Memory(model=GPTType.gpt_4)
function_memory = Memory(model=GPTType.gpt_4)
logic_memory = Memory(model=GPTType.gpt_4)


@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'


@app.route('/api/new_object', methods=['POST'])
def new_object():
    project = request.json.get('project')
    memory_dict = request.json.get('memory_dict')
    print(project, memory_dict)
    if project is None:
        return "project is none"
    user_message = object_prompt.format(memory=memory_dict)
    response = object_memory.ask_gpt(user_message=user_message)
    print("response", response)
    response = json.loads(response)
    # print("response["object"]", response["object"])  # description
    # print(response["description"])
    return jsonify({'spriteName': response["object"], 'description': response["description"]})


@app.route('/api/text_to_image', methods=['POST'])
def text_to_image():
    text = request.json.get('text')
    drawing_agent = GPTTools(GPTType.gpt_3, "Output the IDEA in JSON format.")
    response = drawing_agent.create_chat_completion(
        user_message=drawing_prompt.format(drawing=text))
    response = json.loads(response)
    print("prompt", response['prompt'])
    image_base64 = generate_draw(response["prompt"], './static/test.png')
    return jsonify({'image': image_base64})


@app.route('/api/image_to_image', methods=['POST'])
def image_to_image():
    print("image_to_image")
    text = request.json.get('text')  # user input
    image_base64 = request.json.get('user_image')  # base64
    if image_base64 is None:
        return "image_base64 is none"
    base_img_bytes = base64.b64decode(image_base64)
    img = Image.open(io.BytesIO(base_img_bytes)).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255))
    combined = Image.alpha_composite(bg, img)
    combined.convert('RGB').save('./static/temp.png', 'PNG')
    drawing_agent = GPTTools(GPTType.gpt_3, "Output the IDEA in JSON format.")
    response = drawing_agent.create_chat_completion(
        user_message=drawing_prompt.format(drawing=text))
    response = json.loads(response)
    print("prompt", response['prompt'])
    image_base64 = generate_controlnet(
        prompt=response['prompt'], base_image="./static/temp.png")
    return jsonify({'image': image_base64})


@app.route('/api/text_to_sound', methods=['POST'])
def text_to_sound():
    """ audio generate api version """
    api_url = 'http://127.0.0.1:5555/generate'
    prompt = request.json.get('prompt')
    steps = 200
    data = {
        "prompt": prompt,
        "steps": steps
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    # audio_data_b64 = generate_audio(prompt, steps)
    if response.status_code == 200:
        audio_data_b64 = response.json()['audio_data']
    # print(audio_data_b64)
    return jsonify({'sound': audio_data_b64})


@app.route('/api/character_decomposition', methods=['POST'])
def character_decomposition():
    question = request.json.get('question')
    memory_dict = request.json.get('memory_dict')
    if memory_dict is None:
        return "Input the mind map"
    user_message = function_prompt.format(
        question=question, memory=memory_dict)
    response = function_memory.ask_gpt(user_message=user_message)
    print("response", response)
    response = json.loads(response)
    return jsonify({'answer': response["function"]})
    # return jsonify({'answer': scratch_func["answer"]})


@app.route('/api/new_logic', methods=['POST'])
def new_logic():
    question = request.json.get('question')
    memory_dict = request.json.get('memory_dict')
    # print(function)
    if memory_dict is None:
        return "Input the mind map"
    user_message = logic_prompt.format(
        question=question, memory=memory_dict)
    response = logic_memory.ask_gpt(user_message=user_message)
    print("response", response)
    response = json.loads(response)
    return jsonify({'logic': response["logic"]})


@app.route('/api/generate_code', methods=['POST'])
def generate_code():
    logic = request.json.get('logic')
    gpt_tuned = GPTFineTuned("ft:gpt-3.5-turbo-0613:personal::8HnuPdtX")
    code = gpt_tuned.code_generation(logic)
    # extracted_list = re.findall(r'\"(.*?)\"', code)
    return jsonify({'code': code})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)
