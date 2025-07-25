import os
import logging
from flask import Flask, render_template, jsonify, request, session
import requests
import json
import random

# Set up logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ollama API endpoint
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "llama2",
    "stream": False,
    "options": {
        "temperature": 0.7,
        "top_p": 1.0,
    }
}

@app.route('/')
def index():
    logging.info('Main page accessed')
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    logging.info('Quiz page accessed')
    return render_template('quiz.html')

@app.route('/get-question')
def get_question():
    try:
        logging.info('Generating a new question using Ollama')
        
        question_themes = [
            "the global rail industry",
            "the Australian rail industry, including specific lines or projects",
            "Siemens Mobility's innovations in rail technology",
            "an engaging fact about high-speed trains",
            "a historical fact about Australian railways"
        ]
        selected_theme = random.choice(question_themes)

        prompt = (
            f"Generate a multiple-choice question about {selected_theme}. "
            "The question should be engaging for a high school student. "
            "Format the output as a single, valid JSON object with 'question', 'options' (a list of 4), and 'answer' keys. "
            "Example: "
            '{"question": "What is the standard gauge of a railway track?", "options": ["1435 mm", "1520 mm", "1600 mm", "1067 mm"], "answer": "1435 mm"}'
        )

        response = requests.post(
            OLLAMA_ENDPOINT,
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()

        # The response from Ollama might be a stream of JSON objects, 
        # so we need to parse it carefully.
        full_response = response.text
        # Find the last JSON object in the stream
        last_json_str = full_response.strip().split('\n')[-1]
        response_data = json.loads(last_json_str)
        
        # The actual content is in the 'response' key
        question_data_text = response_data.get('response', '{}')
        question_data = parse_question_data(question_data_text)

        if not all(k in question_data for k in ['question', 'options', 'answer']):
            raise ValueError("Invalid format from Ollama API")

        # Store correct answer in session
        session['correct_answer'] = question_data['answer']

        # Remove answer from data sent to client
        del question_data['answer']

        logging.info(f"Generated question: {question_data['question']}")
        return jsonify(question_data)
    except requests.exceptions.ConnectionError:
        logging.error("Could not connect to Ollama. Make sure Ollama is running.")
        return jsonify({"error": "Could not connect to the local model. Please ensure Ollama is running."}), 500
    except Exception as e:
        logging.error(f"Error generating question with Ollama: {e}")
        return jsonify({"error": "Could not generate a question at this time."}), 500

@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    selected_option = data.get('selected_option')
    correct_answer = session.get('correct_answer')

    if not correct_answer:
        logging.error("Correct answer not found in session.")
        return jsonify({"error": "Could not verify the answer. Please restart the quiz."}), 400

    is_correct = selected_option == correct_answer
    logging.info(f"Selected: '{selected_option}', Correct: '{correct_answer}', Result: {is_correct}")

    return jsonify({"correct": is_correct, "correct_answer": correct_answer})

@app.route('/score')
def score():
    user_score = request.args.get('score', 0, type=int)
    total_questions = request.args.get('total', 5, type=int) # Default to 5
    return render_template('score.html', score=user_score, total=total_questions)

def parse_question_data(text):
    try:
        # The response might be wrapped in ```json ... ``` or have other text.
        json_str = text[text.find('{'):text.rfind('}')+1]
        return json.loads(json_str)
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from response: {text}")
        # This is a simple fallback, more robust parsing might be needed
        return {}

if __name__ == '__main__':
    app.run(debug=True) 