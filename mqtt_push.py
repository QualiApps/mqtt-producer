#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import random
import json
import uuid
import sys
import time
from datetime import datetime

rmq_user = 'rabbit'
rmq_pass = 'rabbit'

rmq_host = (len(sys.argv) > 1) and sys.argv[1] or '127.0.0.1'
sleep_time = (len(sys.argv) > 2) and sys.argv[2] or 1
device_type = (len(sys.argv) > 3) and sys.argv[3] or 'temperature'
random_min = (len(sys.argv) > 4) and sys.argv[4] or 1
random_max = (len(sys.argv) > 5) and sys.argv[5] or 100
car_id = (len(sys.argv) > 6) and sys.argv[6] or 'car'


def on_connect(client, userdata, flags, rc):
    pass


try:
    client = mqtt.Client()
    client.username_pw_set(rmq_user, password=rmq_pass)
    client.on_connect = on_connect
    client.connect(rmq_host)

    while True:
        input_mess = {'id': str(uuid.uuid4()), 'car': str(car_id),
                      'time': str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
                      'type': device_type, 'value': random.randrange(int(random_min), int(random_max))}
        client.publish(topic="mqtt.device." + device_type, payload=json.dumps(input_mess), qos=0)
        time.sleep(float(sleep_time))
except KeyboardInterrupt:
    client.disconnect()
    print ''
except Exception as e:
    client.disconnect()
    print 'Producer error: ', e
