from flask_restx import Model, fields, reqparse
from werkzeug.datastructures import FileStorage

from src.api.v1.users.views import ns_users

responseListImageModel: Model = ns_users.model(
    "ResponseListImage",
    {
        "img_name": fields.String(description="Image name", example="bicycle.png"),
    },
)

imageModel: Model = ns_users.model(
    "Image",
    {
        "img_content": fields.String(
            description=(
                "Image encrypted content. Can be decrypted using"
                " function `decrypt` in `helpers.crypto.crypto.py`, requires user's"
                " private key. Private key MUST be generated from"
                " `generateAndWriteKeyToFile` function."
            ),
            example="PNG\r\n\u001a\n\u0000...",
        ),
        "img_name": fields.String(description="Image name", example="bicycle.png"),
        "quotient": fields.String(
            description="Quotient for encrypted content",
            example="98 98 98 98 77 2 91 91...",
        ),
    },
)


permissionModel: Model = ns_users.model(
    "Permission",
    {
        "userId": fields.String(
            description="User id", example="628387db1dc6fa1a0cd84c42"
        ),
        "role": fields.String(description="User role for this image", example="write"),
    },
)

uploadImageFormParser: reqparse.RequestParser = ns_users.parser()
uploadImageFormParser.add_argument(
    "imageFile", location="files", type=FileStorage, required=True
)
uploadImageFormParser.add_argument("quotient", location="form", required=True)


shareImageFormParser: reqparse.RequestParser = ns_users.parser()
shareImageFormParser.add_argument("user_id", location="form", required=True)
shareImageFormParser.add_argument("role", location="form", required=True)

editPermissionFormParser: reqparse.RequestParser = shareImageFormParser.copy()
editPermissionFormParser.remove_argument("user_id")
