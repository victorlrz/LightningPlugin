#!/usr/bin/env python3
from lightning import Plugin
import time
import os
import json

plugin = Plugin()

@plugin.method("snake")
def snake(plugin):
    """Starts a game of snake in a new console"""
    plugin.log("starting snake")

    os.system('cmd.exe /c start cmd.exe /c cmd/k python "Z:\\Bitcoin\\vic\\snake.py"')

    return None

@plugin.method("getRewardMessage")
def getRewardMessage(plugin):
    """Outputs encoded reward message to send over the lightning network after you ended your snake game"""
    file = open("/mnt/z/Bitcoin/vic/rewards/reward.txt")
    score = int(file.read())

    scorestr = f"Your score is : {score}"

    plugin.log(scorestr)

    command = f'lightning-cli signmessage "{scorestr}"'
    stream = os.popen(command)
    output = stream.read()

    jsonstr = json.loads(output)


    for key in jsonstr:
        plugin.log(f"{key}: {jsonstr[key]}")

    stream.close()
    stream, output, jsonstr = None, None, None

    return None

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("Snake plugin initialized")

plugin.run()
