import json
from typing import Tuple, Union


def getInput(*args):
    ans = {}
    for arg in args:
        ans[f"{arg}"] = str(input(f"{arg}: "))
    return ans


def handleRes(res: Tuple[str, int], msg="") -> str:
    if not res:
        return msg

    data, status = res
    dataObj: Union[dict, list] = json.loads(data)
    if status is not None:

        # We got status code 4xx
        if status // 100 == 4 and isinstance(dataObj, dict):
            return "Error: %s" % dataObj.get("message", "")

    if data is not None:
        if isinstance(dataObj, list):
            if len(dataObj) == 0:
                return msg + "No data"

            result = msg

            result += json.dumps(dataObj)

            return result

        return msg + json.dumps(dataObj)
