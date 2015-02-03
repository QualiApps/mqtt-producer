# Version: 0.0.1
FROM fedora:21

MAINTAINER Yury Kavaliou <test@test.com>

RUN yum install -y python-pip
RUN pip install paho-mqtt

ADD mqtt_push.py /home/mqtt_push.py

ENTRYPOINT ["python", "/home/mqtt_push.py"]
