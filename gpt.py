from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from env import *
import openai
from langchain.prompts import PromptTemplate
from typing_extensions import Protocol
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import json
from prompt import *

init_env()

_template = """

    Following the previous prompt, write a prompt that describes the following elements:
    {desc}

    You should only respond in JSON format, as described below:
    The return format is as follows:
    {{
        "question":"$YOUR_QUESTION_HERE",
        "answer": "$YOUR_ANSWER_HERE"
    }}
    Make sure the response can be parsed by Python json.loads
    """


class GPTChain:

    def __init__(self, input_var: List, _template: str, output_var: List) -> None:
        llm = ChatOpenAI(model=MODEL, openai_api_key=openai.api_key)
        prompt = PromptTemplate(
            input_variables=input_var,
            template=_template
        )
        # prompt_print = PromptTemplate.from_template(_template)
        # print(prompt_print.format(project="car", sprites="stuff"))
        self.template = _template
        self.chain = LLMChain(prompt=prompt, llm=llm)
        self.input_var = input_var
        self.output_var = output_var

    def print_format(self, input_dict):
        # prompt = PromptTemplate(
        #     input_variables=input_var,
        #     template=_template
        # )
        prompt_print = PromptTemplate.from_template(self.template)
        print(prompt_print.format(input_dict))

    def run(self, text):
        res = self.chain.run(text)
        # 解析json
        result = json.loads(res)
        return result, self.output_var


# text_refine = GPTChain(NewObject.input_var, NewObject.prompt, NewObject.output_var)
# print(text_refine.run({"project": "一个关于龟兔赛跑的故事", "sprites": "[兔子，乌龟，汽车，障碍物]"}))
t2i = GPTChain(T2I.input_var, T2I.prompt, T2I.output_var)
print(t2i.run({"project": "一个关于龟兔赛跑的故事", "drawing": "终点线"}))


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
