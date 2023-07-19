import fire
import gevent
import gevent.monkey
gevent.monkey.patch_all()


def run_celery():
    from os import execvp
    execvp("celery", [
        "celery",
        "-A", "audio_jax_whisper.wsgi.celery", 
        "worker", "--loglevel=info", "--concurrency=1"
    ])


def run_flower():
    from os import execvp
    execvp("celery", [
        "celery",
        "-A", "audio_jax_whisper.wsgi.celery", 
        "flower"
    ])


def web():
    from os import execvp
    
    execvp("gunicorn", [
        "gunicorn",
        "--config", "audio_jax_whisper/gunicorn-conf.py",
        "--reload",
        "--bind", "127.0.0.1:5002",
        "audio_jax_whisper.wsgi",
    ])



if __name__ == "__main__":
    fire.Fire()