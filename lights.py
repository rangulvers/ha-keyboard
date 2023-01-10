import configparser
from midi import Midi
from mqtt import Mqtt
from homeassistant import Homeassistant

config = configparser.ConfigParser()
config.read("config.ini")

mqtt_client = None
midi = None

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config['HASERVER']['Token']}"
}
ha = Homeassistant(headers, config['HASERVER']
                   ['Server'], config['HASERVER']['Endpoint'])


def start_mqtt_server():
    mqtt_client = Mqtt()
    mqtt_client.connect(config['MQTT']['Broker'], int(config['MQTT']['Port']))


def startProgramm():
    midi = Midi()
    midi.connect()

    for msg in midi.get_midi_input():
        if msg.type == "note_on":
            brightness_pct = midi.convert_midi_velocity_to_range(msg.velocity)
            color = midi.convert_midi_note_to_rgb(msg.note)
            print(f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
            ha.change_light(brightness_pct, color)


def main():
    while True:
        print("\n ========== [MAIN MENU] ==========")
        print(' 1. List availabe MIDI Ports')
        print(' 2. List available Lights ')
        print(' 3. Start Programm')
        print(' 8. Start Server')
        print(' 9. Exit')
        userInput = input('\n Enter your selection: ')

        if userInput == '1':
            midi.list_midi_ports()
        elif userInput == '2':
            ha.get_lights()
        elif userInput == '3':
            startProgramm()
        elif userInput == '8':
            start_mqtt_server()
        elif userInput == '9':
            return
        else:
            print('\n Select from Main Menu')


if __name__ == '__main__':
    main()
