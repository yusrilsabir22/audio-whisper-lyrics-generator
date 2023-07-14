import json
import sys
import time
import requests
import logging

from flask import Blueprint, request, url_for, abort, Response, stream_with_context
from celery import current_app
from urllib.parse import urlparse, parse_qs
from .tasks import transcribe_audio


main = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@main.route("/")
def index():
    logger.info("test")
    return "ok"


@main.route("/transcribe")
def transcribe():
    audio_url = request.args.get("audio_url")
    assert audio_url != None
    language = request.args.get("language")
    cb_url = url_for("main.bg_hook", _external=True, secret="test")
    data = dict(
        audio_url=audio_url,
        cb_url=cb_url,
        language=language or "en"
    )
    job = transcribe_audio.delay(data)
    return json.dumps({"message": "push to queue", "status": "processing", "job": job.task_id})


@main.route("/cancel-job")
def get_jobs():
    task_id = request.args.get("task_id")
    task = transcribe_audio.AsyncResult(task_id)
    task.abort()
    return f"cancelled {task_id}"


@main.route("/list-jobs")
def list_jobs():
    capp = current_app.tasks['audio_jax_whisper.tasks.transcribe_audio']
    i = capp.app.control.inspect()
    n_tasks = []
    n_tasks.extend(i.active()['celery@blondev.local'])
    n_tasks.extend(i.reserved()['celery@blondev.local'])
    return json.dumps(n_tasks)


@main.route("/bg-hook", methods=["POST"])    
def bg_hook():
    secret = request.args.get("secret")
    if secret != "test":
        abort(401)
    body = request.json
    print(f"BG HOOK: {body}")
    print("\nsave to db...")
    return "", 200
