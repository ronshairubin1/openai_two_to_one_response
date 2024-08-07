#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:41:22 2024

"""

from openai import OpenAI
from colorama import init, Fore, Style
import os
import json

# Initialize colorama
init(autoreset=True)

# Verify the environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to save conversation history to a JSON file
def save_conversation_history(conversation_history, file_path='data/conversation_history.json'):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Add print statement here
        print(f"Saving conversation history to {os.path.abspath(file_path)}")
        with open(file_path, 'w') as file:
            json.dump(conversation_history, file)
        print(f"Conversation history saved to {os.path.abspath(file_path)}")
    except Exception as e:
        print(f"Error saving conversation history: {e}")

# Function to load conversation history from a JSON file
def load_conversation_history(file_path='data/conversation_history.json'):
    try:
        # Print statement to show the absolute path from which the file is being loaded
        print(f"Loading conversation history from {os.path.abspath(file_path)}")
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Print statement to indicate the file was not found
        print(f"No existing conversation history found at {os.path.abspath(file_path)}")
        return []
    except Exception as e:
        print(f"Error loading conversation history: {e}")
        return []

# Function to communicate with OpenAI
def chat_with_openai(messages, temperature, top_p, max_tokens, frequency_penalty, presence_penalty):
    response = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response.choices[0].message.content

# Helper function to get user input with default values
def get_input(prompt, default):
    user_input = input(prompt)
    return float(user_input) if user_input else default

def main():
    print(Fore.GREEN + "Welcome to the OpenAI chat! Type 'exit' to quit." + Style.RESET_ALL)
    print()

    # Prompt the user to set the parameters with defaults
    temperature = get_input(Fore.CYAN + "Set the temperature (0.0 to 1.0) [default 0.7]: " + Style.RESET_ALL, 0.7)
    top_p = get_input(Fore.CYAN + "Set the top_p (0.0 to 1.0) [default 1.0]: " + Style.RESET_ALL, 1.0)
    max_tokens = int(get_input(Fore.CYAN + "Set the max_tokens (1 to 2048) [default 100]: " + Style.RESET_ALL, 100))
    frequency_penalty = get_input(Fore.CYAN + "Set the frequency_penalty (-2.0 to 2.0) [default 0.0]: " + Style.RESET_ALL, 0.0)
    presence_penalty = get_input(Fore.CYAN + "Set the presence_penalty (-2.0 to 2.0) [default 0.0]: " + Style.RESET_ALL, 0.0)
    print()

    while True:
        user_input = input(Fore.LIGHTBLUE_EX + "You: " + Style.RESET_ALL)
        if user_input.lower() == 'exit':
            break
        
        # Create messages with the new user input
        messages = [{"role": "user", "content": user_input}]
        
        # Run the prompt twice
        response1 = chat_with_openai(messages, temperature, top_p, max_tokens, frequency_penalty, presence_penalty)
        response2 = chat_with_openai(messages, temperature, top_p, max_tokens, frequency_penalty, presence_penalty)

        # Evaluate which response is better
        evaluation_prompt = (
            f"Here are two responses to the prompt:\n\n"
            f"Prompt: {user_input}\n\n"
            f"Response 1: {response1}\n\n"
            f"Response 2: {response2}\n\n"
            f"Determine which response is (a) more accurate and (b) better written. "
            f"List the reasons why."
        )
        evaluation_messages = [{"role": "user", "content": evaluation_prompt}]
        evaluation = chat_with_openai(evaluation_messages, temperature, top_p, max_tokens, frequency_penalty, presence_penalty)

        # Print both responses and the evaluation
        print("\nResponse 1:", response1)
        print("\nResponse 2:", response2)
        print("\nEvaluation:", evaluation)

        # Determine the better response
        if "Response 2" in evaluation:
            better_response = response2
        else:
            better_response = response1

        # Print the better response
        print("\nBetter Response:", better_response)

if __name__ == "__main__":
    main()