from os import environ

_ = environ.get

REDIS_URL = _("REDIS_URL", "localhost:6379")
S3_ENDPOINT_URL = _("S3_ENDPOINT_URL")
S3_API_KEY = _("S3_API_KEY")
S3_API_SECRET = _("S3_API_SECRET")
S3_BUCKET = _("S3_BUCKET")
S3_REGION = _("S3_REGION")