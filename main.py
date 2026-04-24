import json
from judge import judge_score
from agent import call_model

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

"""



teller_prompt = """
You are a storyteller. You are given a story_request and you need to tell a story appropriate for ages 5 to 10.
Category: {category}
Context: {context}
Point of view: {pov}

story_request: {story_request}

Story:
"""

refine_prompt="""Here is a story: {curr_story}

A judge gave this feedback: {feedback}
Please improve the story by following these instructions: {instructions}
Write the improved story appropriate for ages 5-10."""

feedback_prompt="""
Here is a story: {curr_story}
User has provided feedback: {feedback}
Please improve the story by following the user feedback. 
Write the improved story appropriate for ages 5-10."""

CATEGORIES = {
    "1": {
        "name":"Fan Fiction",
        "example":"e.g. A story set in the Marvel universe where a child befriends Spider-Man"
    },
    "2": {
        "name":"Sci-Fi",
        "example":"e.g. A child astronaut discovers a planet of friendly talking robots"
    },
    "3": {
        "name":"Cartoon",
        "example":"e.g. Bluey and Bingo go on a backyard adventure and find a secret garden"
    },
    "4": {
        "name":"Classic Fairy Tale",
        "example":"e.g. A kind child helps a lost fairy find her way back to an enchanted kingdom"
    },
    "5": {
        "name":"Classic Literature",
        "example":"e.g. A new friend joins Alice and the Mad Hatter for a tea party in Wonderland"
    },
}

POVS = {
    "1": "First person (the main character tells the story using I/we)",
    "2": "Third person (narrator tells the story using he/she/they)",
    "3": "Second person (the reader is the main character, using you)",
}

def get_category():
    print("\nPick a story category:")
    for key, val in CATEGORIES.items():
        print(f" {key}. {val['name']}")
    choice= input("Choice (1-5): ").strip()
    if choice not in CATEGORIES:
        print("Invalid choice, defaulting to Classic Fairy Tale.")
        choice= "4"
    selected= CATEGORIES[choice]
    print(f"\nExample context for {selected['name']}: {selected['example']}")
    context=input("Enter your context (or press Enter to use default): ").strip()
    if not context:
        context=selected["example"].replace("e.g. ", "")
    return selected["name"], context

def get_pov():
    print("\nPick a point of view:")
    for key, val in POVS.items():
        print(f"  {key}. {val}")
    choice = input("Choice (1-3): ").strip()
    if choice not in POVS:
        print("Invalid choice, defaulting to Third person.")
        choice= "2"
    pov=POVS[choice]
    character=input("Who is the storyteller? (press Enter to leave unspecified): ").strip()
    if character:
        pov+= f", told from the perspective of {character}"
    return pov

def main():
    # Step 1: generate initial story
    user_input= input("What kind of story do you want to hear? ")
    category, context=get_category()
    pov=get_pov()
    story_prompt=teller_prompt.format(
        story_request=user_input,
        category=category,
        context=context,
        pov=pov
    )
    story = call_model(story_prompt)
    

    # Step 2: refine story until total score passes baseline
    max_attempts=5
    for attempt in range(max_attempts):
        try:
            judge_response=judge_score(story)
            print("judge says:", judge_response)
            score=sum(judge_response["criteria_scores"].values())
            if score==5:
                break
            story=call_model(refine_prompt.format(curr_story=story, feedback=judge_response['feedback'], instructions=judge_response['instructions']))
        except KeyError:
            break
    
    print(story)
    
    # Step 3: user feedback loop:
    while True:
        user_feedback=input("\nAre you happy with the story? (yes/no):")
        if user_feedback.lower()=='yes':
            break
        changes=input('What would you like to change?')
        story=call_model(feedback_prompt.format(curr_story=story, feedback=changes))
        print(story)

if __name__ == "__main__":
    main()