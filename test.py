from env import *

from prompt import *
init_env()
memory = Memory(system_message="chatbot")
content = memory.completion(input="Not too bad - how are you?")
print(content)