from os import environ

_ = environ.get

REDIS_URL = _("REDIS_URL", "localhost:6379")