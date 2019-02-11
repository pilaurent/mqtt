"""
Taken from Book: Hands-On MQTT Programming with Python
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from config import *
from vehicle_commands import *
import paho.mqtt.client as mqtt
import time
import json


things_name = "thingstodo"
commands_topic = "mqtt/listen/{}/commands".format(things_name)
processed_commands_topic = "foo/{}/executedcommands".format(things_name)

class LoopControl:
    is_last_command_processed = False

def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))
    # Check whether the result form connect is the CONNACK_ACCEPTED connack code
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to the commands topic filter
        client.subscribe(
            processed_commands_topic, 
            qos=2)


def on_message(client, userdata, msg):
    if msg.topic == processed_commands_topic:
        print(str(msg.payload))
        if str(msg.payload).count(CMD_TURN_OFF_ENGINE) > 0:
            LoopControl.is_last_command_processed = True


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))


def build_command_message(command_name, key="", value=""):
    if key:
        # The command requires a key
        command_message = json.dumps({
            COMMAND_KEY: command_name,
            key: value})
    else:
        # The command doesn't require a key
        command_message = json.dumps({
            COMMAND_KEY: command_name})
    return command_message

def publish_command(client, command_name, key="", value=""):
    command_message = build_command_message(
        command_name, key, value)
    result = client.publish(topic=commands_topic,
                            payload=command_message, qos=2)
    print("Command sent to {}".format(commands_topic))
    time.sleep(1)
    return result


if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    last_will_payload = build_command_message(CMD_PARK_IN_SAFE_PLACE)
    client.will_set(topic=commands_topic, 
        payload=last_will_payload, 
        qos=2,
        retain=True)
    client.connect(host=mqtt_server_host,
       port=mqtt_server_port,
       keepalive=mqtt_keepalive)
    client.loop_start()

    publish_command(client, "START", "START", 0)
    client.disconnect()
    client.loop_stop()
