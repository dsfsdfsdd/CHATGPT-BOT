import openai
import os

openai.api_key = os.getenv("OPENAI_API")
model_engine = "text-davinci-003"
max_tokens = 256

def chatgpt_result(prompt):
    completion = openai.ChatCompletion.create(
        engine=model_engine,
        prompt=prompt
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion.choices[0].message.content
