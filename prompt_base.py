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
    No need to write down the reasoning process, just tell me the generated object. The return format is JSON format:
    {{
        "object": "$Generated_Object"
    }}
"""
sound_prompt = """
    You are an expert on prompting engineering. I will give you some examples, fill the prompt with knowledge for <{sound}>. 
    
    Example: An audience cheering and clapping.
    Example: Rolling thunder with lightning strikes.
    Example: Car engine sound.
    
    The return format is JSON format:
    {{
        "prompt": "$YOUR_PROMPT"
    }}
"""
drawing_prompt_new = """
    You are an expert on prompting engineering for text to image generation. I will give you some examples, fill the prompt with knowledge for <{drawing}>. 
    template "[character or landscape], [artist], [style]",
    Example: Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k. Respond the prompt only, in English.
    Example" best high quality landscape. Ethereal gardens of marble built in a shining teal river in future city. By Dorian Cleavenger. Long shot, studio lighting, octane render.
    
    The return format is JSON format:
    {{
        "prompt": "$YOUR_PROMPT"
    }}
"""
drawing_prompt = """
    Stable Diffusion is an AI art generation model similar to DALLE-2.
    Here are some prompts for generating art with Stable Diffusion. 

    Example:
    - Create an image of a colorful, enchanting fantasy castle surrounded by a magical forest. The castle should have tall, whimsical spires and be adorned with sparkling gems. The forest is filled with friendly animals, like talking rabbits and dancing birds, and the trees have leaves in various bright colors. There are also mystical flowers glowing softly, and a clear blue sky with a rainbow in the background.
    - Illustrate a vibrant scene of children having a space adventure in a cartoon-style spaceship. The spaceship is bright and friendly-looking, with large windows and fun, whimsical shapes. Inside, children of various descents are wearing colorful space suits and helmets, looking out at a starry galaxy with planets and comets. Include a friendly alien waving at them from a nearby planet.
    - Depict an underwater exploration scene with children in a submarine. The submarine is shaped like a large, friendly fish and is exploring a beautiful coral reef. Around the submarine are various sea creatures like smiling dolphins, colorful fish, and a gentle turtle. The water is a clear, shimmering blue, and sunbeams are filtering through from the surface.
    
    The prompt should adhere to and include all of the following rules:

    - Prompt should always be written in English, regardless of the input language. Please provide the prompts in English.
    - Each prompt should consist of a description of the scene followed by modifiers divided by commas.
    - When generating descriptions, focus on portraying the visual elements rather than delving into abstract psychological and emotional aspects. Provide clear and concise details that vividly depict the scene and its composition, capturing the tangible elements that make up the setting.
    - The modifiers should alter the mood, style, lighting, and other aspects of the scene.
    - Multiple modifiers can be used to provide more specific details.
    
    I want you to write me one single prompt exactly about the IDEA follow the rules above:
    IDEA: {drawing}
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
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "function": "$GENERATED_FUNCTION"
    }}
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
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
    {{
        "logic": "$GENERATED_LOGIC"
    }}
"""
