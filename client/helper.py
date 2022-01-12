import json, pickle
def getInput(*args):
    ans = {}
    for arg in args:
        ans[f"{arg}"] = str(input(f"{arg}: "))
    return ans

def handleRes(ob, msg="", extract=None):
    if ob == None:
        return msg
    ob = json.loads(ob)
    if "status" in ob.keys():
        if ob["status"] == "error":
            print(f"Error: %s" % ob.get("message"))
            return

    if "data" in ob.keys():
        if type(ob.get("data")) ==  list:
            if len(ob.get("data")) == 0:
                print(msg + "No data")
            result = msg
            for item in ob.get("data"):
                if extract:
                    result += " " + json.dumps(item[extract])
                else:
                    result += " " + json.dumps(item)
            print(result)
            return
        if type(ob.get("data")) == dict:
            print(msg + json.dumps(ob.get("data")))
            return
        print(msg + ob.get("data"))
        return


if __name__ == "__main__":
    # ans = getInput("username", "password")
    # print(ans)
    handleRes({"status": "success","code": "200","data": [{"img_name": "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}, {"img_name": "bicycle.png","img_content": "\u00ff...","quotient": "22 22...",}],}, "Image list: ", extract="img_name")