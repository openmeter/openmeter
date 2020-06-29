FROM arm32v7/ubuntu:18.04

RUN mkdir /dsmr_fluvius

RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y python3-serial python3-pip python3-yaml
RUN pip3 install paho-mqtt

COPY p1_fluvius_smartmeter.yaml /dsmr_fluvius/p1_fluvius_smartmeter.yaml
COPY p1_fluvius_smartmeter.py /dsmr_fluvius/p1_fluvius_smartmeter.py
COPY SM_raw.txt /dsmr_fluvius/SM_raw.txt

WORKDIR /dsmr_fluvius

#CMD ["/bin/bash"]
CMD ["python3","p1_fluvius_smartmeter.py"]