#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import uuid
import sys
import time
from telemetry import Telemetry
from datetime import datetime
import os
import random
import string

# RabbitMQ credentials
rmq_user = os.environ.get("RMQ_USER", "rabbit")
rmq_pass = os.environ.get("RMQ_PASS", "rabbit")

def vin_generator(size=17, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# broker IP
rmq_host = (len(sys.argv) > 1) and sys.argv[1] or os.environ.get("RMQ_PORT_5672_TCP_ADDR", "127.0.0.1")

# pause between each message (0.000002 ~8k/s)
sleep_time = (len(sys.argv) > 2) and sys.argv[2] or os.environ.get("DELAY_MESS", 0.5)

# object identifier (car-a, car-b, etc...)
vin = (len(sys.argv) > 3) and sys.argv[3] or 'VIN{}'.format(vin_generator())

try:
    client = mqtt.Client()
    client.username_pw_set(rmq_user, password=rmq_pass)
    client.connect(rmq_host)

    for data in Telemetry():
        input_mess = {
            'VIN': vin,
            'time': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        input_mess['telemetry'], input_mess['gps'] = data

        client.publish(topic="mqtt.device.telemetry",
                       payload=json.dumps(input_mess),
                       qos=0)

        #from pprint import pprint
        #pprint(input_mess)

        time.sleep(float(sleep_time))

except KeyboardInterrupt:
    client.disconnect()
except Exception as e:
    # disconnect client and reraise exception
    client.disconnect()
    raise
