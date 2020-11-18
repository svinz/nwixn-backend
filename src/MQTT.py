import paho.mqtt.client as mqtt
import ssl
import os
import socket
import logging

LOG = logging.getLogger("root")

class NW3MQTT:
    """ Class for the MQTT communication to MQTT broker
    """
    def __init__(self, server, port ,topic, ca, cert, keyfile):
        #
        self._server = server
        self._topic = topic
        self._port = port
        
        #check if the certs is actually files
        if not os.path.isfile(ca): 
            LOG.debug("Unable to find: {}".format(ca))
            raise IOError("Unable to find: {}".format(ca))
        if not os.path.isfile(cert):
            LOG.debug("Unable to find: {}".format(cert))
            raise IOError("Unable to find: {}".format(cert))
        if not os.path.isfile(keyfile):
            LOG.debug("Unable to find: {}".format(keyfile))
            raise IOError("Unable to find: {}".format(keyfile))

        self.mqttc = mqtt.Client()
        self.mqttc.enable_logger(logger=LOG) #enabling the logger 
        self.mqttc.tls_set(ca_certs=ca, certfile=cert, keyfile=keyfile, cert_reqs=ssl.CERT_REQUIRED)
        try:
            self.mqttc.connect(self._server,self._port,60)
            LOG.info("Connected to: {}:{}".format(self._server,self._port))
        except socket.gaierror as e:
            LOG.exception(e)
            LOG.error("Cannot connect to server: {}:{}".format(self._server,self._port))
        
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        subscribe_topics = []
        for i in topic["subscribe"]:
            subscribe_topics.append((i,1))
        self.mqttc.subscribe(subscribe_topics)
        #self.mqttc.loop_start()

    def publish(self, topic, message):
        self.mqttc.publish(topic=topic,payload=message,qos=1)
        
    def __call__(self):
        self.mqttc.loop()

    def on_message(self,mqttc,userdata,message):
        #print(userdata)
        #print(message.topic + ": " + str(message.payload))
        LOG.info(message.topic + ": " + message.payload.decode())
    def on_subscribe(self,mqttc, obj, mid, granted_qos):
        LOG.info("Subscribed: " + str(mid) + " " + str(granted_qos))
        #print("Subscribed: " + str(mid) + " " + str(granted_qos))
