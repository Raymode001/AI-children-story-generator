from openai import OpenAI
import os

def call_model(prompt: str, max_tokens=3000, temperature=0.1) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # please use your own openai api key here.
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content # type: ignore
