#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read data from a Smartmeter's P1 port and publish it via MQTT
"""

import paho.mqtt.client as mqtt
import time
import threading
import sys
import random

mqtt_broker = "mqtt_broker"

class MyTelegram:
    def __init__(self):
        self.actual_voltage_l1 = 230
        self.actual_amperage_l1 =0
        self.actual_power_used_watt = 0
        self.actual_power_returned_watt = 0
        self.day_used_KWh = 0
        self.night_used_KWh = 0
        self.day_returned_KWh = 0
        self.night_returned_KWh = 0
        self.gasmeter = 0


def send_p1_telegram(mqttc, mqtt_topic_base, tele):
    # Mimic real data
    telegram.actual_voltage_l1 = round(random.uniform(220,240),2)
    telegram.actual_amperage_l1 =round(random.uniform(3,5),2)
    telegram.actual_power_used_watt =round(telegram.actual_voltage_l1 * telegram.actual_amperage_l1,0)
    telegram.actual_power_returned_watt = random.randint(3000,4000)
    telegram.day_used_KWh =round(tele.day_used_KWh + 0.05,2)
    telegram.night_used_KWh =round(tele.night_used_KWh + 0.01,2)
    telegram.day_returned_KWh =round(tele.day_returned_KWh + 0.001,2)
    telegram.night_returned_KWh =round(tele.night_returned_KWh,2)
    telegram.gasmeter = round(tele.gasmeter + 0.05,2)

    for attr, value in telegram.__dict__.items():
        topic = mqtt_topic_base + attr
        publish_message(mqttc, topic, value)


def recon():
    if reconnect_counter > 5:
        sys.exit(1)

    try:
        mqttc.reconnect()
        print("Successful reconnected to the MQTT server")
    except:
        print("Could not reconnect to the MQTT server")


def on_connect(client, userdata, flags, rc):
    print("Successful connected to the MQTT server")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from MQTT, trying to reconnect")
        recon()


def publish_message(mqttc, mqtt_path, msg):
    mqttc.publish(mqtt_path, payload=msg, qos=0, retain=False)
    print(
        "published message {0} on topic {1} at {2}".format(
            msg, mqtt_path, time.asctime(time.localtime(time.time()))
        )
    )



def main():
    ###
    # Main
    ###

    # Connect to the MQTT broker
    mqttc = mqtt.Client("smartmeter_simulator")
    mqttc.username_pw_set("mqtt_username", "mqtt_password")

    # Define the mqtt callbacks
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect

    # Connect to the MQTT server
    try:
        mqttc.connect(mqtt_broker, port=1883, keepalive=45)
    except Exception as err:
        print("could not connect to the mqtt host: {}".format(err))

    print(
        "succesful connected to the mqtt host {}:{}".format(
        mqtt_broker, "1883"
        )
    )

    # Run in simulation
    print("Running in simulation mode")

    mqtt_topic_base = "Home/Smartmeter/Simulation/"
    global telegram
    telegram = MyTelegram()

    while True:
        send_p1_telegram(mqttc, mqtt_topic_base, telegram)
        print('ok')
        time.sleep(5)



if __name__ == "__main__":
    sys.exit(main())


# End of program