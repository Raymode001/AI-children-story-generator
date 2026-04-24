import os
import openai
import json
from agent import call_model

judge_prompt = """
You are a teacher of children of ages 5 to 10. You are given a story_output and you need to judge the story appropriate for children of ages 5 to 10, according to the following criteria.
For each, respond with exactly 1 (Pass) or 0 (Fail).

    Safety: No graphic violence, gore or genuinely traumatic themes for kids of age 5-10. Mystery, imagination, mild suspense, and fantasy creatures are allowed and encouraged.

    Vocabulary: No complex academic or adult language. Vocabulary used should be understandable for a US 4th grade student. 

    Structure: Has a clear story arch, for example: Exposition - Rising Action - Climax - Falling Action - Resolution. It needs to have at least one
  challenge or exciting moment for the character to overcome.

    Sensory: Uses at least two descriptions of sounds, smells, or colors.

    Ending: The story ends on a happy or optimistic note.

You MUST provide your judgment as a JSON object with the following fields, the following judgement only as an example: 

Judgment: {{
"criteria_scores": {{"safety": 1, "vocab": 1, "structure": 0, "sensory": 1, "ending": 1}},
"feedback": "The story is safe and sweet, but it lacks a middle conflict (structure=0).",
"instructions": "Add a small challenge the character faces before the happy ending."
}}

The story_output is:
story_output: {story_output}

Judgment:
"""

def judge_score(story: str) -> dict:
    response = call_model(judge_prompt.format(story_output=story))
    try: 
        return json.loads(response)
    except json.JSONDecodeError:
        return {"feedback": response, "instructions": "Please improve the story."}
    
