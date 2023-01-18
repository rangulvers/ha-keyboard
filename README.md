# ha-keyboard

With this progrmam you can connect to any MIDI e.g digital piano and interact with the played notes.

Start the application by running

````console
    python lights.py
````

## Commands

````console
========== [MAIN MENU] ==========

1. List available MIDI Ports
2. List available Lights
3. Start Program
8. Connect MQTT
0. Play Demo Song
X. EXIT

````

### 1. List available MIDI Ports
This will list all available MIDI Ports connect to the device

Output

````console
0.  ['Midi Through:Midi Through Port-0 14:0', 'Midi Through:Midi Through Port-0 14:0']
1.  ['Midi Through:Midi Through Port-0 14:0', 'Midi Through:Midi Through Port-0 14:0']
````

### 2. List available Lights
This will list all available lights available in homeassistant that are capable to change their RGB value. 
You must select on of the lights in order to run the program

### 3. Start Program
This will start the program and will listen to any MIDI input coming from the the MIDI port and change the selected light RGB and brightness value

### 8. Connect MQTT
This will start a MQTT connection to the defined MQTT Broker in the ````config.ini````and broadcast the played note to the MQTT broker

### 0. Play Demo Song
This will play a demo song and change the lights based on the MIDI input from the song

### X. Exit
Exit program

## Config.ini

````ini
[MQTT]
Broker = broker.mqttdashboard.com
Port = 1883
Topic = {MQTT TOPIC} #default ha-keyboard

[HASERVER]
Server = {Homeassistant Server IP}
Endpoint = api
Token = {API TOKEN} # Setup token under your user profile setings

````
