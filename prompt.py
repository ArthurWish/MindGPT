from dataclasses import dataclass
import json
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)
# PROMPT_NEW = json.load(open("./scratch_prompt.json", "r"))


@dataclass
class NewObject:
    input_var = ["project", "sprites"]
    output_var = ["spriteName", "description"]
    prompt = """
        The following is a Scratch project that children will want to complete: {project}.
        Sprites designed for children include: {sprites}.
        Your task is to generate signle creative and simple sprites for children based on the project theme and already designed sprites. These generated sprites should be suitable for programming with Scratch.
        You should only respond in JSON format, as described below:
        The return format is as follows:
        {{
            "spriteName": "$YOUR_SPRITE_NAME",
            "description": "$YOUR_SPRITE_DESCRIPTION"
        }}
        Make sure the response can be parsed by Python json.loads
    """


@dataclass
class T2I:
    input_var = ["drawing"]
    output_var = ["prompt"]
    prompt = """
        You are an expert on prompt engineering for text to image generation. Here is a text description: {drawing}, fill the prompt with knowledge for <{drawing}>
        I will give you a example.
        prompt: "Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k."
        The return format is as follows:
        {{
            "prompt": "$YOUR_PROMPT"
        }}
        Make sure the response can be parsed by Python json.loads
    """


@dataclass
class NewScraScratchFunction:
    # TODO: 采用openai的格式
    prompt = """
        I have Scratch sprite about {sprite}. Your task is that generate some functions of this sprite that can be used for Scratch programming.
        Following are some examples.
        sprite: ["car"]
        functions: ["Keep the car moving",
            "Adjust the car's direction", "Stop the car at end line"]
        sprite: ["Track"]
        functions: ["Touching the track causes the track to change color"]
        sprite: ["obstacle"]
        functions: ["Make a sound when hitting an obstacle",
            "Getting closer to an obstacle makes the car make a sound"]

        You should only respond in JSON format, as described below:
        The return format is as follows:
        {{
            "functions": "$GENERATED_FUNCSIONS"
        }}
        Make sure the response can be parsed by Python json.loads
    """


@dataclass
class ScratchFunction:
    # 将一个编程对象Sprite分解为编程函数
    input_var = ["sprite"]
    output_var = ["question", "answer"]
    examples = [
        {"sprite": "I have a Scratch project about racing game, and I have a sprite named car", "functions": [
            "Keep the car moving", "Adjust the car's direction", "Stop the car at end line"]},
        {"sprite": "I have a Scratch project about racing game, and I have a sprite named track", "functions": [
            "Touching the track causes the track to change color"]},
        {"sprite": "I have a Scratch project about racing game, and I have a sprite named obstacle", "functions": [
            "Make a sound when hitting an obstacle", "Getting closer to an obstacle makes the car make a sound"]}
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{sprite}"),
            ("ai", "{functions}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a Scratch programming teacher. Your task is that generate some functions of this sprite that can be used for Scratch programming."),
            few_shot_prompt,
            ("human", "{sprite}"),
        ]
    )


@dataclass
class a:
    input_var = ["function", "previous_logic"]
    output_var = ["question", "answer"]
    prompt = """
        You are an expert on Scratch programming. Solve a question answering task with interleaving Thought. I have a Scratch function about {function} and the written programming logic includes {previous_logic}. Give me programming logic that conforms {function}.
        Here are some examples.
        question: ["Keep the car moving"]
        answer: ["Initial position", "Control direction"]
        question: ["Adjusting the car's direction"]
        answer: ["when the car veers off track to the left", "when the car veers off track to the right"]
        question: ["when the car veers off track to the left"]
        answer: ["Determine statement", "Conditional statement", "Motion"]
        You should only respond in JSON format, as described below:
        The return format is as follows:
        {{
            "question": "$MY_QUESTION",
            "answer": "$YOUR_ANSWER"
        }}
        Make sure the response can be parsed by Python json.loads
    """


@dataclass
class DetailLogic:
    # 将分解得到的Scratch函数细化为编程逻辑，可以无限细化
    # TODO 在prompt中加入已经输入的内容
    input_var = ["function", "previous_logic"]
    output_var = ["question", "answer"]
    examples = [
        {"function": "I have a function: Keep the car moving", "logic": [
            "Initial position", "Control direction"]},
        {"function": "I have a function: Adjusting the car's direction", "logic": [
            "when the car veers off track to the left", "when the car veers off track to the right"]},
        {"function": "I have a function: when the car veers off track to the left", "logic": [
            "Determine statement", "Conditional statement", "Motion control"]}
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{function}"),
            ("ai", "{logic}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    # print(few_shot_prompt.format())
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a Scratch programming teacher. Your task is that generate some programming logic of this function that can be used for Scratch programming."),
            few_shot_prompt,
            ("human", "{function}"),
        ]
    )


@dataclass
class CodeGeneration:

    input_var = ["logic", "previous_code"]
    output_var = ["question", "answer"]
    examples = [
        {"logic": "Click on the character to switch to the next costume", 
         "code": [
         "when this sprite clicked",
         "switch costume to []",
         "wait [0.3] seconds",
         "switch costume to []",
         "wait [0.3] seconds"
         ]},
        {"logic": "Click on the green flag to change the background and make the character talk", 
         "code": [
         "when green flag clicked",
         "switch backdrop to [Savanna]",
         "wait [2] seconds",
         "switch backdrop to [Metro]",
         "say [Let's explore] for [2] seconds"
         ]},
        {"logic": "Click on the character to change the color and play the sound", 
         "code": [
         "when this sprite clicked",
         "change [color] effect by [25]",
         "play sound [Magic Spell]"
         ]}
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{logic}"),
            ("ai", "{code}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    # print(few_shot_prompt.format())
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a Scratch programming teacher. Your task is that generate Scratch codes of this logic that can be used for Scratch programming."),
            few_shot_prompt,
            ("human", "{logic}"),
        ]
    )

    # 将得到的编程逻辑生成Scratch文本形式代码
    # input_var = ["logic", "previous_code"]
    # output_var = ["question", "answer"]
#     prompt = """
#         You are an expert on Scratch programming. Solve a question answering task with interleaving Thought. I have a programming logic about {logic} and the written Scratch blocks includes {previous_code}. Give me Scratch codes that conforms {logic}.
#         Here are some examples.
#         {
#       "question": "点击角色，切换到下一个costume",
#       "answer": [
#          "when this sprite clicked",
#          "switch costume to []",
#          "wait [0.3] seconds",
#          "switch costume to []",
#          "wait [0.3] seconds"
#       ]
#    },
#    {
#       "question": "点击绿旗，改变背景并使角色说话",
#       "answer": [
#          "when green flag clicked",
#          "switch backdrop to [Savanna]",
#          "wait [2] seconds",
#          "switch backdrop to [Metro]",
#          "say [Let's explore] for [2] seconds"
#       ]
#    },
#    {
#       "question": "点击绿旗，如果触碰到角色就播放声音",
#       "answer": [
#          "when green flag clicked",
#          "forever",
#          "if touching [star] then",
#          "play sound [Collect] until done"
#       ]
#    },
#    {
#       "question": "点击绿旗，如果触碰到角色播放声音并增加分数",
#       "answer": [
#          "when green flag clicked",
#          "set [Score] to [0]",
#          "forever",
#          "if touching [star] then",
#          "change [Score] by [1]",
#          "play sound [Collect] until done"
#       ]
#    },
#    {
#       "question": "点击绿旗，当分数足够切换背景",
#       "answer": [
#          "when green flag clicked",
#          "switch backdrop to []",
#          "wait until (Score) == (10)",
#          "switch backdrop to [Nebula]",
#          "when backdrop switches to [Nebula]",
#          "play sound [Win] until done"
#       ]
#    },
#    {
#       "question": "按下空格，使角色跳起来",
#       "answer": [
#          "when [space] key pressed",
#          "change y by [60]",
#          "wait [0.3] seconds",
#          "change y by [-60]"
#       ]
#    },
#    {
#       "question": "按下空格，改变角色姿势",
#       "answer": [
#          "when [space] key pressed",
#          "switch costume to [max-c]",
#          "wait [0.3] seconds",
#          "switch costume to [max-b]"
#       ]
#    },
#    {
#       "question": "点击绿旗，实现角色跑步动画",
#       "answer": [
#          "when green flag clicked",
#          "go to x:[-140],y:[-60]",
#          "repeat [50]",
#          "move [10] steps",
#          "next costume"
#       ]
#    },
#    {
#       "question": "点击绿旗，使两个角色对话",
#       "answer": [
#          "when green flag clicked",
#          "say [I have a pet owl!] for [2] seconds",
#          "wait [2] seconds",
#          "when green flag clicked",
#          "wait [2] seconds",
#          "say [What's its name] for [2] seconds"
#       ]
#    },
#    {
#       "question": "点击角色，改变颜色，播放声音",
#       "answer": [
#          "when this sprite clicked",
#          "change [color] effect by [25]",
#          "play sound [Magic Spell]"
#       ]
#    }
#         You should only respond in JSON format, as described below:
#         The return format is as follows:
#         {{
#             "question": "$MY_QUESTION",
#             "answer": "$YOUR_ANSWER"
#         }}
#         Make sure the response can be parsed by Python json.loads
#     """
