import pvporcupine
from pvrecorder import PvRecorder
import argparse
import os
import time
import struct
from dotenv import load_dotenv
import tempfile

from stt import get_wav_file
from agent import Agent


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_device_index', help='Index of input audio device', type=int, default=0)
    parser.add_argument('--audio_buffer_file', help='Absolute path to record audio', default="current.wav")
    args = parser.parse_args()
    
    audio_buffer_file_name = args.audio_buffer_file
    audio_device_index = args.audio_device_index
    proactivity_frequency_sec = 10
    keywords_command = {
        0: 'wakeword',
        1: 'stopword',
        2: 'interrupt'
    }
    
    load_dotenv()
    api_key = os.getenv('API_KEY')
    wake_keyword_path = 'C:/Users/User1/Desktop/make_jarvis/.venv/dear/wake_word/Милый_ru_windows_v3_0_0.ppn'
    stop_keyword_path = 'C:/Users/User1/Desktop/make_jarvis/.venv/dear/wake_word/Хватит_ru_windows_v3_0_0.ppn'
    interrupt_keyword_path = 'C:/Users/User1/Desktop/make_jarvis/.venv/dear/wake_word/Достаточно_ru_windows_v3_0_0.ppn'
    model_path = 'C:/Users/User1/Desktop/make_jarvis/.venv/dear/wake_word/porcupine_params_ru.pv'

    porcupine = pvporcupine.create(access_key=api_key, keyword_paths=[wake_keyword_path, stop_keyword_path], model_path=model_path)

    recorder = PvRecorder(frame_length=porcupine.frame_length, device_index= audio_device_index)
    recorder.start()

    current_audio_file_name = os.path.abspath(audio_buffer_file_name)
    wav_file = get_wav_file(current_audio_file_name)
    
    settings = {
        "proactivity_frequency_sec":proactivity_frequency_sec,
        "wav_file": wav_file,
        "current_audio_file_name":current_audio_file_name,
        "memory_debug_thread": False,
        "proactive_actions_thread": False
        }
        
    agent = Agent(settings)       
    agent.start()

    try:
        while agent.is_alive():
            pcm = recorder.read()
            result = porcupine.process(pcm)
            wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))
           
            if result >= 0:
                
                current_audio_content = open(current_audio_file_name, 'rb').read()
                temp_audio_file_name = tempfile.mktemp(suffix=".wav")
                with open(temp_audio_file_name, 'wb') as f:
                    f.write(current_audio_content)
                agent.add_event ({'type':keywords_command[result],'result':None, 'current_audio_file_name':temp_audio_file_name})
                if wav_file is not None:
                    wav_file.close()
                os.unlink(current_audio_file_name)
                wav_file  = get_wav_file(current_audio_file_name)  


    except KeyboardInterrupt:
        print('Stopping....')
        agent.stop()
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()