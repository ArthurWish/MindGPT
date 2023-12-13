from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO
import io
import base64
import requests


def extract_block_types(data):
    block_types = []
    for item in data:
        if 'block_type' in item:
            block_types.append(item['block_type'])
            # 如果有嵌套的字典，递归提取
            if 'arguments' in item:
                for key, value in item['arguments'].items():
                    if isinstance(value, dict):
                        block_types.extend(extract_block_types([value]))
    return block_types


def decode_base64_to_image(encoding):
    if encoding.startswith("data:image/"):
        encoding = encoding.split(":")[1].split(",")[1]
    image = Image.open(io.BytesIO(base64.b64decode(encoding)))
    return image


def generate_controlnet(prompt, base_image):
    url = "http://10.73.3.223:55233"
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
