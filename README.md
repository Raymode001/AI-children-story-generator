# AI Children Story Generator

An interactive AI-powered story generator for children ages 5-10. The system uses a multi-agent design where a storyteller generates the initial story, an LLM judge evaluates its quality, and a refiner iteratively improves it based on the judge's feedback. The user can also provide their own feedback to modify the story after it is generated.

## System Components

| File | Role |
|---|---|
| `main.py` | Orchestrates the full pipeline — user input, storyteller, judge loop, user feedback loop |
| `judge.py` | LLM judge — scores the story on 5 criteria and returns structured feedback |
| `agent.py` | Shared interface to `gpt-3.5-turbo` via the OpenAI API |
| `diagram.md` | Block diagram of the full system flow |

## How to Run

**1. Set your OpenAI API key in the terminal:**
```
$env:OPENAI_API_KEY="sk-your-key-here"
```

**2. Run the program:**
```
python main.py
```

**3. Follow the prompts:**
- Enter your story request
- Select a category (Fan Fiction, Sci-Fi, Cartoon, Classic Fairy Tale, Classic Literature)
- Enter a context or press Enter to use the provided example
- Select a point of view and optionally name the storyteller character
- The system will generate, judge, and refine the story automatically
- After the final story is printed, provide feedback or type `yes` to exit

## Design Decisions

- **Score-based judge** — the judge scores the story on 5 criteria (safety, vocabulary, structure, sensory, ending). A perfect score of 5 exits the loop early; otherwise the story is refined up to 5 times.
- **Structured JSON output from judge** — the judge returns `criteria_scores`, `feedback`, and `instructions` as JSON, allowing the refiner to act on specific, targeted guidance rather than vague critique.
- **Category and context selector** — users can pick from 5 story universes and customize the context, enabling tailored generation strategies per category.
- **User feedback loop** — after the judge loop completes, the user can request further changes interactively until satisfied.

---

# Hippocratic AI Coding Assignment
Welcome to the [Hippocratic AI](https://www.hippocraticai.com) coding assignment

## Instructions
The attached code is a simple python script skeleton. Your goal is to take any simple bedtime story request and use prompting to tell a story appropriate for ages 5 to 10.
- Incorporate a LLM judge to improve the quality of the story
- Provide a block diagram of the system you create that illustrates the flow of the prompts and the interaction between judge, storyteller, user, and any other components you add
- Do not change the openAI model that is being used. 
- Please use your own openAI key, but do not include it in your final submission.
- Otherwise, you may change any code you like or add any files

---

## Rules
- This assignment is open-ended
- You may use any resources you like with the following restrictions
   - They must be resources that would be available to you if you worked here (so no other humans, no closed AIs, no unlicensed code, etc.)
   - Allowed resources include but not limited to Stack overflow, random blogs, chatGPT et al
   - You have to be able to explain how the code works, even if chatGPT wrote it
- DO NOT PUSH THE API KEY TO GITHUB. OpenAI will automatically delete it

---

## What does "tell a story" mean?
It should be appropriate for ages 5-10. Other than that it's up to you. Here are some ideas to help get the brain-juices flowing!
- Use story arcs to tell better stories
- Allow the user to provide feedback or request changes
- Categorize the request and use a tailored generation strategy for each category

---

## How will I be evaluated
Good question. We want to know the following:
- The efficacy of the system you design to create a good story
- Are you comfortable using and writing a python script
- What kinds of prompting strategies and agent design strategies do you use
- Are the stories your tool creates good?
- Can you understand and deconstruct a problem
- Can you operate in an open-ended environment
- Can you surprise us

---

## Other FAQs
- How long should I spend on this? 
No more than 2-3 hours
- Can I change what the input is? 
Sure
- How long should the story be?
You decide