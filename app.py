from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import url_for
from flask import request, session
from chat_bot_0 import *
import textile
from text_modification import *

main_html = '/chatbot_v0_7.html'

app = Flask(__name__)
app.secret_key = 'TyBrce_secret_key_session'

print(__name__)
@app.route(main_html, methods=['GET','POST'])
def main_page_handle():
    model_id = "../../llama3_2_1B-unsloth-checkpoints"

    input = None
    answer = None
    if request.method == 'POST':
        print(request.form)
        print(session)
        if ('ClearChat' in str(request.form)):
            session['pre_chat'] = ''
            session['chat_memo'] = ''
            return render_template(main_html)
 
        if 'chat_memo' in str(session.keys()):
            session_chat = session['chat_memo']
        else:
            session_chat = None
        
        tokenizer, model = model_loading(model_id)
        answer = chat_bot(tokenizer, model, request.form['question'], request.form['bot_role'], session_chat = session_chat)
        
        input = 'Your Input:\n[Bot\'s role]: {}\n[Your question]: {}\n'.format(escape(request.form['bot_role']), escape(request.form['question']))
        
        chat = input+answer
        if 'chat_memo' in str(session.keys()):
            session['chat_memo'] = session['chat_memo'] + chat
        else:
            session['chat_memo'] = chat

        if 'pre_chat' in str(session.keys()):
            chat = chat + session['pre_chat']
        session['pre_chat'] = chat

        replace_text = textile.textile(chat)
        update_html = text_modification(render_template(main_html, answer = True), file_type='text')
        return update_html.replace_content(new_element=replace_text, replaced_element='replaced_part_')
    else:
        if 'pre_chat' in session.keys():
            update_html = text_modification(render_template(main_html, answer = 1), file_type='text')
            return update_html.replace_content(new_element = textile.textile(session['pre_chat']), replaced_element = 'replaced_part_')
        else: 
            return render_template(main_html)

@app.route('/session_out')
def session_out():
    session.pop('pre_chat', None)
    session.pop('chat_memo', None)
    return 'You have cleared the session!'

@app.route('/')
def home_page():
    return render_template('index.html')
