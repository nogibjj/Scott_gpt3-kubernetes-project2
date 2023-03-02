# from fastapi import FastAPI
# from pydantic import BaseModel
# import openai
# import os
# import uvicorn


# app = FastAPI()

# # Configure the OpenAI API key
# openai.api_key = os.environ['OPENAI_API_KEY']

# # Define the request model
# class Question(BaseModel):
#     question: str

# # Define the API endpoint
# @app.post('/api/ask')
# def ask(question: Question):
#     # Call the OpenAI API to generate an answer
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=question.question,
#         temperature=0.5,
#         max_tokens=100,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     # Return the answer as JSON
#     answer = response.choices[0].text.strip()
#     return {'answer': answer}

# # Define the root endpoint
# @app.get('/')
# def root():
#     return {'message': 'Hello, world!'}


# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8080)


from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import uvicorn
from typing import Optional

app = FastAPI()

# Configure the OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the request model
class Question(BaseModel):
    question: str
    prompt: Optional[str] = None

# Define the API endpoint
@app.post('/api/ask')
def ask(question: Question):
    # Create the GPT-3 prompt
    prompt = f"{question.prompt}\n{question.question}" if question.prompt else question.question

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response from the API response
    response_text = response.choices[0].text.strip()

    # Return the response as JSON
    return {'response': response_text}

# Define the root endpoint
@app.get('/')
def root():
    return {
        'message': 'Welcome to the GPT-3 Question Answering API!',
        'instructions': 'To use this API, send a POST request to /api/ask with the following fields in the request body: question (string) and prompt (optional string). The API will return a JSON object with the generated response.'
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
