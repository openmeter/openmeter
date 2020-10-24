FROM python:3.9-alpine3.12

RUN mkdir /dsmr_fluvius

RUN apt-get update

RUN pip install pyserial
RUN pip install pyyaml

RUN pip install paho-mqtt

COPY p1_smartmeter_fluvius.yaml /dsmr_fluvius/p1_smartmeter_fluvius.yaml
COPY p1_smartmeter_fluvius.py /dsmr_fluvius/p1_smartmeter_fluvius.py

WORKDIR /dsmr_fluvius

ENTRYPOINT ["python3","p1_smartmeter_fluvius.py"]

CMD p1_smartmeter_fluvius.py