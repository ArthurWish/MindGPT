import IPython
import soundfile as sf
from tango import Tango

tango = Tango("declare-lab/tango-full-ft-audiocaps")

prompt = "An audience cheering and clapping"
audio = tango.generate(prompt)
sf.write(f"{prompt}.wav", audio, samplerate=16000)
IPython.display.Audio(data=audio, rate=16000)