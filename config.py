# NOTE: No trailing comma at the end of the last field
class Config(object):
    SESSION_COOKIE_SECURE = False,
    SECRET_KEY = "my secret key",
    # WTF_CSRF_ENABLED = False


class DBConfig(object):
    MONGODB_HOST = "mongodb+srv://admin:admin@crypto.hkttz.mongodb.net/app"
