'''
Created on Jan 27, 2020

@author: ubuntu
'''
import os
import time
import argparse
from dataprovider.mqtt.qclient import QClient
from dataprovider.logger.log import LOGGER

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_TOPIC = "sample/message"

def generate(topic):
    call_counter = 0
    last_time = time.time()
    qclient = QClient(topic)
    while True:
        message = "Hello Lars Nr {}".format(call_counter)
        qclient.publish(message)
        call_counter += 1
        time.sleep(1)

        if time.time() - last_time > 10.0:
            LOGGER.info("%s: %s messages published - %s messages confirmed",
                        topic,
                        qclient.get_number_publish_calls(),
                        qclient.get_number_publish_callbacks())
            last_time = time.time()

def _init_from_env(topic):
    """ Initialize collector from environment variables """
    env_topic = os.getenv('DATACOLLECTOR_TOPIC')
    if env_topic is None:
        env_topic = topic
    return env_topic

def options():
    """Parse and polish the command-line options """
    """and supply reasonable defaults."""
    arg_parser = argparse.ArgumentParser(description='DataGenerator', usage="%(prog)s [-t <topic>]")
    arg_parser.add_argument('--topic', '-t', default=['sample/message'], nargs=1, help='(Optional) Provide a topic')
    opt = arg_parser.parse_args()
    return opt

def main():
    opt = options()
    topic = _init_from_env(opt.topic[0])
    generate(topic)

if __name__ == '__main__':
    main()
