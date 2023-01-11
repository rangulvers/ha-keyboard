import mido
import traceback
import colorsys


class Midi():

    midi_port = None
    degrees = 360
    segements = 11  # Pianos have 88 Keys. This splits them up into chunks of 8. ajust the number for more detailed color changes

    def __init__(self) -> None:
        pass

    def connect(self, homeassistant):
        for msg in mido.open_input(self.midi_port):
            if msg.type == "note_on":
                brightness_pct = self.midi.convert_midi_velocity_to_range(
                    msg.velocity)
                color = self.midi.convert_midi_note_to_rgb(msg.note)
                print(
                    f"{msg.velocity} ==> {brightness_pct} | {msg.note} ==> {color}")
                homeassistant.change_light(brightness_pct, color)

    def list_midi_ports(self):
        try:
            midiPort = mido.get_input_names()
            for idx, midi in enumerate(midiPort):
                print(f"{idx}.  {midiPort}")

        except Exception as e:
            print(traceback.format_exc())

    def convert_midi_note_to_rgb(self, note):
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
        import time
        demo = mido.MidiFile('bells.mid')

        for msg in demo.play():
            if msg.type == "note_on":
                mqtt.publish(msg)
                brightness_pct = self.convert_midi_velocity_to_range(
                    msg.velocity)
                color = self.convert_midi_note_to_rgb(msg.note)
                print(
                    f"Vel : {msg.velocity} ==> Bright : {brightness_pct} || Note : {msg.note} ==> Color : {color}")
                homeassistant.change_light(
                    brightness_pct, color)

                time.sleep(0.2)
