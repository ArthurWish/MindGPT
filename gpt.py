import ast
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from env import *
import openai
from langchain.prompts import PromptTemplate
from typing import List, Dict
from langchain.chains import LLMChain
import json
from prompt import *
import re
init_env()


class GPTChain:

    def __init__(self, input_var: List, _template: str, output_var: List) -> None:
        llm = ChatOpenAI(model=MODEL, openai_api_key=openai.api_key)
        prompt = PromptTemplate(
            input_variables=input_var,
            template=_template
        )
        # # prompt_print = PromptTemplate.from_template(_template)
        # # print(prompt_print.format(project="car", sprites="stuff"))
        self.template = _template
        self.chain = LLMChain(prompt=prompt, llm=llm)
        self.input_var = input_var
        self.output_var = output_var

    def print_format(self, input_dict):
        prompt_print = PromptTemplate.from_template(self.template)
        print(prompt_print.format(input_dict))

    def run(self, text):
        res = self.chain.run(text)
        # 解析json
        result = json.loads(res)
        return result


class FewGPTChain:

    def __init__(self, input_var: List, few_shot_prompt: str, output_var: List) -> None:
        llm = ChatOpenAI(model=MODEL, openai_api_key=openai.api_key)
        self.chain = LLMChain(prompt=few_shot_prompt, llm=llm)
        self.input_var = input_var
        self.output_var = output_var
        self.prompt = few_shot_prompt

    def print_format(self):
        print(self.prompt.format())

    def str_to_list(self, s):
        pattern = re.compile(r"\[\'(.*?)\'\]")
        match = pattern.search(s)
        if not match:
            return None

        content = match.group(1)
        parts = content.split("', '")
        result = [part.replace("\\'", "'") for part in parts]
        return result

    def run(self, text):
        res: str = self.chain.run(text)
        print(res)
        # result = json.loads(res)
        return self.str_to_list(res)

# text_refine = GPTChain(NewObject.input_var, NewObject.prompt, NewObject.output_var)
# print(text_refine.run({"project": "一个关于龟兔赛跑的故事", "sprites": "[兔子，乌龟，汽车，障碍物]"}))
# t2i = GPTChain(T2I.input_var, T2I.prompt, T2I.output_var)
# print(t2i.run({"project": "一个关于龟兔赛跑的故事", "drawing": "终点线"}))


class GPTFineTuned:

    def code_generation(self, content, model_id="ft:gpt-3.5-turbo-0613:personal::8HnuPdtX"):
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[
                {"role": "system",
                    "content": "You are a Scratch programming expert."},
                {"role": "user", "content": content}
            ]
        )
        return re.findall(r'\"(.*?)\"', response.choices[0].message["content"])


def create_chat_completion(messages,
                           model=None,
                           temperature=0,
                           max_tokens=None) -> str:
    """Create a chat completion using the OpenAI API"""
    response = None
    response = openai.ChatCompletion.create(model=model,
                                            messages=messages,
                                            temperature=temperature,
                                            max_tokens=max_tokens)
    if response is None:
        raise RuntimeError("Failed to get response")

    return response.choices[0].message["content"]


def translate_to_english(content):
    """将我给定的文本翻译为英文，只回答结果："""
    temp_memory = []
    temp_memory.append({
        "role":
        "user",
        "content":
        f"""Translate the following Chinese sentences into English:{content}
    """
    })
    # print(temp_memory)
    return create_chat_completion(model="gpt-3.5-turbo",
                                  messages=temp_memory,
                                  temperature=0)


@dataclass
class Memory:
    def __init__(self, model, memory: Dict):
        self.system_message = {
            "role": "system", "content": f"You are a helpful Scratch programming teacher. Your task is to answer my questions based on the mind map below in the form of a dictionary: {memory}"}
        self.model = model
        self.chat_messages = []
        self.chat_messages.append(self.system_message)

    def create_chat_completion(self, messages,
                               temperature=0,
                               max_tokens=None) -> str:
        """Create a chat completion using the OpenAI API"""
        response = None

        response = openai.ChatCompletion.create(model=self.model,
                                                messages=messages,
                                                temperature=temperature,
                                                max_tokens=max_tokens)
        if response is None:
            raise RuntimeError("Failed to get response")

        return response.choices[0].message["content"]

    def add_user_message(self, message):
        self.chat_messages.append(message)
        response = create_chat_completion(self.chat_messages)
        self.chat_messages.append("user")
