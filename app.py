from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import url_for
from flask import request, session
import textile, os, time
from chat_bot_0 import *
from text_modification import *
from whisper_transcriber import *
from file_name_counter import file_name_counter
from file_handler import convert_to_wav

from flask_session import Session #to extend the ssession capacity

main_html = '/chatbot_v1.html'
whisper_id = '../whisper-base-openai'
model_id = "../llama3_2_1B-unsloth"
cert_pub_key = 'https_cert_Aliyun_fullchain/fullchain.pem'
private_key = 'https_cert_Aliyun_fullchain/www.ty-bruce-server.site.key'
https_enable = True #by enable this, audio function can work for public access

tokenizer, model = model_loading(model_id)
whisper_processor, whisper_model = load_whisper_model(whisper_id)
file_name_counter = file_name_counter()

audio_file = 'file'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TyBrce_secret_key_session'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route(main_html, methods=['GET','POST'])
def main_page_handle():

    input = None
    answer = None
    if request.method == 'POST':
        #print(request.form)
        #print(session)
        start_time = time.time()
        if ('ClearChat' in str(request.form)):
            session.clear()
            session['pre_chat'] = ''
            session['chat_memo'] = ''
            return render_template(main_html)
 
        if 'chat_memo' in str(session.keys()):
            session_chat = session['chat_memo']
        else:
            session_chat = None

        if audio_file in request.files:
            #audio input detected
            file = request.files[audio_file]
            file_name = file_name_counter.get_current_index() + '.wav'
            file_name_counter.add_file_index()
            file_path = os.path.join('audios', file_name)
            file.save(file_path)
            file.close
            file_path = convert_to_wav(file_path)
            question = whisper_transcribe(file_path, whisper_processor, whisper_model)
            bot_role = 'Your are a omniscient secretory who always responds to questions from people all over the world.'
        else:
            question = request.form['question']
            bot_role = request.form['bot_role']

        answer = chat_bot(tokenizer, model, question, bot_role, session_chat = session_chat)
        
        input = 'Your Input:\n[Bot\'s role]: {}\n[Your question]: {}\n'.format(escape(bot_role), escape(question))
        
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
        print(f'Processing Time: {time.time() - start_time}')
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

if __name__ == '__main__':
    if https_enable:
        app.run(ssl_context=(cert_pub_key, private_key), host='0.0.0.0', port=5320)
    else:
        app.run(host='0.0.0.0', port = 5320)
