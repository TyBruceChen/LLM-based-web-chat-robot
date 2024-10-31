from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio   #to read mp3 file, pydub and ffmpeg backend are required to install

def load_whisper_model(model_id = "whisper-base-openai"):
    print("Loading Whisper Processor and Model ...")
    whisper_processor = WhisperProcessor.from_pretrained(model_id)
    whisper_model = WhisperForConditionalGeneration.from_pretrained(model_id)
    print("Whisper Loaded")
    return whisper_processor, whisper_model

def whisper_transcribe(audio_path, 
                      whisper_processor,
                      whisper_model,
                      sample_rate = 16000, 
                      input_language = None, #['english', 'chinese','japanese', None]
                      whisper_task = None, #['translate','transcribe',None]
                      return_special_tokens = True):
        
    #audio, original_sample_rate = librosa.load(model_id, sr=sample_rate)
    audio, original_sample_rate = torchaudio.load(audio_path, normalize = True)
    print(f'Original Sample Rate: {original_sample_rate}')
    if len(audio.shape) > 1:
        audio = audio.mean(dim=0) #convert the stero audio into monophonic audio

    audio = torchaudio.transforms.Resample(orig_freq = original_sample_rate, new_freq = sample_rate)(audio)
    print(audio.shape)
    print(audio)


    whisper_model.config.force_decoder_ids = input_language   #Currently, it does not set with any pre-defined language detection mode
    if whisper_task != None:
        forced_decoder_ids = whisper_processor.get_decoder_prompt_ids(language = input_language, task=whisper_task)

    input_features = whisper_processor(
        audio, 
        sampling_rate = sample_rate, 
        return_tensors = "pt").input_features

    if whisper_task != None:
        predicted_ids = whisper_model.generate(input_features, forced_decoder_ids = forced_decoder_ids)
    else:
        predicted_ids = whisper_model.generate(input_features)
        
    transcription = whisper_processor.batch_decode(predicted_ids, skip_special_tokens = return_special_tokens)

    print(transcription)
    return transcription[0]

    if __name__ == "__main__":
        whisper_processor, whisper_model = load_whisper_model()
        whisper_transcibe('Recording_CN_EN.mp3', whisper_processor, whisper_model)
        print()
