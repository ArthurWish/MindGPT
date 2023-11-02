import base64
import io
from typing import List
from flask import Flask, jsonify, request, make_response
import os
from flask_cors import CORS, cross_origin
import json
from PIL import Image
import requests
from prompt import *
from gpt import FewGPTChain, GPTChain, create_chat_completion, translate_to_english
from image import generate_controlnet, generate_draw

app = Flask(__name__)
CORS(app, resources=r"/*", supports_credentials=True, origins='*')
# CORS(app, resources=r"/*")
os.makedirs('./static', exist_ok=True)
os.makedirs('./static/images', exist_ok=True)


@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'


@app.route('/api/new_object', methods=['POST'])
def new_object():
    project = request.json.get('project')
    sprites = request.json.get('sprites')
    if sprites is None:
        sprites = ""
    chain = GPTChain(NewObject.input_var, NewObject.prompt,
                     NewObject.output_var)
    new_object = chain.run({"project": project, "sprites": sprites})
    print(new_object["spriteName"])  # description
    print(new_object["description"])
    return jsonify({'spriteName': new_object["spriteName"], 'description': new_object["description"]})


@app.route('/api/text_to_image', methods=['POST'])
def text_to_image():
    text = request.json.get('text')
    chain = GPTChain(T2I.input_var, T2I.prompt, T2I.output_var)
    content = chain.run({"drawing": translate_to_english(text)})
    prompt = content["prompt"]
    image_base64 = generate_draw(prompt, './static/test.png')
    return jsonify({'image': image_base64})


@app.route('/api/image_to_image', methods=['POST'])
def image_to_image():
    text = request.json.get('text')  # user input
    image_base64 = request.json.get('user_image')  # base64
    base_img_bytes = base64.b64decode(image_base64)
    img = Image.open(io.BytesIO(base_img_bytes)).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255))
    combined = Image.alpha_composite(bg, img)
    combined.convert('RGB').save('./static/temp.png', 'PNG')
    chain = GPTChain(T2I.input_var, T2I.prompt, T2I.output_var)
    content = chain.run({"drawing": translate_to_english(text)})
    image_base64 = generate_controlnet(
        prompt=content['prompt'], base_image="./static/temp.png")
    return jsonify({'image': image_base64})


@app.route('/api/text_to_sound', methods=['POST'])
def text_to_sound():
    api_url = 'http://127.0.0.1:5555/generate'
    prompt = request.json.get('text')
    steps = 200
    data = {
        "prompt": prompt,
        "steps": steps
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        audio_data_b64 = response.json()['audio_data']
    return jsonify({'sound': audio_data_b64})


@app.route('/api/character_decomposition', methods=['POST'])
def character_decomposition():
    project = request.json.get('project')
    sprite = request.json.get('sprite')
    chain = FewGPTChain(ScratchFunction.input_var,
                        ScratchFunction.final_prompt, ScratchFunction.output_var)
    # print("scratch_func" + sprite + project)
    scratch_func: List = chain.run({"sprite": sprite})
    return jsonify({'answer': scratch_func})
    # return jsonify({'answer': scratch_func["answer"]})


@app.route('/api/new_logic', methods=['POST'])
def new_logic():
    function = request.json.get('function')
    previous_logic = request.json.get('previous_logic')
    # print(function)
    chain = FewGPTChain(DetailLogic.input_var,
                        DetailLogic.final_prompt, DetailLogic.output_var)
    logic = chain.run({"function": function})

    return jsonify({'logic': logic})


@app.route('/api/generate_code', methods=['POST'])
def generate_code():
    logic = request.json.get('logic')
    previous_code = request.json.get('previous_code')
    chain = FewGPTChain(CodeGeneration.input_var,
                     CodeGeneration.final_prompt, CodeGeneration.output_var)
    code = chain.run({"logic": logic})
    # scratch_block = "base64_encoded_Scratch_block_image_generated_from_"
    return jsonify({'code': code})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)
