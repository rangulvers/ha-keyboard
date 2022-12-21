import argparse
import requests
import mido
import time
import logging
import traceback
import colorsys

server = "http://192.168.2.136:8123"
endpoint = "api"

# Set up the authentication headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmMTZiN2VhNGM4ZWU0NDM2OTU0Mjg0ZDdmOWRmNmM5YSIsImlhdCI6MTY3MTUzODEyNiwiZXhwIjoxOTg2ODk4MTI2fQ.T3YJ-KGTN6BOp0VR0_3rQ5ILgW0NsA3XKZH0hF60GVs"
}

degrees = 360
segments = 11

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) /
#             (OldMax - OldMin)) + NewMin


def convertMidiToRGB(note):

    n = degrees / segments
    rad = round((n*note/degrees), 4)

#    rrad = round(rad/360,4)

    r, g, b = colorsys.hls_to_rgb(rad, 0.5, 1)

    rgb_color = [round(r*255), round(g*255), round(b*255)]

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

    print("######## RUNNING DEMO MODE #########")
    for x in range(1, 89):
        brightness_pct = 100
        color = convertMidiToRGB(x)
        print(f"Bright : {brightness_pct} || Note : {x} ==> Color : {color}")
        changeLightToHA(brightness_pct, color, light)
        time.sleep(0.2)

    print("########## PLAYING DEMO SONG ##########")
    time.sleep(1)
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
    print("############### DEBUG")
    midiInput = mido.open_input(midiPort)
    for msg in midiInput:
        if msg.type == "note_on":
            print("--------")
            print(msg)

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
    elif args.debug:
        runDebug(args.midi)
    elif args.midi:
        main(args.midi, args.light)
    elif args.demo:
        playDemo(args.light)
    else:
        parser.print_help()
