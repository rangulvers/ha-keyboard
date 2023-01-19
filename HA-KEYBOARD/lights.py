import configparser
import typer
from rich import print
from midi import Midi
from mqtt import Mqtt
from homeassistant import Homeassistant

config = configparser.ConfigParser()
config.read("config.ini")

mqtt_client = Mqtt(config['MQTT']['Broker'],
                   int(config['MQTT']['Port']),
                   config['MQTT']['Topic']
                   )
midi = Midi()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config['HASERVER']['Token']}"
}
ha = Homeassistant(headers, config['HASERVER']
                   ['Server'], config['HASERVER']['Endpoint'])


def start_mqtt_server():
    """Start the MQTT Server and connect to the broker defined in the config.ini file
    """
    mqtt_client.connect()


def live_keyboard():
    """listen to the live played notes from the connected keyboard
    """
    midi.connect(ha)


def play_demo_song():
    midi.play_demo(ha, mqtt_client)


def main():
    while True:
        print("\n ========== [MAIN MENU] ==========")
        print(' 1. List availabe MIDI Ports')
        print(' 2. List available Lights ')
        print(' 3. Start Programm')
        print(' 8. Connect MQTT')
        print(' 0. Play Demo Song')
        print(' X. Exit')
        userInput = typer.prompt('Enter your selection: ').upper()

        if userInput == '1':
            midi.list_midi_ports()
        elif userInput == '2':
            ha.get_lights()
        elif userInput == '3':
            live_keyboard()
        elif userInput == '8':
            start_mqtt_server()
        elif userInput == '0':
            play_demo_song()
        elif userInput == '9':
            return
        else:
            print('Select from Main Menu')


if __name__ == '__main__':
    typer.run(main)
