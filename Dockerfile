# MQTT Producer

FROM fedora:21

MAINTAINER Yury Kavaliou <yury_kavaliou@epam.com>

RUN yum install -y python-pip \
    && pip install paho-mqtt

COPY ./trips/ /home/trips/
COPY telemetry.py /home/telemetry.py
COPY mqtt_push.py /home/mqtt_push.py

ENTRYPOINT ["python", "/home/mqtt_push.py"]