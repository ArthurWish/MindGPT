import os
import soundfile as sf
import base64
# from tango import Tango
from io import BytesIO
from env import *

init_env()


# def generate_audio(prompt, steps):
#     """
#     prompt: Rolling thunder with lightning strikes
#     """
#     tango = Tango("declare-lab/tango-full-ft-audiocaps")
#     audio = tango.generate(prompt, steps)

#     # use BytesIO to save audio data, instead of writing to disk
#     with BytesIO() as audio_buffer:
#         sf.write(audio_buffer, audio, samplerate=16000, format='WAV')
#         audio_data = audio_buffer.getvalue()

#     # create the base64 encoded string
#     audio_data_b64 = base64.b64encode(audio_data).decode('utf-8')

#     return audio_data_b64
