from env import *

from prompt import *
from gpt import *
init_env()
gpt_ = GPTFineTuned()
print(gpt_.code_generation(content="当汽车碰到障碍物，分数减1，颜色变红"))