# System Block Diagram

## Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                            USER                                 │
│  - Story request                                                │
│  - Category selection (Fan Fiction, Sci-Fi, Cartoon, etc.)      │
│  - Context input                                                │
│  - Point of view selection                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │  story_request, category, context, pov
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       STORYTELLER                               │
│  teller_prompt → call_model (gpt-3.5-turbo)                     │
│  Generates an age-appropriate story (ages 5-10)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │  initial story
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     JUDGE LOOP (max 5 attempts)                 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                        JUDGE                            │   │
│   │  judge_prompt → call_model (gpt-3.5-turbo)              │   │
│   │  Evaluates story on 5 criteria:                         │   │
│   │    - Safety                                             │   │
│   │    - Vocabulary                                         │   │
│   │    - Structure                                          │   │
│   │    - Sensory                                            │   │
│   │    - Ending                                             │   │
│   │  Returns: criteria_scores, feedback, instructions       │   │
│   └──────────────┬──────────────────────────────────────────┘   │
│                  │                                              │
│          score = sum(criteria_scores)                           │
│                  │                                              │
│         ┌────────┴────────┐                                     │
│         │                 │                                     │
│      score==5          score < 5                                │
│         │                 │                                     │
│         │                 ▼                                     │
│         │    ┌────────────────────────┐                         │
│         │    │        REFINER         │                         │
│         │    │  refine_prompt +       │                         │
│         │    │  feedback +            │                         │
│         │    │  instructions →        │                         │
│         │    │  call_model            │                         │
│         │    │  (gpt-3.5-turbo)       │                         │
│         │    └────────────┬───────────┘                         │
│         │                 │  refined story                      │
│         │                 └──────────────► (loop back to JUDGE) │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │  final story
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT TO USER                             │
│  Prints the final story                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   USER FEEDBACK LOOP                            │
│                                                                 │
│   User: "Are you happy with the story? (yes/no)"                │
│         │                                                       │
│      ┌──┴──┐                                                    │
│     yes    no                                                   │
│      │      │                                                   │
│     END     │  User provides changes                            │
│             ▼                                                   │
│   ┌─────────────────────────┐                                   │
│   │   feedback_prompt +     │                                   │
│   │   user changes →        │                                   │
│   │   call_model            │                                   │
│   │   (gpt-3.5-turbo)       │                                   │
│   └──────────┬──────────────┘                                   │
│              │  updated story                                   │
│              └──────────────► (loop back to user)               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Summary

| Component | File | Role |
|---|---|---|
| Storyteller | `main.py` (teller_prompt) | Generates initial story from user request |
| Judge | `judge.py` (judge_prompt) | Evaluates story quality on 5 criteria |
| Refiner | `main.py` (refine_prompt) | Improves story using judge feedback |
| User Feedback | `main.py` (feedback_prompt) | Improves story using user change requests |
| LLM API | `agent.py` (call_model) | Single shared interface to gpt-3.5-turbo |

