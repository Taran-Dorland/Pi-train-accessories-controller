import requests
import json

def getTurnouts():
    url = 'http://192.168.0.230:12080/json/turnouts'
    req = requests.get(url)
    data = json.loads(req.content)
    return data



def getRoster():
    url = 'http://192.168.0.230:12080/json/roster'
    req = requests.get(url)
    data = json.loads(req.content)
    return data