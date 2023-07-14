import multiprocessing


bind = "0.0.0.0:8080"
preload = True
timeout = 180
worker_class = 'gevent'

def post_fork(server, worker):
    import gevent.monkey
    gevent.monkey.patch_all()
