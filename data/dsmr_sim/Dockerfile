# version: 0.3
FROM arm32v7/ubuntu:18.04

RUN mkdir /dsmr_sim

RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y python3-serial python3-pip python3-yaml
RUN pip3 install paho-mqtt

COPY /openmeter/data/dsmr_sim/p1_smartmeter_fluvius_sim.py /dsmr_sim/p1_smartmeter_fluvius_sim.py

WORKDIR /dsmr_sim

#CMD ["/bin/bash"]
CMD ["python3","p1_smartmeter_fluvius_sim.py"]
