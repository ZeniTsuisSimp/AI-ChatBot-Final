from flask import Flask, render_template, request, jsonify, session
import ollama
import uuid

app = Flask(__name__, template_folder='template', static_folder='static')

# Generate a random secret key using uuid4
app.secret_key = uuid.uuid4().hex

@app.route("/")
def index():
    # Initialize chat history on the first load
    session['chat_history'] = []
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["msg"]

    # Retrieve chat history from session
    chat_history = session.get('chat_history', [])

    # Add the user message to the chat history
    chat_history.append({'role': 'user', 'content': user_msg})

    # Get the AI response
    response = get_chat_response(chat_history)

    # Append the chatbot's response to the chat history
    chat_history.append({'role': 'assistant', 'content': response})

    # Update session variables
    session['chat_history'] = chat_history

    return jsonify({"response": response})

def get_chat_response(chat_history):
    try:
        # Construct the messages for the model
        messages = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]

        # Pass the chat history to the model
        response = ollama.chat(
            model='llama3.2',
            messages=messages
        )
        return response["message"]["content"]
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
