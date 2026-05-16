import json
import os

from anthropic import Anthropic
from groq import Groq
from dotenv import load_dotenv

from app.prompts.extraction_prompt import build_extraction_prompt

load_dotenv()

llm = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

fallback_llm = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_with_anthropic(prompt: str):
    
    response = llm.message.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.content[0].text

def extract_with_groq(prompt: str):
    
    response = fallback_llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def extract_structured_data(user_query: str):
    prompt = build_extraction_prompt(user_query)
    
    try:
        text_response = extract_with_anthropic(prompt)
        provider = "anthropic"
        
    except Exception as anthropic_error:
        print(f"Anthropic failed: {anthropic_error}")
        print("Falling back to Groq...")
        
        try:
            text_response = extract_with_groq(prompt)
            provider = "groq (fallback)"

        except Exception as groq_error:
            print(f"Groq failed: {groq_error}")
            raise Exception("Both Anthropic and Groq requests failed")
        
    extracted_data = json.loads(text_response)
    
    return {
        "provider": provider,
        "data": extracted_data
    }