import json, pickle
def getInput(*args):
    ans = {}
    for arg in args:
        ans[f"{arg}"] = str(input(f"{arg}: "))
    return ans

def handleRes(ob, msg="", extract=None):
    # print("ob", ob)
    # print(type(ob))
    if not ob:
        return msg
    ob = json.loads(ob)
    if "status" in ob.keys():
        if ob["status"] == "error":
            return f"Error: %s" % ob.get("message")

    if "data" in ob.keys():
        if type(ob.get("data")) ==  list:
            if len(ob.get("data")) == 0:
                return msg + "No data"
            result = msg
            for item in ob.get("data"):
                if extract:
                    result += " " + json.dumps(item[extract])
                else:
                    result += " " + json.dumps(item)
            return result
        if type(ob.get("data")) == dict:
            return msg + json.dumps(ob.get("data"))
        return msg + ob.get("data")


if __name__ == "__main__":
    # ans = getInput("username", "password")
    # print(ans)
    handleRes({"status": "success","code": "200","data": [{"img_name": "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}, {"img_name": "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}],}, "Image list: ", extract="img_name")