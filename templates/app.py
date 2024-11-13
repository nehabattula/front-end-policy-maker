from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

AZURE_FUNCTION_URL = "https://<YOUR_AZURE_FUNCTION_URL>"  # Replace with your Azure Function URL

def call_azure_function(prompt, use_case):
    payload = {
        'prompt': prompt,
        'use_case': use_case  # Pass the use case (e.g., policy or faq)
    }
    response = requests.post(AZURE_FUNCTION_URL, json=payload)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error calling Azure Function: {response.status_code}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt')  # Expecting JSON data
    use_case = request.json.get('use_case')  # Get use case from the request
    response = call_azure_function(prompt, use_case)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)