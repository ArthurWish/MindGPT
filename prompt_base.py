object_prompt = """
    Your task is to first extract the programming objects that already exist in the mind map, and then generate new ones based on the theme of the mind map. If you think the object does not exist, generate a new one.
    The generated object should not duplicate the content of the mind map, and the description must be concise to meet the level of children.
    Following are some examples.
    Mind map: {{
        "赛车游戏": {{
            "车": {{
                "描述": "一辆蓝色的车"
            }},
            "障碍物": {{
                "描述": "用来阻挡车"
            }}
        }}
    }}
    Extracted objects: ["车", "障碍物"]
    Generated object: {{ "赛道": "汽车应该在赛道内行驶" }}
    
    Mind map: {{
        "小猫钓鱼": {{
            "小猫": {{
                "描述": "一只白色的可爱小猫"
            }},
            "鱼": {{
                "描述": "在水里游的鱼"
            }}
        }}
    }}
    Extracted objects: ["小猫", "鱼"]
    Generated object: {{ "钓鱼竿": "猫手里的鱼竿，用来钓鱼" }}
    The following is a mind map that children will want to complete: {memory}.
    No need to write down the reasoning process, just tell me the final result. The return format is as follows:
    {{
        "object": "$object"
        "description": "$description"
    }}
    Make sure the response can be parsed by Python json.loads.
"""


drawing_prompt = """
    The following is a mind map that children want to complete: {memory}.
    You are an expert on prompt engineering for text to image generation. Here is a text description: {drawing}, fill the prompt with knowledge for <{drawing}>
    I will give you a example.
    prompt: "Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k."
    The return format is as follows:
    {{
        "prompt": "$YOUR_PROMPT"
    }}
    Make sure the response can be parsed by Python json.loads
"""

function_prompt = """
    Your task is to first extract the programming functions that already exist in the mind map, and then generate new ones based on the theme of the mind map. If you think the functions does not exist, generate a new one.
    The generated function should not duplicate the content of the mind map, and the description must be concise to meet the level of children.
    Following are some examples.
    Question: Generate a new function of car
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": ["Keep the car moving", "Adjust the car's direction"]
            }},
        "track": {{
                "function": ["Touching the track causes the track to change color"]
            }}
    }}
    Extracted functions: ["Keep the car moving", "Adjust the car's direction"]
    Generated function: {{ "car": "Stop the car at end line" }}
    Question: Generate a new function of track
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": ["Keep the car moving", "Adjust the car's direction"]
            }},
        "track": {{
                "function": ["Touching the track causes the track to change color"]
            }}
    }}
    Extracted functions: ["Touching the track causes the track to change color"]
    Generated function: {{ "track": "Make a sound when approaching the track" }}
    Question: {question}
    Mind map: {memory}
    No need to write down the reasoning process, just tell me the final result. The return format is as follows:
    The return format is as follows:
    {{
        "function": "$GENERATED_FUNCSION"
    }}
    Make sure the response can be parsed by Python json.loads
    """

logic_prompt = """
    Your task is to first extract the programming logic that already exist in the mind map, and then generate new ones based on the theme of the mind map. If you think the logic does not exist, generate a new one.
    The generated logic should not duplicate the content of the mind map, and the description must be concise to meet the level of children.
    Following are some examples.
    Question: Generate a new logic of Keep the car moving.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position"], 
                    "Adjust the car's direction": ["when the car veers off track to the left", "when the car veers off track to the right"]
                }}
            }}
    }}
    Extracted logic: ["Initial position"]
    Generated logic: {{"logic": Control direction}}\n
    Question: Generate a new logic of Adjust the car's direction.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position", "Control direction"], 
                    "Adjust the car's direction": []
                }}
            }}
    }}
    Extracted logic: []
    Generated logic: {{"logic": "when the car veers off track to the left"}}\n
    Question: Generate a new logic of Touching the track causes the track to change color.
    Mind map: {{
        "racing game": {{
            "car": {{
                "function": {{
                    "Keep the car moving": ["Initial position", "Control direction"]
                }}
            }},
            "track": {{
                    "function": {{
                        "Touching the track causes the track to change color": []
                        }}
                }}
    }}
    Extracted logic: []
    Generated logic: {{ "logic": "When the car touches the track color, wait 0.2s and change the car color" }}\n
    Question: {question}
    Mind map: {memory}
    No need to write down the reasoning process, just tell me the final result. The return format is as follows:
    {{
        "logic": "$GENERATED_LOGIC"
    }}
    Make sure the response can be parsed by Python json.loads
"""