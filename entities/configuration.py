class Configuration:

    def __init__(self, simulation_area=1000000.0, user_density=0.000002, macro_density=0.000002, pico_density=0.000002,
                 femto_density=0.000002, bandwidth=20.0, macro_power=46.0, pico_power=30.0, femto_power=23.0,
                 noise_power=-174.0, macro_height=35.0, macro_gain=15.0, pico_gain=5.0, femto_gain=5.0,
                 number_subcarriers=12, number_ofdm_symbols=14, subframe_duration=1.0):
        self._simulation_area = simulation_area
        self._user_density = user_density
        self._macro_density = macro_density
        self._pico_density = pico_density
        self._femto_density = femto_density
        self._macro_power = macro_power
        self._pico_power = pico_power
        self._femto_power = femto_power
        self._bandwidth = bandwidth
        self._noise_power = noise_power
        self._macro_height = macro_height
        self._macro_gain = macro_gain
        self._pico_gain = pico_gain
        self._femto_gain = femto_gain
        self._number_subcarriers = number_subcarriers
        self._number_ofdm_symbols = number_ofdm_symbols
        self._subframe_duration = subframe_duration

    @property
    def simulation_area(self):
        return self._simulation_area

    @property
    def user_density(self):
        return self._user_density

    @property
    def macro_density(self):
        return self._macro_density

    @property
    def pico_density(self):
        return self._pico_density

    @property
    def femto_density(self):
        return self._femto_density

    @property
    def macro_power(self):
        return self._macro_power

    @property
    def pico_power(self):
        return self._pico_power

    @property
    def femto_power(self):
        return self._femto_power

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def macro_height(self):
        return self._macro_height

    @property
    def macro_gain(self):
        return self._macro_gain

    @property
    def pico_gain(self):
        return self._pico_gain

    @property
    def femto_gain(self):
        return self._femto_gain

    @property
    def number_subcarriers(self):
        return self._number_subcarriers

    @property
    def number_ofdm_symbols(self):
        return self._number_ofdm_symbols

    @property
    def subframe_duration(self):
        return self._subframe_duration

    @simulation_area.setter
    def simulation_area(self, simulation_area):
        if simulation_area < 0:
            raise RuntimeError('[ERROR]: The simulation_area parameter should be a positive value')

    @user_density.setter
    def user_density(self, user_density):
        if user_density < 0:
            raise RuntimeError('[ERROR]: The user_density parameter should be a positive value')
        else:
            self._user_density = user_density

    @macro_density.setter
    def macro_density(self, macro_density):
        if (macro_density < 0):
            raise RuntimeError('[ERROR]: The macro_density parameter should be a positive value')
        else: self._macro_density = macro_density

    @pico_density.setter
    def pico_density(self, pico_density):
        if pico_density < 0:
            raise RuntimeError('[ERROR]: The pico_density parameter should be a positive value')
        else: self._pico_density = pico_density

    @femto_density.setter
    def femto_density(self, femto_density):
        if femto_density < 0:
            raise RuntimeError('[ERROR]: The femto_density parameter should be a positive value')
        else: self._femto_density = femto_density

    @macro_power.setter
    def macro_power(self, macro_power):
        if macro_power < 0:
            raise RuntimeError('[ERROR]: The macro_power parameter should be a positive value')
        else: self._macro_power = macro_power

    @pico_power.setter
    def pico_power(self, pico_power):
        if pico_power < 0:
            raise RuntimeError('[ERROR]: The pico_power parameter should be a positive value')
        else: self._pico_power = pico_power

    @femto_power.setter
    def femto_power(self, femto_power):
        if femto_power < 0:
            raise RuntimeError('[ERROR]: The femto_power parameter should be a positive value')
        else: self._femto_power = femto_power

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        if bandwidth < 0:
            raise RuntimeError('[ERROR]: The bandwidth parameter should be a positive value')
        else: self._bandwidth = bandwidth

    @noise_power.setter
    def noise_power(self, noise_power):
        if noise_power < 0:
            raise RuntimeError('[ERROR]: The noise_power parameter should be a positive value')
        else: self._noise_power = noise_power

    @macro_height.setter
    def macro_height(self, macro_height):
        if macro_height < 0:
            raise RuntimeError('[ERROR]: The macro_height parameter should be a positive value')
        else: self._macro_height = macro_height

    @macro_gain.setter
    def macro_gain(self, macro_gain):
        if macro_gain < 0:
            raise RuntimeError('[ERROR]: The macro_gain parameter should be a positive value')
        else: self._macro_gain = macro_gain

    @pico_gain.setter
    def pico_gain(self, pico_gain):
        if pico_gain < 0:
            raise RuntimeError('[ERROR]: The pico_gain parameter should be a positive value')
        else: self._pico_gain = pico_gain

    @femto_gain.setter
    def femto_gain(self, femto_gain):
        if femto_gain < 0:
            raise RuntimeError('[ERROR]: The femto_gain parameter should be a positive value')
        else: self._femto_gain = femto_gain

    @number_subcarriers.setter
    def number_subcarriers(self, number_subcarriers):
        if number_subcarriers < 0:
            raise RuntimeError('[ERROR]: The number_subcarriers parameter should be a positive value')
        else: self._number_subcarriers = number_subcarriers

    @number_ofdm_symbols.setter
    def number_ofdm_symbols(self, number_ofdm_symbols):
        if number_ofdm_symbols < 0:
            raise RuntimeError('[ERROR]: The number_ofdm_symbols parameter should be a positive value')
        else: self._number_ofdm_symbols = number_ofdm_symbols

    @subframe_duration.setter
    def subframe_duration(self, subframe_duration):
        if subframe_duration < 0:
            raise RuntimeError('[ERROR]: The subframe_duration parameter should be a positive value')
        else: self._subframe_duration = subframe_duration

    def __str__(self) -> str:
        return 'A'


c = Configuration(0.01)
print(c)

