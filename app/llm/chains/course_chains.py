from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from app.llm.models import llama3_model
from app.llm.prompts.course_prompts import base_course_prompt, module_prompt

# FOR GENERATING THE BASE COURSE OUTLINE
_base_course_examples = [
    {
        "input": "Teach me about making games in C",
        "output": """{
  "title": "Game Development with C: From Basics to Advanced Techniques",
  "description": "Learn the fundamentals and best practices of creating engaging games using the C programming language. This comprehensive course covers game development basics, game loop, event handling, graphics, sound, AI, physics, and more.",
  "modules": [
    "Introduction to Game Development with C: Setting up a Development Environment",
    "Game Loop Fundamentals: Understanding the Main Loop, Input Handling, and Timing",
    "Event Handling in Games: Mouse, Keyboard, and Gamepad Inputs",
    "2D Graphics Programming with SDL and OpenGL: Drawing Shapes, Textures, and Sprites",
    "Sound Design for Games: Creating Audio Effects and Music with FMOD and OpenAL",
    "Game AI and Pathfinding: Implementing Simple AI Behaviors and Complex Routing Algorithms",
    "Physics Engines in Games: Using Bullet Physics and PhysX to Simulate Real-World Dynamics",
    "Advanced Game Development Topics: Networking, Multiplayer, and Optimization Techniques",
    "Project Development: Creating a Complete 2D Game with C, SDL, OpenGL, and FMOD"
  ]
}""",
    },
]

_example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

_base_course_few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=_example_prompt, examples=_base_course_examples
)

_base_course_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", base_course_prompt),
        _base_course_few_shot_template,
        ("human", "{input}"),
    ]
)


@lru_cache
def get_outline_course_chain():
    """Generate a JSON object with a new course outline.
    The JSON fields include title, description, and modules (list)

    Returns:
        RunnableSerializable: The chain
    """
    return _base_course_prompt | llama3_model


# FOR GENERATING A MODULE IN A COURSE
_module_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            module_prompt,
        ),
        (
            "human",
            "{input}",
        ),
    ]
)


@lru_cache
def get_module_creation_chain():
    """Creates a Markdown module that belongs to a course outline.

    Returns:
        RunnableSerializable: The chain
    """
    return _module_prompt_template | llama3_model
