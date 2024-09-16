import os
import instructor
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
from anthropic import Anthropic
from groq import Groq

# Setup various API clients
oai_instr_client = instructor.from_openai(OpenAI())
claude_client = instructor.from_anthropic(Anthropic())
groq_client = instructor.from_groq(Groq(), mode=instructor.Mode.TOOLS)
oai_client = OpenAI()

### DEFINE OUTPUT STRUCTURES ###

# Define the structure for book information (Instructor implementations including OpenAI, Claude, and Llama on Groq)
class BookInfo(BaseModel):
    title: str = Field(..., description="The title of the book")
    author: str = Field(..., description="The author of the book")
    genres: List[str] = Field(..., description="A list of genres the book belongs to")
    publication_year: int = Field(..., description="The year the book was published")
    summary: str = Field(..., description="A brief summary of the book's plot")
    #recommendations: str = Field(..., description="A list of recommended books based on the book's summary")
    #takeaways: str = Field(..., description="A list of takeaways from the book based on your knowledge")

# In book_analysis.py

def get_oai_instructor_book_info(user_book_summary):
    model = "gpt-4o-2024-08-06"
    result = oai_instr_client.chat.completions.create(
        model=model,
        response_model=BookInfo,
        messages=[{"role": "user", "content": user_book_summary}],
    )
    return result, model

def get_claude_instructor_book_info(user_book_summary):
    model = "claude-3-5-sonnet-20240620"
    result = claude_client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": user_book_summary,}],
        response_model=BookInfo,
    )
    return result, model

def get_llama_instructor_book_info(user_book_summary):
    model = "llama-3.1-70b-versatile"
    result = groq_client.chat.completions.create(
        model=model,
        response_model=BookInfo,
        messages=[{"role": "user", "content": user_book_summary}],
    )
    return result, model

def get_oai_structured_outputs_book_info(user_book_summary):
    model = "gpt-4o-2024-08-06"
    result = oai_client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts book information."},
            {"role": "user", "content": user_book_summary}
        ],
        response_format=BookInfo
    )
    result = result.choices[0].message.parsed
    return result, model
