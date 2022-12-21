import argparse
import requests
import mido
import time
import logging
import traceback

server = "http://192.168.2.136:8123"
endpoint = "api"

# Set up the authentication headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmMTZiN2VhNGM4ZWU0NDM2OTU0Mjg0ZDdmOWRmNmM5YSIsImlhdCI6MTY3MTUzODEyNiwiZXhwIjoxOTg2ODk4MTI2fQ.T3YJ-KGTN6BOp0VR0_3rQ5ILgW0NsA3XKZH0hF60GVs"
}

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) /
#             (OldMax - OldMin)) + NewMin


def convertMidiToRGB(note):
    if note in range(1, 11):
        rgb_color = [192, 57, 43]
    if note in range(11, 20):
        rgb_color = [155, 89, 182]
    if note in range(20, 30):
        rgb_color = [41, 128, 185]
    if note in range(30, 40):
        rgb_color = [26, 188, 156]
    if note in range(40, 50):
        rgb_color = [39, 174, 96]
    if note in range(50, 60):
        rgb_color = [241, 196, 15]
    if note in range(60, 70):
        rgb_color = [243, 156, 18]
    if note in range(70, 90):
        rgb_color = [211, 84, 0]
    return rgb_color


def convertMidiVelocityToRange(velocity):
    newVelocity = round((((velocity - 0) * (100 - 0)) /
                         (127 - 0)) + 0)
    return newVelocity


def changeLightToHA(brightness_pct, color, light):
    data = {
        "entity_id": light,
        "brightness_pct": brightness_pct,
        "rgb_color": color
    }

    # Send the request to call the service
    response = requests.post(
        f"{server}/{endpoint}/services/light/turn_on", json=data, headers=headers)
    # print(response)
    # Check the response status code
    if response.status_code != 200:
        print("Error calling service:", response.text)

# Main Loop to listen to MIDI Input from Keyboard


def main(midiPort, light):
    midiInput = mido.open_input(midiPort)
    for msg in midiInput:
        if msg.type == "note_on":
            brightness_pct = convertMidiVelocityToRange(msg.velocity)
            color = convertMidiToRGB(msg.note)
            print(f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
            changeLightToHA(brightness_pct, color, light)

# Play Demo File


def playDemo(light):
    mid = mido.MidiFile('bells.mid')
    brightness_pct = 0

    for msg in mid.play():
        if msg.type == "note_on":
            brightness_pct = convertMidiVelocityToRange(msg.velocity)
            color = convertMidiToRGB(msg.note)
            print(
                f"Vel : {msg.velocity} ==> Bright : {brightness_pct} || Note : {msg.note} ==> Color : {color}")
            changeLightToHA(brightness_pct, color, light)

        time.sleep(0.2)

# List Midi Input Ports


def listPorts():
    try:
        midiPort = mido.get_input_names()
        print(midiPort)
    except Exception as e:
        logging.error(traceback.format_exc())


def runDebug(midiPort):
    logging.basicConfig(format='%(levelname)s%:%(message)s', level=logging.DEBUG)
    logging.info("####STARTING DEBUG####")
    midiInput = mido.open_input(midiPort)
    for msg in midiInput:
        logging.debug(msg)
        #if msg.type == "note_on":
        #    brightness_pct = convertMidiVelocityToRange(msg.velocity)
        #    color = convertMidiToRGB(msg.note)
        #    print(f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
        #    changeLightToHA(brightness_pct, color, light)

    # Main entry Point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--midi",
        dest="midi"
    )

    parser.add_argument(
        "--light",
        dest="light",
        nargs="?",
        type=str,
        const="light.extended_color_light_9",  # Poster Basement,
        default="light.extended_color_light_9"
    )
    parser.add_argument(
        "--ports",
        dest="ports",
        action="store_true"
    )
    parser.add_argument(
        "--demo",
        dest="demo",
        action="store_true"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true"
    )
    args = parser.parse_args()

    if args.ports:
        listPorts()
    elif args.midi:
        main(args.midi, args.light)
    elif args.demo:
        playDemo(args.light)
    elif args.debug:
        runDebug(args.midi)
    else:
        parser.print_help()
