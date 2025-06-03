ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:3.11
FROM $BUILD_FROM

WORKDIR /app

RUN apk add --no-cache \
    py3-paho-mqtt \
    py3-pyserial

# Copy main script
COPY serial2mqtt.py /app/serial2mqtt.py

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
