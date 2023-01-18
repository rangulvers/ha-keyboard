import traceback
import colorsys
import time
import mido


class Midi():

    """MIDI Class to controll interaction with MIDI ports
        Returns:
            MIDI: MIDI Controller
    """

    midi_port = None
    degrees = 360
    segements = 11  # Pianos have 88 Keys. This splits them up into chunks of 8. ajust the number for more detailed color changes

    def __init__(self) -> None:
        pass

    def connect(self, homeassistant):
        """connect midi controller to midi port

        Args:
            homeassistant (homeassistant): homeassistant object
        """
        for msg in mido.open_input(self.midi_port):
            if msg.type == "note_on":
                brightness_pct = self.midi.convert_midi_velocity_to_range(
                    msg.velocity)
                color = self.midi.convert_midi_note_to_rgb(msg.note)
                print(
                    f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
                homeassistant.change_light(brightness_pct, color)

    def list_midi_ports(self):
        # FIXME : test if this works on RPI
        """list all available midi ports 
        """
        try:
            midiPort = mido.get_input_names()
            for idx, midi in enumerate(midiPort):
                print(f"{idx}.  {midiPort}")
            select_midi_port = input('\n Please select a midi port: ').upper()

            if select_midi_port == "X":
                return
            else:
                self.midi_port = midiPort[int(select_midi_port)][0]
        except Exception as e:
            print(traceback.format_exc(e))

    def convert_midi_note_to_rgb(self, note):
        """Convert the currently played note to an RGB value

        Args:
            note (MIDI NOTE): Note

        Returns:
            int[R,G,B]: RGB Color Value
        """
        # https://www.rapidtables.com/convert/color/rgb-to-hsl.html
        n = self.degrees / self.segements
        rad = round((n*note/self.degrees), 4)

        r, g, b = colorsys.hls_to_rgb(rad, 0.5, 1)

        rgb_color = [round(r*255), round(g*255), round(b*255)]

        return rgb_color

    def convert_midi_velocity_to_range(self, velocity):
        # MIDI Velocity Range 0 - 127 https://www.cs.cmu.edu/~rbd/papers/velocity-icmc2006.pdf
        newVelocity = round((((velocity - 0) * (100 - 0)) /
                            (127 - 0)) + 0)
        return newVelocity

    def play_demo(self, homeassistant, mqtt):

        demo = mido.MidiFile('bells.mid')

        for msg in demo.play():
            if msg.type == "note_on":

                brightness_pct = self.convert_midi_velocity_to_range(
                    msg.velocity)
                color = self.convert_midi_note_to_rgb(msg.note)
                print(
                    f"Vel : {msg.velocity} ==> Bright : {brightness_pct} || Note : {msg.note} ==> Color : {color}")
                homeassistant.change_light(
                    brightness_pct, color)
                mqtt.send_message(int(msg.note))
                time.sleep(0.2)
