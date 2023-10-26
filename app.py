import base64
import io
from flask import Flask, jsonify, request
import os
from flask_cors import CORS
import json
from PIL import Image
from prompt import *
from gpt import GPTChain, create_chat_completion, translate_to_english
from image import generate_controlnet, generate_draw

app = Flask(__name__)
CORS(app)
os.makedirs('./static', exist_ok=True)
os.makedirs('./static/images', exist_ok=True)

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
    text = request.json.get('text') # user input
    image_base64 = request.json.get('user_image') # base64
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
    chain = GPTChain(ScratchFunction.input_var,
                     ScratchFunction.prompt, ScratchFunction.output_var)
    scratch_func = chain.run({"project": project, "sprite": sprite})
    print(scratch_func)
    return jsonify({'function': scratch_func["answer"]})


@app.route('/api/new_logic', methods=['POST'])
def new_logic():
    function = request.json.get('function')
    previous_logic = request.json.get('previous_logic')
    chain = GPTChain(DetailLogic.input_var,
                     DetailLogic.prompt, DetailLogic.output_var)
    logic = chain.run({"funcion": function, "previous_logic": previous_logic})
    return jsonify({'logic': logic["answer"]})


@app.route('/api/generate_code', methods=['POST'])
def generate_code():
    logic = request.json.get('logic')
    chain = GPTChain(CodeGeneration.input_var,
                     CodeGeneration.prompt, CodeGeneration.output_var)
    code = chain.run(logic)
    scratch_block = "base64_encoded_Scratch_block_image_generated_from_"
    return jsonify({'code': code, 'Scratch_block': scratch_block})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)
