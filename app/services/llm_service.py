import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from app.prompts.extraction_prompt import build_extraction_prompt

load_dotenv()

llm = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def extract_structured_data(user_query: str):
    prompt = build_extraction_prompt(user_query)
    
    # response = llm.message.create(
    #     model="claude-3-haiku-20240307",
    #     max_tokens=300,
    #     temperature=0,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )
    
    # text_response = response.content[0].text
    
    text_response = {"text":"Smth smth"}
        
    return text_response