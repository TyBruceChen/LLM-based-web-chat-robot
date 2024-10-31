import transformers
import torch
import time
from text_modification import continuous_token_sequence

def chat_template_generate(question, 
        chatbot_role = 'You are a friendly chatbot who always responds in the style of a research assistance is AI lab'):
    
    return f'<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{chatbot_role}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'

def text_generation(text):
    return f'<|begin_of_text|>{text}'

def model_loading(model_id):
    #load tokenizer and model
    dtype = torch.bfloat16  #parameter type for model loading

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('Loading model and tokenizer...')
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
    model = transformers.AutoModelForCausalLM.from_pretrained(model_id,
        torch_dtype= dtype).to(device)
    print('Model and tokenizer loaded')
    return tokenizer, model


def chat_bot(tokenizer, model, question, chatbot_role=None, session_chat = None, max_length = 8192):
    memory_ratio = 0.25 #left how much percent of tokens for current answering {(1-memory_ratio) = memory size ratio}
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    if chatbot_role == None:
        chat = chat_template_generate(question)
    else:
        chat = chat_template_generate(question, chatbot_role)

    #print(f'Input: {chat}\n')  

    time_start = time.time()
    input_ids = tokenizer(chat, 
                      return_tensors = 'pt')['input_ids'].to(device)
     
    input_ids, pre_chat_len = continuous_token_sequence(input_ids, session_chat, tokenizer, device,  max_length = max_length, sw = max_length*memory_ratio)

    print(f'Window Length:{pre_chat_len}')

    output_tensors = model.generate(input_ids,
                                do_sample = True,
                                temperature = 0.9,
                                max_length = max_length)

    print(f'Time used for token generation:{time.time()-time_start}')
    #print(output_tensors.size())
   
    output_tensors = output_tensors[0][pre_chat_len:].unsqueeze(dim=0)
    print(f'LLM Current Prediction: {tokenizer.batch_decode(output_tensors)[0]}')
    return tokenizer.batch_decode(output_tensors)[0].split('assistant<|end_header_id|>')[-1].replace('<|eot_id|>', '\n')
