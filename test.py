from openai import OpenAI
import os

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    # Make a request to the chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    # Accessing the message content correctly
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {str(e)}")