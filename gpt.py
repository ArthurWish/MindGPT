import ast
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from env import *
from openai import OpenAI
from langchain.prompts import PromptTemplate
from typing import List, Dict
from langchain.chains import LLMChain
import json
from prompt import *
import re

init_env()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client.api_key = os.getenv("OPENAI_API_KEY")


class GPTChain:

    def __init__(self, input_var: List, _template: str, output_var: List) -> None:
        llm = ChatOpenAI(model=MODEL, openai_api_key=client.api_key)
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
        llm = ChatOpenAI(model=MODEL, openai_api_key=client.api_key)
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

    def __init__(self, model_id) -> None:
        self.model_id = model_id

    def code_generation(self, user_message):
        response = client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system",
                    "content": "You are a Scratch programming expert."},
                {"role": "user", "content": user_message}
            ]
        )
        return re.findall(r'\"(.*?)\"', response.choices[0].message.content)


def create_chat_completion(messages,
                           model=MODEL,
                           temperature=0,
                           max_tokens=None) -> str:
    """Create a chat completion using the OpenAI API"""
    response = None
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=temperature,
                                              max_tokens=max_tokens)
    if response is None:
        raise RuntimeError("Failed to get response")

    return response.choices[0].message.content


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
class GPTType:
    gpt_3 = "gpt-3.5-turbo-1106"
    gpt_4 = "gpt-4-1106-preview"


class GPTTools:
    # TODO 完成不同类型任务切换不同能力的gpt
    def __init__(self, model, system_prompt) -> None:
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]

    def create_chat_completion(self, user_message,
                               temperature=0,
                               max_tokens=None) -> str:
        """Create a chat completion using the OpenAI API"""
        user_message = {"role": "user", "content": user_message}
        self.messages.append(user_message)
        response = client.chat.completions.create(model=self.model,
                                                  messages=self.messages,
                                                  response_format={
                                                      "type": "json_object"},
                                                  temperature=temperature,
                                                  max_tokens=max_tokens)
        if response is None:
            raise RuntimeError("Failed to get response")

        return response.choices[0].message.content


class Memory:
    def __init__(self, model):
        self.system_message = {
            "role": "system", "content": "You are a helpful Scratch programming teacher. The return format is JSON format."}
        self.model = model
        self.chat_messages = []
        self.chat_messages.append(self.system_message)

    def create_chat_completion(self, messages,
                               temperature=0,
                               max_tokens=None) -> str:
        """Create a chat completion using the OpenAI API"""
        response = None

        response = client.chat.completions.create(model=self.model,
                                                  messages=messages,
                                                  response_format={
                                                      "type": "json_object"},
                                                  temperature=temperature,
                                                  max_tokens=max_tokens)
        if response is None:
            raise RuntimeError("Failed to get response")
        return response.choices[0].message.content

    def ask_gpt(self, user_message):
        self.chat_messages.append({"role": "user", "content": user_message})
        print(self.chat_messages)
        response = self.create_chat_completion(self.chat_messages)
        self.chat_messages.append({"role": "assistant", "content": response})
        return response
