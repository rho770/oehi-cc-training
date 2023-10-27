#!/usr/bin/env python

import os
import platform
import random
import time
from paho.mqtt import client as mqtt_client


#broker = 'localhost'           # Broker in container should be used for the tutorial
broker = 'broker.emqx.io'       # Free public MQTT broker
port = 1883
topic = "data-collector"
node = platform.node()

# Generate a Client ID with the publish prefix.
client_id = f'edge-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def collect_publish(client):
    while True:
        time.sleep(1)
        load = os.getloadavg()
        msg = f"{node};{load[0]}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    collect_publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
