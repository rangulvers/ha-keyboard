import paho.mqtt.client as paho
from rich import print


class Mqtt():

    client = None
    topic = 'ha-keyboard'
    server = ''
    port = 1831

    def __init__(self, server, port, topic):
        self.server = server
        self.port = port
        self.topic = topic

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, client, userdata, mid):
        print(f"client: {client} | userdata: {userdata} | mid: {str(mid)}")

    def on_connect(self, client, userdata, flags, rc):
        print('CONNACK received with code %d.' % (rc))

    def send_message(self, data):
        self.client.publish(f'{self.topic}/demoSong', data)

    def connect(self):
        self.client = paho.Client()
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.connect(self.server, self.port)
        self.client.subscribe(f'{self.topic}/#')
        self.client.loop_start()
