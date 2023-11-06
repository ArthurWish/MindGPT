from prompt import ScratchFunction
from gpt import *
from env import *

init_env()


chain = FewGPTChain(CodeGeneration.input_var,
                    CodeGeneration.final_prompt, CodeGeneration.output_var)
# print("scratch_func" + sprite + project)
scratch_func = chain.run({"logic": "Adjusting the car's direction"})
# print(scratch_func)
import re


def str_to_list(s):
    pattern = re.compile(r"\[\'(.*?)\'\]")
    match = pattern.search(s)
    if not match:
        return None
    
    content = match.group(1)
    parts = content.split("', '")
    result = [part.replace("\\'", "'") for part in parts]
    return result

lst = str_to_list(scratch_func)
print(lst)


