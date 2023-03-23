from flask import Flask, request, jsonify, render_template, flash
import openai
import time
import os
from html import escape


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
results_dir = os.path.abspath(f'{BASE_DIR}/results/')

SECRET_KEY = "Kiig3kv-3sd+gFd6?21c£36g65kzxvDsbinjm*vd"

# You need your own api Key here, you can get one from:
# https://platform.openai.com/account/api-keys
CHATGPT_API_KEY = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class ChatGPT:
    # stores history of chat only for open session.
    current_chat = []

    def ask_question(question, api_KEY=CHATGPT_API_KEY):
        openai.api_key = api_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            temperature=0.7,
            max_tokens=3900
        )
        answer = response.choices[0].text
        ChatGPT.current_chat.append({'question': f'{question.strip()}','answer': f'{answer.strip()}'})
        return answer
    
    def chat_history():
        return ChatGPT.current_chat


@app.route('/')
def chatgpt():
    # Main ChatGPT page
    return render_template('chatgpt.html')


@app.route('/get-answer', methods=['POST'])
def chat_now():
    if request.method == 'POST':
        try:
            # get question text from Form
            question = request.form['question']
            answer = ChatGPT.ask_question(question).strip()
            # get previous chat for this session
            history_chat = ChatGPT.chat_history()
            timestr = time.strftime("%d-%m-%Y")
            fpath = os.path.join(results_dir, f'{timestr}.txt') 
            # Saves the history also in file for today's day           
            with open(fpath,"a") as f:
                f.write(f'Question: {question}\nAnswer: {answer}')

            return jsonify({'answer': answer, 'history_chat': history_chat})
        except Exception as err:
            flash(f'Error: {err}')
            return jsonify({'err': f'Error: {err}'})
    
    
if __name__ == '__main__':
    app.run()#debug=True)