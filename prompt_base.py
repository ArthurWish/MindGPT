subject_extracted_prompt = """
    The content summarized in one topic sentence must be concise and in line with the cognitive level of children.
    User_input: {input}
    The return format is JSON format:
    {{
        "subject": "$Extracted_Subject"
    }}
"""

object_generation_prompt = """
    Your task is to first extract the programming objects that already exist in the mind map, and then generate three new objects based on the theme of the mind map. If you think the object does not exist, generate three new objects.
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
        "object1": "$Generated_Object",
        "object2": "$Generated_Object",
        "object3": "$Generated_Object"
    }}
"""

logic_extracted_prompt = """
    The code logic extracted below must be concise and in line with children's cognitive level.
    User input: {input}
    No need to write down the reasoning process. The return format is JSON format:
    {{
        "extracted_logic": "$Extracted_Logic"
    }}
"""
logic_queries_prompt = """
    Please generate three questions to ask about the following content that requires Scratch programming to improve the quality of Scratch code.
    User_input: {input}
    No need to write down the reasoning process. The return format is JSON format:
    {{
        "question1": "$Logic_question",
        "question2": "$Logic_question,
        "question3": "$Logic_question"
    }}
"""
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
    You are an expert on prompting engineering. I will give you some examples.
    
    Example: An audience cheering and clapping.
    Example: Rolling thunder with lightning strikes.
    Example: Car engine sound.
    
    Translate detected Chinese into English and no need to write down the reasoning process, just tell me the final prompt. 
    
    My text input is {sound}. The return format is JSON format:
    {{
        "prompt": "$YOUR_PROMPT"
    }}
"""
drawing_prompt_new = """
    You are an expert on prompting engineering for text to image generation. I will give you some examples, write the prompt. 
    
    Example: Cute small dog, full character, design by mark ryden and pixar and hayao miyazaki, 2D, animation, cartoon, high quality, 4k. Respond the prompt only, in English.
    Example: best high quality landscape. Ethereal gardens of marble built in a shining teal river in future city. By Dorian Cleavenger. Long shot, studio lighting, octane render.
    
    The prompt should adhere to and include all of the following rules:
    
    - Translate detected Chinese into English and no need to write down the reasoning process, just tell me the final prompt. 
    - If the text input is about characters, provide a white background and don't have complex backgrounds. If the text input is about landscape, don't show any characters, just objects related to the landscape.
    
    My text input is {drawing}. The return format is JSON format:
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

code_prompt = """
    Select blocks from the Scratch blocks below to program. Try to use the control, event, sensing and variable blocks. Please ensure that the generated blocks can be spliced correctly.
    Here is an example:
    {{
        "code": [{{'block_type': 'event_whenflagclicked', 'arguments': {{}}}}, {{'block_type': 'control_forever', 'arguments': {{}}}}, {{'block_type': 'control_if', 'arguments': {{'condition': {{'block_type': 'sensing_touchingobject', 'arguments': {{'object': '障碍物'}}}}, {{'block_type': 'looks_seteffectto', 'arguments': {{'effect': 'color', 'value': 100}}, {{'block_type': 'operator_subtract', 'arguments': {{'NUM1': {{'block_type': 'sensing_of', 'arguments': {{'property': 'score', 'object': 'Stage'}}, 'NUM2': 1}}]
    }}
    
    User input: {user_input}
    No need to write down the reasoning process, just tell me the final result. The return format is JSON format:
        {{
            "code": "$block_type"
        }}
    
    Scratch blocks: 
        askandwait
        backdropnumbername
        control_create_clone_of
        control_delete_this_clone
        control_forever
        control_if
        control_if_else
        control_repeat
        control_start_as_clone
        control_stop
        control_wait
        costumenumbername
        current
        direction
        event_broadcast
        event_broadcastandwait
        event_whenbackdropswitchesto
        event_whenbroadcastreceived
        event_whenflagclicked
        event_whengreaterthan
        event_whenkeypressed
        event_whenthisspriteclicked
        looks_changeeffectby
        looks_changesizeby
        looks_cleargraphiceffects
        looks_goforwardbackwardlayers
        looks_gotofrontback
        looks_hide
        looks_nextbackdrop
        looks_nextcostume
        looks_say
        looks_sayforsecs
        looks_seteffectto
        looks_setsizeto
        looks_show
        looks_switchbackdropto
        looks_switchcostumeto
        looks_think
        looks_thinkforsecs
        loudness
        motion_changexby
        motion_changeyby
        motion_glidesecstoxy
        motion_glideto
        motion_goto
        motion_gotoxy
        motion_ifonedgebounce
        motion_movesteps
        motion_pointindirection
        motion_pointtowards
        motion_setrotationstyle
        motion_setx
        motion_sety
        motion_turnleft
        motion_turnright
        of
        operator_add
        operator_and
        operator_contains
        operator_divide
        operator_equals
        operator_gt
        operator_join
        operator_length_of
        operator_letter_of
        operator_lt
        operator_mathop
        operator_mod
        operator_multiply
        operator_not
        operator_or
        operator_random
        operator_round
        operator_subtract
        repeat_until
        sensing_colortouchingcolor
        sensing_daysince2000
        sensing_distanceto
        sensing_keypressed
        sensing_mousedown
        sensing_mousex
        sensing_mousey
        sensing_resettimer
        sensing_setdragmode
        sensing_touchingcolor
        sensing_touchingobject
        size
        sound_changeeffectby
        sound_changevolumeby
        sound_clearsoundeffects
        sound_play
        sound_playuntildone
        sound_seteffectto
        sound_setvolumeto
        sound_stopallsounds
        timer
        username
        wait_until
        x_position
        y_position
        my variable
        data_setvariableto
        data_changevariableby
        data_showvariable
        data_hidevariable
"""
