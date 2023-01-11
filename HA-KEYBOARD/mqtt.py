import paho.mqtt.client as paho


class Mqtt():

    client = None
    topic = 'ha-keyboard/#'

    def __init__(self) -> None:
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, client, userdata, mid):
        print(f"client: {client} | userdata: {userdata} | mid: {str(mid)}")

    def on_connect(self, client, userdata, flags, rc):
        print('CONNACK received with code %d.' % (rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def send_message(self, data):
        self.client.publish(f'{self.topic}/demoSong', data)

    def connect(self, broker, port=1883):
        self.client = paho.Client()
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.connect(broker, port)
        self.client.subscribe(self.topic)
        self.client.loop_start()
