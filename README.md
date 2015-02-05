# Mqtt producer
The python script, which using as a MQTT producer for RabbitMQ broker. 

Running the daemon

<pre>
<code>
docker run -d -P --name producer qapps/mqtt_producer [options]
</code>
</pre>

options:
    RMQ_SERVER_IP - rabbitmq IP-address
    SLEEP_TIME - pause, between each message
    ES_INDEX_TYPE - elasticsearch index type
    RAND_MIN - min value
    RAND_MAX - max value
    CAR_ID - id car
