"""
Taken from Book: Hands-On MQTT Programming with Python
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""

from config import *
import paho.mqtt.client as mqtt
import time
from vehicle_commands import *
import json

object_name = "thingstodo"
commands_topic = "myapi/thingstodo/new/{}/commands".format(object_name)

class LoopControl:
    is_last_command_processed = False

def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))
    client.subscribe("mqtt/listen/#", qos=2)
    client.subscribe("myapi/thingstodo/done/#", qos=2)


def on_subscribe(client, userdata, mid, granted_qos):
    print("I've subscribed with QoS: {}".format(
        granted_qos[0]))


def on_message(client, userdata, msg):
    pass

def publish_command(client, command_name, key="", value=""):
    command_message = build_command_message(
        command_name, key, value)
    result = client.publish(topic=commands_topic,
                            payload=command_message, qos=2)
    print("Command sent to {}".format(commands_topic))
    time.sleep(1)
    return result

def build_command_message(command_name, key="", value=""):
    if key:
        command_message = json.dumps({
            COMMAND_KEY: command_name,
            key: value})
    else:
        command_message = json.dumps({
            COMMAND_KEY: command_name})
    return command_message

def on_message_answer(client, userdata, msg):
    print("Message received on ANSWER. Topic: {}. Payload: {}".format(
        msg.topic, 
        str(msg.payload)))
    time.sleep(5)
    for i in range(100):
        publish_command(client, str(msg.payload), "GO", i)
    
def on_message_jobdone(client, userdata, msg):
    print("Message received on JOBDONE. Topic: {}. Payload: {}".format(
        msg.topic, 
        str(msg.payload)))

if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.max_inflight_messages_set(2000)
    client.reconnect_delay_set(min_delay=1, max_delay=240)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.message_callback_add('mqtt/listen/thingstodo/#',on_message_answer)
    client.message_callback_add('myapi/thingstodo/done/thingstodo/#',on_message_jobdone)
    client.on_message = on_message
    client.connect(host=mqtt_server_host,
        port=mqtt_server_port,
        keepalive=mqtt_keepalive)
    client.loop_forever()