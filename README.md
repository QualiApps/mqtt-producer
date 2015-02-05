Mqtt producer
===========
The python script, which using as a MQTT producer for RabbitMQ broker. 

Running the daemon
-----------------

`docker run -d -P --name producer qapps/mqtt_producer [options]`


options:

    1 - rabbitmq IP-address (default - 127.0.0.1)

    2 - pause, between each message (in sec) (default - 1)

    3 - elasticsearch index type (string) (default - temperature)

    4 - min random value (int) (default - 1)

    5 - max random value (int) (default - 100)

    6 - id car (string) (default - "car")

