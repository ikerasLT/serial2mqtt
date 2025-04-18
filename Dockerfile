ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /app

RUN pip install paho-mqtt pyserial

COPY serial2mqtt.py /app/espnow_mqtt.py

COPY run.sh /app/run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

