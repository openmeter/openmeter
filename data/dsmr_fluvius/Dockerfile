FROM arm32v7/ubuntu:18.04 as base

RUN mkdir /dsmr_fluvius

RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y python3-serial python3-pip python3-yaml
RUN pip3 install paho-mqtt

COPY p1_smartmeter_fluvius.yaml /dsmr_fluvius/p1_smartmeter_fluvius.yaml
COPY p1_smartmeter_fluvius.py /dsmr_fluvius/p1_smartmeter_fluvius.py

WORKDIR /dsmr_fluvius


############# Development################

FROM base as development

RUN pip3 install debugpy

ENTRYPOINT ["python3","-m","debugpy","--listen","0.0.0.0:5678","--wait-for-client","-m","p1_smartmeter_fluvius.py"]

############# Production #################

FROM base as production

ENTRYPOINT ["python3","-m"]

CMD p1_smartmeter_fluvius.py