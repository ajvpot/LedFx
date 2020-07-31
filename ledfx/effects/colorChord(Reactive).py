import random

from ledfx.color import COLORS
from ledfx.effects.audio import AudioReactiveEffect, FREQUENCY_RANGES
from ledfx.effects.gradient import GradientEffect
from ledfx.effects.noteFinder import NoteFinder
import voluptuous as vol
import numpy as np

class ColorChordAudioEffect(AudioReactiveEffect, GradientEffect):
    NAME = "ColorChord"
    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('sensitivity', description='Responsiveness to changes in sound', default = 0.7): vol.All(vol.Coerce(float), vol.Range(min=0.2, max=0.99)),
        vol.Optional('color_lows', description='Color of low, bassy sounds', default = "red"): vol.In(list(COLORS.keys())),
    })

    _nf = None

    def config_updated(self, config):
        #todo: pass sample rate
        self._nf = NoteFinder(48000)
        decay_sensitivity = (self._config["sensitivity"]-0.2)*0.25
        self._p_filter = self.create_filter(
            alpha_decay = decay_sensitivity,
            alpha_rise = self._config["sensitivity"])
        self.lows_colour = np.array(COLORS[self._config['color_lows']], dtype=float)

    def audio_data_updated(self, data):
            if self._nf is not None:
                self._nf.samples_updated(data.audio_sample(True))

            amps = self._nf.get_amplitudes()
            segment_length = int(self.pixel_count/len(amps))
            p = np.zeros(np.shape(self.pixels))
            for freq, amp in amps.items():
                p[int(freq%len(amps))*segment_length:(int(freq%len(amps))+1)*segment_length] += self.lows_colour*amp*20

            self.pixels = self._p_filter.update(p)
