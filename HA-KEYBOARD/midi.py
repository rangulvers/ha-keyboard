import mido
import traceback
import colorsys


class Midi():

    midi_port = None
    midi_input = None
    degrees = 360
    segements = 80

    def __init__(self) -> None:
        pass

    def get_midi_input(self):
        return self.midi_input

    def connect(self):
        self.midi_input = mido.open_input(self.midi_port)

    def list_midi_ports(self):
        try:
            midiPort = mido.get_input_names()
            for idx, midi in enumerate(midiPort):
                print(f"{idx}.  {midiPort}")

        except Exception as e:
            print(traceback.format_exc())

    def convert_midi_note_to_rgb(self, note):
        n = self.degrees / self.segements
        rad = round((n*note/self.degrees), 4)

        r, g, b = colorsys.hls_to_rgb(rad, 0.5, 1)

        rgb_color = [round(r*255), round(g*255), round(b*255)]

        return rgb_color

    def convert_midi_velocity_to_range(self, velocity):
        newVelocity = round((((velocity - 0) * (100 - 0)) /
                            (127 - 0)) + 0)
        return newVelocity

    def play_demo(self, homeassistant):
        import time

        demo = mido.MidiFile('bells.mid')

        for msg in demo.play():
            if msg.type == "note_on":
                brightness_pct = self.convert_midi_velocity_to_range(
                    msg.velocity)
                color = self.convert_midi_note_to_rgb(msg.note)
                print(
                    f"Vel : {msg.velocity} ==> Bright : {brightness_pct} || Note : {msg.note} ==> Color : {color}")
                homeassistant.change_light(
                    brightness_pct, color, homeassistant.light)

                time.sleep(0.2)
        pass
