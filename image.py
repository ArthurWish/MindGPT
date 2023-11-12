import base64
import configparser
import io
import requests
import openai
from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO
from rembg import remove
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import json

# 解码图像


def decode_base64_to_image(encoding):
    if encoding.startswith("data:image/"):
        encoding = encoding.split(":")[1].split(",")[1]
    image = Image.open(io.BytesIO(base64.b64decode(encoding)))
    return image


def generate_draw_with_stable_v2(prompt, save_path):
    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, ugly arms, ugly hands, ugly teeth, ugly nose, ugly mouth, ugly eyes, ugly ears,",
        "steps": 25,
        "sampler_name": "Euler a",
        "cfg_scale": 7,
        "width": 512,
        "height": 512
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    data = response.json()
    for encoded_result in data['images']:
        result_data = base64.b64decode(encoded_result)
        with open(f"{save_path}.png", "wb") as f:
            f.write(result_data)
        # image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
    # for i, image in enumerate(data["artifacts"]):
        # image_data = image["base64"]
        # with open(f"{save_path}.png", "wb") as f:
            # f.write(b64decode(image["base64"]))
    # only use for single image
    return encoded_result


def generate_draw(drawing_content, save_path):
    
    # TODO 多卡推断
    # image_data = t2i.inference(agent_reply, save_path)
    image_data = generate_draw_with_stable_v2(drawing_content, save_path)
    return image_data


def generate_controlnet(prompt, base_image):
    url = "http://127.0.0.1:7860"
    print("[image to image]starting generating image on the basis of controlnet...")
    print("[txt to image with controlnet]starting generating image on the basis of controlnet...")
    print("[image to prompt]", prompt)
    image = Image.open(base_image)
    resized_image = image.resize((512, 512))
    with io.BytesIO() as buffer:
        resized_image.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    payload = {
        "prompt": prompt,
        # "Digital art, a colorful bird, by studio ghibli, makoto shinkai, by artgerm, by wlop, by greg rutkowski, Vivid Colors, white background,simple background",
        "negative_prompt": "ugly, ugly arms, ugly hands, ugly teeth, ugly nose, ugly mouth, ugly eyes, ugly ears,scary,handicapped,",
        "batch_size": 1,
        "steps": 30,
        "sampler_name": "Euler a",
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "script_args": ["outpainting mk2", ],
        "alwayson_scripts": {
            "ControlNet": {
                "args": [
                    {
                        "enabled": True,
                        "input_image": img_base64,
                        # "control_type":"Scribble"
                        # "module": 'scribble_xdog',
                        "model": 'control_v11p_sd15_scribble [d4ba51ff]',
                        "control_mode": 1,  # "My prompt is more important"
                        "module": "invert"
                        # "starting_control_step":0,
                        # "ending_control_step":1,
                        # "guessmode":False
                    }
                ]
            }
        }
    }
    response = requests.post(
        url=f'{url}/sdapi/v1/txt2img', json=payload)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    image = decode_base64_to_image(response.json()['images'][0])
    image.save("./image_to_image.png", format='PNG')

    return data['images'][0]
