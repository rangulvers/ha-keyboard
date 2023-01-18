import requests


class Homeassistant():
    """Controller to connect to Homeassistant and controll the lights
    """

    light = None
    headers = None
    server = None
    endpoint = None

    def __init__(self, headers, server, endpoint):
        self.headers = headers
        self.server = server
        self.endpoint = endpoint

    def get_lights(self):
        """get the available lights from the Homeassistant API
        """
        lights = []
        print('\n ========== LIGHTS ========== ')
        response = requests.get(
            f"{self.server}/{self.endpoint}/states",  headers=self.headers)

        entitites = response.json()
        for e in entitites:
            if e['entity_id'].startswith("light") and 'xy' in e['attributes']['supported_color_modes']:
                try:
                    lights.append(
                        [e['entity_id'], e['attributes']['friendly_name']])
                except:
                    pass

        for idx, l in enumerate(lights):
            print(f"{idx}.  {l[1]}")
        print('X.   Cancle')

        sl = input('\n Please select a light : ').upper()

        if sl == "X":
            return
        else:
            self.light = lights[int(sl)][0]
            print(f"\n Selected : {lights[int(sl)][1]} ({self.light}) ")

    def change_light(self, brightness_pct, color):
        """Change the color and brightness of a light

        Args:
            brightness_pct (int): based on midi velocity
            color (RGB): RGB Color Value
        """
        data = {
            "entity_id": self.light,
            "brightness_pct": brightness_pct,
            "rgb_color": color
        }

        # Send the request to call the service
        response = requests.post(
            f"{self.server}/{self.endpoint}/services/light/turn_on", json=data, headers=self.headers)

        # Check the response status code
        if response.status_code != 200:
            print("Error calling service:", response.text)
