from flask import Flask, render_template, request, jsonify, session
import ollama
import uuid

app = Flask(__name__, template_folder='template', static_folder='static')

app.secret_key = uuid.uuid4().hex

@app.route("/")
def index():
    session['chat_history'] = []
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["msg"]

    chat_history = session.get('chat_history', [])

    chat_history.append({'role': 'user', 'content': user_msg})

    response = get_chat_response(chat_history)

    chat_history.append({'role': 'assistant', 'content': response})

    session['chat_history'] = chat_history

    return jsonify({"response": response})

def get_chat_response(chat_history):
    try:
        messages = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]

        response = ollama.chat(
            model='llama3.2',
            messages=messages
        )
        return response["message"]["content"]
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
