#!/usr/bin/env python
import os
from mqttwrapper import run_script
import json

vehicle_name = "warranty"
commands_topic = "gsxapi/warranty/done/{}/commands".format(vehicle_name)

def message_callback(topic: str, payload: bytes):
    print("Callback from gsxapi new")
    return ["gsxapi/warranty/done/ack", payload]
    
def main():
    run_script(message_callback, broker="mqtt://127.0.0.1",topics=["gsxapi/warranty/new/#"])

if __name__ == '__main__':
    main()