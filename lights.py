import os
import requests
import pprint
import mido
import traceback

running_main_loop = True
server = "http://192.168.2.136:8123"
endpoint = "api"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmMTZiN2VhNGM4ZWU0NDM2OTU0Mjg0ZDdmOWRmNmM5YSIsImlhdCI6MTY3MTUzODEyNiwiZXhwIjoxOTg2ODk4MTI2fQ.T3YJ-KGTN6BOp0VR0_3rQ5ILgW0NsA3XKZH0hF60GVs"
}
selectedLight = ''
slectedMidi = ''


def listMidiPorts():
    try:
        midiPort = mido.get_input_names()
        for idx, midi in enumerate(midiPort):
            print(f"{idx}.  {midiPort}")

    except Exception as e:
        print(traceback.format_exc())


def listHaLights():
    lights = []
    print('\n ========== LIGHTS ========== ')
    response = requests.get(
        f"{server}/{endpoint}/states",  headers=headers)

    entitites = response.json()
    for e in entitites:
        if e['entity_id'].startswith("light") and 'xy' in e['attributes']['supported_color_modes']:
            lights.append(e['entity_id'])
    for idx, l in enumerate(lights):
        print(f"{idx}.  {l}")
    print('X.   Cancle')

    sl = input('\n Please select a light : ').upper()

    if sl == "X":
        return
    else:
        selectedLight = lights[int(sl)]
        print(f"\n Selected : {selectedLight}")


def convertMidiToRGB(note):

    n = degrees / segments
    rad = round((n*note/degrees), 4)

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

    # Check the response status code
    if response.status_code != 200:
        print("Error calling service:", response.text)


def startProgramm():
    midiInput = mido.open_input(slectedMidi)
    for msg in midiInput:
        if msg.type == "note_on":
            brightness_pct = convertMidiVelocityToRange(msg.velocity)
            color = convertMidiToRGB(msg.note)
            print(f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
            changeLightToHA(brightness_pct, color, selectedLight)


def main():
    while running_main_loop:
        print("\n ========== [MAIN MENU] ==========")
        print(' 1. List availabe MIDI Ports')
        print(' 2. List available Lights ')
        print(' 3. Start Programm')
        print(' 9. Exit')
        userInput = input('\n Enter your selection: ')

        if userInput == '1':
            listMidiPorts()
        elif userInput == '2':
            listHaLights()
        elif userInput == '3':
            startProgramm()
        elif userInput == '9':
            return
        else:
            print('\n Select from Main Menu')


if __name__ == '__main__':
    main()
