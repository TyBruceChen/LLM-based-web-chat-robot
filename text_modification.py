import torch

class text_modification():
    def __init__(self,replace_text = 'templates/index.html', file_type = 'read'):
        if file_type == 'read':
            with open (replace_text,'r') as f:
                self.content = f.read()
        elif file_type == 'text':
            self.content = replace_text;
        else:
            print('Error! please input valid file type!')
            
    def replace_content(self,new_element,replaced_element = 'Test Page'):
        self.content = self.content.replace(replaced_element, new_element)
        #self.replaced_element = new_element
        return self.content
    
def lung_type(cls_num,ls = ['COVID-19','Lung-Opacity','Normal','Pneumonia']):
    return ls[cls_num]

def continuous_token_sequence(tokens, session_chat, tokenizer, device, max_length=8, sw=4):
    if session_chat == None:
        print('No previous session')
        return tokens, 0
   
    session_chat = tokenizer(session_chat,
       return_tensors = 'pt')['input_ids'].to(device)
    prompt = "The above are questions I asked to you (with timeline order from end to start). Now this is my question:"
    prompt_ids = tokenizer(prompt, 
            return_tensors = 'pt')['input_ids'].to(device)
    prompt_length = len(prompt_ids[0])
    #print(session_chat.size())
    #print(tokens.size())
    if len(session_chat[0]) <= (max_length - sw):
        print('session_chat dirctly appended')
        inputs = torch.cat((session_chat,prompt_ids, tokens), 1)
        #print(f'LLM Inputs: {tokenizer.batch_decode(inputs[0])}') 
        return inputs, int(len(session_chat[0])) 
    else:
        print('session_chat cropped and appended')
        inputs = torch.cat((session_chat[0][-(max_length - int(sw)):].unsqueeze(dim = 0),tokens), 1)
        #print(f'LLM Inputs: {tokenizer.batch_decode(inputs[0])}')
        #print(f'Sliding window: {max_length - sw}')
        return inputs, int(max_length - sw)
