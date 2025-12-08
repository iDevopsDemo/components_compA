import unittest
from unittest.mock import patch, ANY, MagicMock
import paho.mqtt.client as mqtt
from dataprovider.mqtt.qclient import QClient


class PublishTests(unittest.TestCase):

    def setUp(self):
        # Use a MagickMock for the MqttClient
        self.mqtt_client = MagicMock()
        self.mqtt_client.connect.return_value = mqtt.MQTT_ERR_SUCCESS

    @patch('dataprovider.mqtt.qclient.MqttClient')
    def test_publish_withMqttClient_publishesDefaultTopic(self, mqtt_mock):
        # Arrange
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client
        # - Create QClient, which invokes connect
        qclient = QClient()

        # Act
        qclient.publish("message")

        # Assert
        self.mqtt_client.publish.was_called_with(qclient.topic, ANY, ANY)
        self.assertEqual(qclient.get_number_publish_calls(), 1)

    @patch('dataprovider.mqtt.qclient.MqttClient')
    def test_publish_withMqttClient_publischesGivenMessage(self, mqtt_mock):
        message = "message"
        # Arrange
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client
        # - Create QClient, which invokes connect
        qclient = QClient()

        # Act
        qclient.publish(message)

        # Assert
        self.mqtt_client.publish.was_called_with(ANY, message, ANY)
        self.assertEqual(qclient.get_number_publish_calls(), 1)
