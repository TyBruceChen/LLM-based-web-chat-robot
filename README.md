# LLM-based-web-chat-robot

## Introduction:
A server-side deployed agent that provides web chat robot service for users. The current utilized LLM model(s) is Llama3.2 ([Meta](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)). [Flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/) realizes web service. <br>
**New Feature Updates:** UI improved. \
![image](https://github.com/user-attachments/assets/af3484a5-6fb5-4ce0-8e65-50e7c469019a)

**Privious Features:** Combined with OpenAI's [Whisper](https://huggingface.co/openai/whisper-base) model, audio input is currently supported.
![Screenshot_15-10-2024_17428_47 109 36 149](https://github.com/user-attachments/assets/54c51889-a54c-419c-8b51-922fe00cae68)

## Basic Concepts:
* **Token**: Special numbers that represent human-language words (English, Chinese, Japanese, ...) or part of it. <br><br>
* **Token Length Capacity**: the maximum length of tokens that the model (LLM) can generate. Specified by ```model_id``` in ```app.py```. <br><br>
* **Memory**: To enable LLM to have continuous conversations with humans, previous conversations are concatenated with the current question to feed into LLM. This enables the LLM have 'memory' like human beings to perceive past information. <br><br>
* **Memory Length**: As you may notice, the memory length is limited by the ```token length```. Thanks to Meta, the Llama3.2-1B has powerful performance with the ability to generate a maximum of 128K tokens in one go (GPT-2 only has 1024 perceptive token spectrum). In this case, when the total number of tokens encoded from the previous conversations exceed the maximum capacity, the oldest will be cropped out (FIFO), like a stack. This cropping threshold is controlled by ```memory_ratio``` at ```chat_bot_0.py```, with value ```0.25``` which means there are 75% of tokens can serve as 'memories'. The set max token length is 8192. <br><br>
* **Special Tokens**: In large language model training, some special words are added to the dataset to guide through training. To use its fine-tuned model, we need to follow their special token format to get better performance. See Llama3.2's special token definition: https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/text_prompt_format.md. In this case, I remove the ```eos_token``` for the previous conversations.

## Requirments:
**Python packages:** ```transformers>=4.44.2, torch>=2.5.0, torchaudio>=2.5.0, torchvision>=2.5.0, Flask, ffmpeg-python, textile, soundfile， Flask-Session``` <br>
**Suggested Machine:** In the author's deployment, ```torch.bfloat16``` precision model is loaded at a ```RTX 3080``` GPU with around ```2 GB``` VRAM utilization for inference (average time: ```4~5 s```). Thus a Nvidia GPU with at least 2GB VRAM is suggested. <br>
**Model Download:** In this project, I used [unsloth](https://huggingface.co/unsloth/Llama-3.2-1B-Instruct)'s fine-tuned Llama3.2-1B model from huggingface. Other fine-tuned Llama3.2 are also feasible in theory but not tested. <br>
**(Optional) service exposure**: frp is configured to forward local service to public use.
**Dependencies:** ffmpeg

## Deployment:
1. Modify the ```model_id``` parameter to your downloaded Llama3.2-1B directory.
2. (Optional) To expose the service to the public, modify the ```frpc.ini``` file. Also, install and modify frps on the server side.
4. (Optional) Run the program at the backend: first activate your targeted python environment, then write a systemctl task to run the ```run_webbot.sh```.
5. Install ffmpeg (audio file decoding dependency). For Windows: download from [release](https://github.com/BtbN/FFmpeg-Builds), then add the /bin folder in the unzipped directory to system environment path. For Ubuntu: ```sudo apt install ffmpeg```.
6. To satisfy audio transmission from https protocol, SSL certification is essential for Flask server, which includes the public key (certification) and private key. You can either choose to generate one by yourself or apply for one from Service Providers.
7. RUn: Activate your environment, ```python app.py``` <br>

Starting Sequence: frps -> frpc -> app.py


## Disclaim:
This is a non-commercial project. The author is not responsible for any leading implication! Please do not use this project for any malicious purpose.
