# mqtt_broker Dockerfile
# version: 0.5
# NOTE: Dockerfile for the MQTT broker for the openmeter project

FROM arm32v6/eclipse-mosquitto:1.6.9

EXPOSE 1883 9001
# expose these ports on the docker virtual network
# you still need to use -p or -P to open/forward these ports on host

COPY ./config/mosquitto.conf /mosquitto/config/mosquitto.conf


#RUN todo: checck if necessary
# forward request and error logs to docker log collector



#CMD ["", "", ""]
# required: run this command when container is launched
# only one CMD allowed, so if there are multiple, last one wins
