# NOTE: No trailing comma at the end of the last field!!!
# NOTE: No trailing comma at the end of the last field!!!
# NOTE: No trailing comma at the end of the last field!!!
class Config(object):
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = "my secret key"
    WTF_CSRF_ENABLED = False


class DBConfig(object):
    MONGODB_HOST = "mongodb+srv://<username>:<password>@crypto-image.u1r0p.mongodb.net/CryptoImage"


class JWTConfig(object):
    JWT_SECRET_KEY = "my super secret key"
