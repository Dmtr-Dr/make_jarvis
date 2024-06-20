from datetime import datetime
from stt import transcribe_audio_file
from llm import answer_from_llm, get_random_ice_break
from tts import do_tts

def answer_action(current_audio_file,  st_memory=None, lt_memory=None, current_transcript = None):
    if not current_transcript:
        transcription = transcribe_audio_file(current_audio_file)
    else:
        transcription = current_transcript
    print(transcription)
    answer = answer_from_llm(transcription, st_memory=st_memory, lt_memory=lt_memory)
    
    if st_memory is not None:
        st_memory.append(("user",transcription))
        st_memory.append(("assistant",answer))
    
    print(answer)
    do_tts(answer)

def proactive_action(st_memory=None, lt_memory=None):
    answer = get_random_ice_break(st_memory=st_memory, lt_memory=lt_memory)

    if st_memory is not None:
        st_memory.append(("assistant",answer))    

    print(answer)
    do_tts(answer)