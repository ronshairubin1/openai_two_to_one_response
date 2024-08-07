from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import datetime
import threading
import webbrowser
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Set up OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File path for logging decisions and errors
log_file_path = "/Users/ronshairubin/ML_API/Python_Code/ML/my_first_flask_project/Decision.txt"

def log_to_file(message, mode='a'):
    with open(log_file_path, mode) as file:
        file.write(message + "\n")

def initialize_log_file():
    log_to_file("New session started at {}\n\n".format(datetime.datetime.now()), 'w')

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        conversation_history = data.get('conversation_history', [])
        input_text = data.get('input', '')

        response1 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *conversation_history,
                {"role": "user", "content": input_text}
            ]
        )

        response2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *conversation_history,
                {"role": "user", "content": input_text}
            ]
        )

        response1_content = response1.choices[0].message.content
        response2_content = response2.choices[0].message.content

        evaluation_prompt = f"Human: {input_text}\n\nAI1: {response1_content}\n\nAI2: {response2_content}\n\n(1) which is more truthful? Weight = 0.5\n(2) which is more interesting and provides more content? Weight = 0.3\n(3) which is better written? Weight = 0.1\n(4) which is more concise? Weight = 0.1\n\nEvaluate and choose the better response between AI1 and AI2."
        evaluation_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )

        evaluation_content = evaluation_response.choices[0].message.content

        better_response = response1_content if "AI1" in evaluation_content else response2_content

        log_to_file(f"Human: {input_text}\nAI1: {response1_content}\nAI2: {response2_content}\nEvaluation: {evaluation_content}\nBetter Response: {better_response}\n")

        return jsonify({
            "response1": response1_content,
            "response2": response2_content,
            "evaluation": evaluation_content,
            "better_response": better_response
        })
    except Exception as e:
        error_message = f"Error: {str(e)}"
        log_to_file(error_message)
        return jsonify({"error": error_message}), 500

def open_browser():
    webbrowser.open_new_tab("http://127.0.0.1:5000")

if __name__ == '__main__':
    initialize_log_file()
    threading.Timer(1, open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)