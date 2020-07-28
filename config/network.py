from enum import Enum


class Network(Enum):

    DEFAULT = (1000000.0, 20.0, 46.0, 32.0, -174.0, 35.0, 0.0, 5.0, 5.0, 1.0, 12.0, 14.0, 1.0, 80.0, -30.0)

    def __init__(self, simulation_area, bandwidth, mbs_power, sbs_power, noise_power, mbs_height, sbs_height, mbs_gain,
                 sbs_gain, ue_height, number_subcarriers, number_ofdm_symbols, subframe_duration, max_bias, min_bias):

        if simulation_area < 0 or simulation_area is None:
            raise RuntimeError('Incorret value for parameter simulation_area: {}'.format(simulation_area))
        else:
            self._simulation_area = simulation_area

        if mbs_power < 0 or mbs_power is None:
            raise RuntimeError('Incorret value for parameter mbs_power: {}'.format(mbs_power))
        else:
            self._mbs_power = mbs_power

        if sbs_power < 0 or sbs_power is None:
            raise RuntimeError('Incorret value for parameter sbs_power: {}'.format(sbs_power))
        else:
            self._sbs_power = sbs_power

        if bandwidth < 0 or bandwidth is None:
            raise RuntimeError('Incorret value for parameter bandwidth: {}'.format(bandwidth))
        else:
            self._bandwidth = bandwidth

        if noise_power > 0 or noise_power is None:
            raise RuntimeError('Incorret value for parameter noise_power: {}'.format(noise_power))
        else:
            self._noise_power = noise_power

        if mbs_height < 0 or mbs_height is None:
            raise RuntimeError('Incorret value for parameter mbs_height: {}'.format(mbs_height))
        else:
            self._mbs_height = mbs_height

        if sbs_height < 0 or sbs_height is None:
            raise RuntimeError('Incorret value for parameter sbs_height: {}'.format(sbs_height))
        else:
            self._sbs_height = sbs_height

        if ue_height < 0 or ue_height is None:
            raise RuntimeError('Incorret value for parameter ue_height: {}'.format(ue_height))
        else:
            self._ue_height = ue_height

        if mbs_gain < 0 or mbs_gain is None:
            raise RuntimeError('Incorret value for parameter mbs_gain: {}'.format(mbs_gain))
        else:
            self._mbs_gain = mbs_gain

        if sbs_gain < 0 or sbs_gain is None:
            raise RuntimeError('Incorret value for parameter sbs_gain: {}'.format(sbs_gain))
        else:
            self._sbs_gain = sbs_gain

        if number_subcarriers < 0 or number_subcarriers is None:
            raise RuntimeError('Incorret value for parameter number_subcarriers: {}'.format(number_subcarriers))
        else:
            self._number_subcarriers = number_subcarriers

        if number_ofdm_symbols < 0 or number_ofdm_symbols is None:
            raise RuntimeError('Incorret value for parameter number_ofdm_symbols: {}'.format(number_ofdm_symbols))
        else:
            self._number_ofdm_symbols = number_ofdm_symbols

        if subframe_duration < 0 or subframe_duration is None:
            raise RuntimeError(
                'Incorret value for parameter subframe_duration: {}'.format(subframe_duration))
        else:
            self._subframe_duration = subframe_duration

        if max_bias is None:
            raise RuntimeError('Incorret value for parameter max_bias: {}'.format(max_bias))
        else:
            self._max_bias = max_bias

        if min_bias is None:
            raise RuntimeError('Incorret value for parameter min_bias: {}'.format(min_bias))
        else:
            self._min_bias = min_bias

    @property
    def simulation_area(self):
        return self._simulation_area

    @property
    def mbs_power(self):
        return self._mbs_power

    @property
    def sbs_power(self):
        return self._sbs_power

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def sbs_height(self):
        return self._sbs_height

    @property
    def sbs_gain(self):
        return self._sbs_gain

    @property
    def mbs_height(self):
        return self._mbs_height

    @property
    def mbs_gain(self):
        return self._mbs_gain

    @property
    def ue_height(self):
        return self._ue_height

    @property
    def number_subcarriers(self):
        return self._number_subcarriers

    @property
    def number_ofdm_symbols(self):
        return self._number_ofdm_symbols

    @property
    def subframe_duration(self):
        return self._subframe_duration

    @property
    def max_bias(self):
        return self._max_bias

    @property
    def min_bias(self):
        return self._min_bias
