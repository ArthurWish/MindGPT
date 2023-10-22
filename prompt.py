from dataclasses import dataclass


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
        You are an expert on prompt engineering for text to image generation. Here is a text description: {drawing}
        I will give you a example, fill the prompt with knowledge for <{drawing}>. 
        template "[character], [artist], [style]", Example:Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k.
        The return format is as follows:
        {{
            "prompt": "$YOUR_PROMPT"
        }}
        Make sure the response can be parsed by Python json.loads
    """

@dataclass
class ScratchFunction:
    # 将一个编程对象Sprite分解为编程函数
    input_var = ["project", "sprite"] # 
    output_var = ["question", "answer"]
    prompt = """
        You are an expert on task decomposition. Solve a question answering task with interleaving Thought. I have a Scratch project about {project}, and a sprite about {sprite} Decompose the sprite to generate functions that can be used for Scratch programming. No explanation.
        Here are some examples.
        Question: ["Car"]
        Answer: ["Keep the car moving", "Adjust the car's direction", "Stop the car at end line"]
        Question: ["Track"]
        Answer: ["Touching the track causes the track to change color"]
        Question: ["obstacle"]
        Answer: ["Make a sound when hitting an obstacle", "Getting closer to an obstacle makes the car make a sound"]
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
    input_var = ["fuction", "previous_logic"] # 
    output_var = ["question", "answer"]
    prompt = """
        You are an expert on Scratch programming logic. Solve a question answering task with interleaving Thought. I have a Scratch function about {function}. Give me some programming logic that the function can use. No explanation.
        Here are some examples.
        Question: ["Keep the car moving"]
        Answer: ["Initial position", "Control direction"]
        Question: ["Adjusting the car's direction"]
        Answer: ["when the car veers off track to the left", "when the car veers off track to the right"]
        Question: ["when the car veers off track to the left"]
        Answer: ["Determine statement", "Conditional statement", "Motion"]
        You should only respond in JSON format, as described below:
        The return format is as follows:
        {{
            "question": "$MY_QUESTION",
            "answer": "$YOUR_ANSWER"
        }}
        Make sure the response can be parsed by Python json.loads
    """
    
@dataclass   
class CodeGeneration:
    # 将得到的Scratch函数细化为编程逻辑，可以无限细化
    input_var = ["logic"] # 
    output_var = ["question", "answer"]
    prompt = """
        You are an expert on Scratch programming logic. Solve a question answering task with interleaving Thought. I have a Scratch function about {function}. Give me some programming logic that the function can use. No explanation.
        Here are some examples.
        Question: ["Keep the car moving"]
        Answer: ["Initial position", "Control direction"]
        Question: ["Adjusting the car's direction"]
        Answer: ["when the car veers off track to the left", "when the car veers off track to the right"]
        Question: ["when the car veers off track to the left"]
        Answer: ["Determine statement", "Conditional statement", "Motion"]
        You should only respond in JSON format, as described below:
        The return format is as follows:
        {{
            "question": "$MY_QUESTION",
            "answer": "$YOUR_ANSWER"
        }}
        Make sure the response can be parsed by Python json.loads
    """