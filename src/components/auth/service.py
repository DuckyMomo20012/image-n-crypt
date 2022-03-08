from src.components.auth.model import TokenBlocklist


def getTokenBlocklistByJTI(jti):
    return TokenBlocklist.objects(jti=jti).first()
