""" MQTT message qclient """
########## Connection methods ######################

import os
import uuid
import json
import socket
import paho.mqtt.client as mqtt
from dataprovider.logger.log import LOGGER

class MqttClient(mqtt.Client):

    def _sock_recv(self, bufsize):
        try:
            return super()._sock_recv(bufsize)
        except AttributeError as exc:
            LOGGER.debug("Socket None workaround: %s", exc)
            raise socket.error

class QClient:
    """ MQTT message qclient """

    DEFAULT_KEEPALIVE = 30
    VALID_TRANSPORT_TYPES = ["tcp", "websockets"]

    def __init__(self, topic=None):
        """ Instantiate mqtt qclient"""

        # connection string will be read from env variables
        self.broker_host = "172.17.0.1"
        self.broker_port = "1883"
        self.broker_keepalive = QClient.DEFAULT_KEEPALIVE
        self.topic = topic
        self.transport = "tcp"

        self.publish_calls = 0
        self.publish_callbacks = 0

        self.active = False
        self._init_from_env()
        self._init_qclient()

    def _init_from_env(self):
        """ Initialize consumer from environment variables """
        env_broker_host = os.getenv('QCLIENT_BROKER_HOST')
        env_broker_port = os.getenv('QCLIENT_BROKER_PORT')

        if env_broker_host is not None:
            self.broker_host = str(env_broker_host)

        if env_broker_port is not None:
            self.broker_port = str(env_broker_port)

    def _init_qclient(self):
        """ _init_qclient """
        LOGGER.info("_init_qclient - ENTER")
        # different id for each workspace
        random_id = str(uuid.uuid4())[0:10]
        client_id = 'DataProvider-' + random_id
        LOGGER.info("Init mqtt client, transport = %s", self.transport)
        self.client = MqttClient(client_id=client_id, transport=self.transport)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_socket_close = self.on_socket_close

        self.connect()

        LOGGER.info("_init_qclient - LEAVE")

########## Publish method ##########################

    def publish(self, message):
        """ Publish message """
        json_message = json.dumps(message)
        LOGGER.debug("sending message to topic %s", self.topic)
        self.publish_calls += 1
        try:
            res = self.client.publish(self.topic, json_message, 1)
            # https://stackoverflow.com/questions/25815910/unable-to-receive-more-than-20-mqtt-messages-using-mosquitto-paho-for-python
            # 2 seconds for 10 packets ?
            #self.client.loop(2, 10)
            res.wait_for_publish()
        except Exception as exc:
            LOGGER.debug("Publishing failed with error: %s", exc)

    def connect(self):
        """ Connect """
        self.active = True
        self.__connect()

    def disconnect(self):
        """ Disconnect """
        self.active = False
        if self.client is not None:
            LOGGER.debug("disconnect - stopping loop")
            self.client.disconnect()
            LOGGER.debug("disconnect - disconnected")

    def __connect(self):
        """ Connect """
        LOGGER.debug("__connect - DNS entry %s port %s", self.broker_host, str(self.broker_port))
        #self.client.connect_async(self.broker_host, int(self.broker_port), self.broker_keepalive)
        self.client.connect(self.broker_host, int(self.broker_port), self.broker_keepalive)
        self.client.loop_start()

########## Callbacks ###############################
    def on_connect(self, client, userdata, flags, rc):
        """ Callback triggered when the qclient connects to the broker. """
        del client, userdata, flags
        LOGGER.debug("on_connect - Connected with result code %s", rc)

    def on_socket_close(self, client, sock):
        """ Callback triggered when the socket connection is closed. """
        del sock
        LOGGER.debug("on_socket_close - connection closed from qclient %s.", client._client_id)

    def on_disconnect(self, client, userdata, rc):
        """ Callback triggered when a qclient disconnects. """
        del client, userdata
        LOGGER.debug("on_disconnect - Disconnected with result code %s", rc)
        #self.__reconnect(False)
        #self.client.loop_stop()

    def on_publish(self, client, userdata, message):
        """ Callback triggered when a message is published. """
        del client, userdata
        self.publish_callbacks += 1
        #LOGGER.debug("on_message - Published: %s  /// %s \n", message.topic, message.payload)

########## Getters and setters #####################

    def get_topic(self):
        """ Getter """
        return self.topic

    def set_topic(self, value):
        """ Setter """
        self.topic = str(value)

    def is_active(self):
        """ Getter """
        return self.active

    def get_number_publish_calls(self):
        return self.publish_calls

    def get_number_publish_callbacks(self):
        return self.publish_callbacks
