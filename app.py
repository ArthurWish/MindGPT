import base64
from flask import Flask, jsonify, request
import os
from flask_cors import CORS
import json
from PIL import Image
from prompt import *
from gpt import GPTChain, create_chat_completion, translate_to_english
app = Flask(__name__)
CORS(app)


@app.route('/api/new_object', methods=['POST'])
def new_object():
    project = request.json.get('project')
    sprites = request.json.get('sprites')
    if sprites is None:
        sprites = ""
    chain = GPTChain(NewObject.input_var, NewObject.prompt, NewObject.output_var)
    new_object = chain.run({"project": project, "sprites": sprites})
    print(new_object["spriteName"]) # description
    print(new_object["description"])
    return jsonify({'spriteName': new_object["spriteName"], 'description': new_object["description"]})

@app.route('/api/text_to_image', methods=['POST'])
def text_to_image():
    text = request.json.get('text')
    chain = GPTChain(T2I.input_var, T2I.prompt, T2I.output_var)
    image_prompt = chain.run({"drawing": text})
    return jsonify({'image_prompt': image_prompt})

@app.route('/api/image_to_image', methods=['POST'])
def image_to_image():
    # TODO
    user_image = request.json.get('user_image')
    image_content = request.json.get('image_content')
    # 对user_image和image_content进行处理，生成image和object_prompt
    # 这里仅作示例，实际处理过程需要根据具体需求编写
    image = "base64_encoded_image_generated_from_" + user_image
    object_prompt = "This is a new image generated from your input image and content"
    return jsonify({'image': image, 'object_prompt': object_prompt})

@app.route('/api/text_to_sound', methods=['POST'])
def text_to_sound():
    # TODO
    text = request.json.get('text')
    # 对text进行处理，生成sound
    # 这里仅作示例，实际处理过程需要根据具体需求编写
    sound = "base64_encoded_sound_generated_from_" + text
    return jsonify({'sound': sound})

@app.route('/api/character_decomposition', methods=['POST'])
def character_decomposition():
    project = request.json.get('project')
    sprite = request.json.get('sprite')
    chain = GPTChain(ScratchFunction.input_var, ScratchFunction.prompt, ScratchFunction.output_var)
    scratch_func = chain.run({"project": project, "sprite": sprite})
    print(scratch_func)
    return jsonify({'function': scratch_func["answer"]})

@app.route('/api/new_logic', methods=['POST'])
def new_logic():
    function = request.json.get('function')
    chain = GPTChain(DetailLogic.input_var, DetailLogic.prompt, DetailLogic.output_var)
    logic = chain.run(function)
    return jsonify({'logic': logic["answer"]})

@app.route('/api/generate_code', methods=['POST'])
def generate_code():
    function = request.json.get('function')
    chain = GPTChain(DetailLogic.input_var, DetailLogic.prompt, DetailLogic.output_var)
    code = chain.run(function)
    scratch_block = "base64_encoded_Scratch_block_image_generated_from_"
    return jsonify({'code': code, 'Scratch_block': scratch_block})

@app.route('/api/new_single_code', methods=['POST'])
def new_single_code():
    content = request.json.get('content')
    # 对content进行处理，生成new_code和Scratch_block
    # 这里仅作示例，实际处理过程需要根据具体需求编写
    new_code = "new_Scratch_code_generated_from_" + content
    scratch_block = "base64_encoded_Scratch_block_image_generated_from_" + content
    return jsonify({'new_code': new_code, 'Scratch_block': scratch_block})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)



