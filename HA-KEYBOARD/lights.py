import configparser
from midi import Midi
from mqtt import Mqtt
from homeassistant import Homeassistant

config = configparser.ConfigParser()
config.read("config.ini")

mqtt_client = None
midi = Midi()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config['HASERVER']['Token']}"
}
ha = Homeassistant(headers, config['HASERVER']
                   ['Server'], config['HASERVER']['Endpoint'])


def start_mqtt_server():
    mqtt_client = Mqtt()
    mqtt_client.connect(config['MQTT']['Broker'], int(config['MQTT']['Port']))


def main():
    midi.connect()

    for msg in midi.get_midi_input():
        if msg.type == "note_on":
            brightness_pct = midi.convert_midi_velocity_to_range(msg.velocity)
            color = midi.convert_midi_note_to_rgb(msg.note)
            print(f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
            ha.change_light(brightness_pct, color)


def play_demo_song():
    midi.play_demo(ha)

    # mid = mido.MidiFile('bells.mid')
    # brightness_pct = 0

    # print("######## RUNNING DEMO MODE #########")

    # # for x in range(1, 89):
    # #     brightness_pct = 100
    # #     color = convertMidiToRGB(x)
    # #     print(f"Bright : {brightness_pct} || Note : {x} ==> Color : {color}")
    # #     changeLightToHA(brightness_pct, color, light)
    # #     time.sleep(0.2)

    # print("########## PLAYING DEMO SONG ##########")
    # time.sleep(1)
    # for msg in mid.play():
    #     if msg.type == "note_on":
    #         brightness_pct = convertMidiVelocityToRange(msg.velocity)
    #         color = convertMidiToRGB(msg.note)
    #         print(
    #             f"Vel : {msg.velocity} ==> Bright : {brightness_pct} || Note : {msg.note} ==> Color : {color}")
    #         changeLightToHA(brightness_pct, color, light)

    #     time.sleep(0.2)


def main():
    while True:
        print("\n ========== [MAIN MENU] ==========")
        print(' 1. List availabe MIDI Ports')
        print(' 2. List available Lights ')
        print(' 3. Start Programm')
        print(' 8. Connect MQTT')
        print(' 0. Play Demo Song')
        print(' X. Exit')
        userInput = input('\n Enter your selection: ').upper()

        if userInput == '1':
            midi.list_midi_ports()
        elif userInput == '2':
            ha.get_lights()
        elif userInput == '3':
            main()
        elif userInput == '8':
            start_mqtt_server()
        elif userInput == '0':
            play_demo_song()
        elif userInput == '9':
            return
        else:
            print('\n Select from Main Menu')


if __name__ == '__main__':
    main()