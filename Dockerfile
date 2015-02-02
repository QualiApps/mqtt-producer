# Version: 0.0.1
FROM fedora:21
MAINTAINER Yury Kavaliou <test@test.com>
RUN yum install -y python-pip
RUN pip install paho-mqtt
