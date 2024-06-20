import vosk
import json
import wave

def get_wav_file(file_name):
    wav_file = wave.open(file_name, "w")
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(16000)
    return wav_file    

def transcribe_audio_file(input_audio_file):

    model = vosk.Model(lang='ru')

    wf = wave.open(input_audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        return None

    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    result_text = ""
    previous_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            current_text = result.get('text', '')
            if current_text != previous_text: 
                result_text += current_text + " "
                previous_text = current_text
        else:
            partial_result = json.loads(rec.PartialResult())
            current_text = partial_result.get('partial', '')
            if current_text != previous_text: 
                result_text += current_text + " "
                previous_text = current_text

    final_result = json.loads(rec.FinalResult())
    current_text = final_result.get('text', '')
    if current_text != previous_text: 
        result_text += current_text

    # Закрываем файл
    wf.close()

    return result_text.strip()