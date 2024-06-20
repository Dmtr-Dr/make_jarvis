from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm_key = os.getenv('LLM_KEY')

client = OpenAI(base_url="https://api.tensorai.ru/v1/openai", api_key=llm_key)  

def answer_from_llm(user_message, st_memory = None, lt_memory = None):

    messages = [
            {"role": "system", "content": "Твое имя милый, ты рад помочь мне и просто поболтать обо всём, ты обращаешься ко мне в мужском лице, твои реплики короткие, но с юмором."}
        ]
    if lt_memory:
        for m in lt_memory:
            messages.append(
                {"role": "system", "content": "факты о предыдущем разговоре:" + m['content']}
            )
    if st_memory:
        for role, message in st_memory:
            messages.append(
                {"role":role,"content": message}
            )
    messages.append(
        {"role":"user","content": user_message}
    )
        
    response = client.chat.completions.create(model="mixtral_8x22b", messages=messages)
    text = response.choices[0].message.content
    return text

def get_random_ice_break(st_memory = None, lt_memory = None):
    
    messages = [
            {"role": "system", "content": "Твое имя Милый, ты рад помочь мне и просто поболтать обо всём, ты обращаешься ко мне в мужском лице, твои реплики короткие, но с юмором."}
        ]
    if lt_memory:
        for m in lt_memory:
            messages.append(
                {"role": "system", "content": "факты о предыдущем разговоре:" + m['content']}
            )
    if st_memory:
        for role, message in st_memory:
            messages.append(
                {"role":role,"content": message}
            )
    messages.append(
        {"role":"user","content": "Скажи что-нибудь, чтобы прервать затянувшееся молчание"}
    )

    response = client.chat.completions.create(model="mixtral_8x22b", messages=messages)
    text = response.choices[0].message.content
    return text
