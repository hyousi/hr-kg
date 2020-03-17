import requests
import time


def ent2avpair(name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    }
    prefix = "http://shuyantech.com/api/cndbpedia/avpair?q="
    api_key = "&apikey=e9210d0f964182ceeca0827bfdb8373f"
    url = prefix + name + api_key
    response_flag = False
    while True:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        if response:
            response_flag = True
        else:
            print("No response, Try again")
        if response_flag:
            break
    return response.json()["ret"]


with open("people.jl") as f:
    profiles = [eval(line.strip()) for line in f.readlines()]

names = set(profile["name"] for profile in profiles)
for profile in profiles:
    name = profile["name"]
    avpairs = ent2avpair(name)
    for avpair in avpairs:
        if avpair[0] == "国籍" and avpair[1] not in ["中国", "中华人民共和国"]:
            print(f"{name}: {avpair}")
            names.remove(name)
