from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Configure the OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the request model
class Question(BaseModel):
    question: str

# Define the API endpoint
@app.post('/api/ask')
def ask(question: Question):
    # Call the OpenAI API to generate an answer
    response = openai.Completion.create(
        engine="davinci",
        prompt=question.question,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the answer as JSON
    answer = response.choices[0].text.strip()
    return {'answer': answer}

# Define the root endpoint
@app.get('/')
def root():
    return {'message': 'Hello, world!'}
