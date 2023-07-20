import time
import whisper
import requests

from celery import shared_task
from celery.contrib.abortable import AbortableTask
from .custom_transcribe import transcribe


# the reason we need to overridde Whisper.transcribe function is to pass custom args
# so we can abort transcribe process when celery.is_aborted is True
# on python this method called monkey patching
whisper.Whisper.transcribe = transcribe


@shared_task(bind=True, base=AbortableTask)
def transcribe_audio(self, data):
    # retrieve data task
    audio_url = data['audio_url']
    language = data['language']
    cb_url = data['cb_url']
    
    # Load model once
    global model
    try:
        if not isinstance(model, whisper.Whisper):
            model = whisper.load_model("tiny", download_root="whisper_pretrained_model")
    except NameError:
        model = whisper.load_model("tiny", download_root="whisper_pretrained_model")
    
    audio = whisper.load_audio(data['audio_url'])
    result = model.transcribe(audio, language=language, fp16=False, is_aborted=self.is_aborted)
    # # if the task is aborted: model.transcribe should be return string e.g. "Task is aborted"
    # # for more information see custom_transcribe.py
    # if isinstance(result, str):
    #     return result

    # post the result to callback url or cb_url
    requests.post(cb_url, json={
        "videoId": audio_url.split("/")[-1],
        "data": result['segments']
    })
    
    return "Done"