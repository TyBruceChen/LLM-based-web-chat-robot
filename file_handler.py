import os
import ffmpeg #get ffmpeg installed from https://github.com/BtbN/FFmpeg-Builds, and add ffmpeg to env PATH

def clear_folder(folder_name = 'audios'):
    file_list = os.listdir(folder_name)
    for file in file_list:
        file_path = os.path.join(folder_name, file)
        os.remove(file_path)

def convert_to_wav(audio_path, folder_name = 'audios'):
    # Convert the file to a 16,000 Hz, mono, PCM format .wav
    compressed_audio = ffmpeg.input(audio_path)
    
    output_name = 'converted_' + os.path.basename(audio_path)
    
    compressed_audio.output(output_name, ar=16000, ac=1, format='wav', acodec='pcm_s16le').run()
    compressed_audio = 0
    os.remove(audio_path)
    output_path = os.path.join(folder_name, output_name)
    os.replace(output_name, output_path)

    return output_path

if __name__ == '__main__':
    convert_to_wav('audios\\1.wav')