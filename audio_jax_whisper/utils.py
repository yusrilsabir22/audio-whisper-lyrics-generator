import time
import inspect
import os

from contextlib import contextmanager
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    cfg = {"broker_url": f"redis://{app.config.get('REDIS_URL')}", "result_backend": f"redis://{app.config.get('REDIS_URL')}"}
    celery.conf.update(cfg)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@contextmanager
def approx_time():
    start = time.time()
    yield
    end = time.time()
    print(f"APPROX: {end-start}")
    
    
def get_name( frame ):
  code = frame.f_code
  name = code.co_name
  for objname, obj in frame.f_globals.items().__iter__():
    try:
      assert obj.__dict__[name].func_code is code
    except Exception:
      pass
    else: # obj is the class that defines our method
      name = '%s.%s' % ( objname, name )
      break
  return name


def get_class_from_frame(fr):
  import inspect
  args, _, _, value_dict = inspect.getargvalues(fr)
  # we check the first parameter for the frame function is
  # named 'self'
  if len(args) and args[0] == 'self':
    # in that case, 'self' will be referenced in value_dict
    instance = value_dict.get('self', None)
    if instance:
      # return its class
      return getattr(instance, '__class__', None)
  # return None otherwise
  return None


class SequentialExecution:
    def __init__(self, frame):
        self.frame = frame
        pass
    
    def __enter__(self):
        indent = 4
        
        # print(self.frame.f_code.co_consts)
        s = inspect.getsourcelines(self.frame.f_code)
        scripts = s[0][1:]
        script = ""
        for line in scripts:
            
            if "with SequentialExecution" in line:
                script += line
                continue
            line_indent = len(line) - len(line.lstrip())
            
            f1 = f"{' '*line_indent}with SequentialExecution(frame=inspect.currentframe()):\n"
            body = f'{" "*indent}{line}'
            script += f"{f1}{body}"
        eval(script)
    def __exit__(self, *args):
        pass