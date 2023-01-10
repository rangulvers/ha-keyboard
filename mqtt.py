import paho.mqtt.client as paho


class Mqtt():

    client = None

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

    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def connect(self, broker, port=1883):

        self.client = paho.Client()
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.connect(broker, port)
        self.client.loop_start()
