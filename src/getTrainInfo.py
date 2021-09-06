import sys, os
import requests
import json

#----------------------------------------------------------------
# Get info from file
with open(os.path.join(sys.path[0], "../include/settings.json")) as file:
    json_settings = json.load(file)

version = json_settings["Version"]
server_ip = json_settings["JMRI_Server"]["IP"]
server_port = json_settings["JMRI_Server"]["Port"]
server_url = "http://{0}:{1}".format(server_ip, server_port)

#----------------------------------------------------------------
# Getters

def getTurnouts():
    url = "{0}/json/turnouts".format(server_url)
    req = requests.get(url)
    data = json.loads(req.content)
    return data

def getRoster():
    url = "{0}/json/roster".format(server_url)
    req = requests.get(url)
    data = json.loads(req.content)
    return data