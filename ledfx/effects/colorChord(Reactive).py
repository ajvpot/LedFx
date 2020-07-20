from ledfx.effects.audio import AudioReactiveEffect, FREQUENCY_RANGES
from ledfx.effects.gradient import GradientEffect
from ledfx.effects.noteFinder import NoteFinder
import voluptuous as vol
import numpy as np

class ColorChordAudioEffect(AudioReactiveEffect, GradientEffect):
    NAME = "ColorChord"
    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('frequency_range', description='Frequency range for the beat detection', default = 'bass'): vol.In(list(FREQUENCY_RANGES.keys())),
    })

    _nf = None

    def config_updated(self, config):
        #todo: pass sample rate
        self._nf = NoteFinder(44100)
        self._frequency_range = np.linspace(
            FREQUENCY_RANGES[self.config['frequency_range']].min,
            FREQUENCY_RANGES[self.config['frequency_range']].max,
            20)

    def audio_data_updated(self, data):
        if True or self._nf is not None:
            self._nf.samples_updated(data.audio_sample(True))

        # Grab the filtered and interpolated melbank data
        magnitude = np.max(data.sample_melbank(list(self._frequency_range)))
        # if magnitude > 0.7:
        #     self.pixels = self.apply_gradient(1.0)
        # else:
        #     self.pixels = self.apply_gradient(0.0)
        if magnitude > 1.0:
            magnitude = 1.0
        self.pixels = self.apply_gradient(magnitude)