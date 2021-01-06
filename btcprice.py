#!/usr/bin/env python3
from lightning import Plugin
import time
import requests

plugin = Plugin()

pluginRun = {"running": True}

symbols = {"EUR":" EUR", "USD":" $", "GBP":" GBP"}

def getBTCvalue(currency):
    res = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    resjson = res.json()
    symbol = symbols[str(currency).strip()]
    return "1 BTC = " + resjson['bpi'][currency]['rate'] + symbol

@plugin.method("BTCvalue")
def BTCvalue(plugin, stopstr=None, currency="USD", count=0, starttime = time.time()):
    """This plugin display BTC value for several currencies and suscribe to several RPC events"""
    global pluginRun
    
    stop = None

    if (stopstr == "True"):
        stop = True
    elif (stopstr == "False"):
        stop = False
    else:
        stop = None

    if (stop != None):
        pluginRun['running'] = stop

    if (pluginRun['running']):
        return None

    count += 1
    #plugin.log(f"tick {count}")
    plugin.log(getBTCvalue(currency))

    time.sleep(5.0 - ((time.time()) - starttime) % 5.0)
    BTCvalue(plugin, None, currency, count, starttime)

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("THE SUPER PLUGIN IS NOT CRASHING")

"""@plugin.subscribe("connect")
def on_connect(plugin, **kwargs):
    plugin.log(str(kwargs))
#plugin.log(f"Received connect event for peer {id} at address: {address}")

@plugin.subscribe("channel_opened")
def on_open(plugin, **kwargs):
    plugin.log(str(kwargs))
    plugin.log("opened channel")

@plugin.subscribe("disconnect")
def on_disc(plugin, id):
    plugin.log(f"Disconnected from peer : {id}")"""

"""
@plugin.subscribe("channel_opened")
def on_channel_opened(plugin, **kwargs):
    print("channel_opened")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("connect")
def on_connect(plugin, **kwargs):
    print("connect")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("disconnect")
def on_disconnect(plugin, **kwargs):
    print("disconnect")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("invoice_payment")
def on_invoice_payment(plugin, **kwargs):
    print("invoice_payment")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("warning")
def on_warning(plugin, **kwargs):
    print("warning")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("forward_event")
def on_forward_event(plugin, **kwargs):
    print("forward_event")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("sendpay_success")
def on_sendpay_success(plugin, **kwargs):
    print("sendpay_success")
    plugin.log(str(kwargs))
    return str(kwargs)

@plugin.subscribe("sendpay_failure")
def on_sendpay_failure(plugin, **kwargs):
    print("sendpay_failure")
    plugin.log(str(kwargs))
    return str(kwargs)
"""

plugin.run()
