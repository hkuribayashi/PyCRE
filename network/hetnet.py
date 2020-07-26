import math
from operator import attrgetter

import numpy as np

from network.ne import NetworkElement
from utils.charts import get_visual
from utils.misc import get_pathloss, get_efficiency


class HetNet:

    flag = False

    def __init__(self, env):
        self.list_ue = list()
        self.list_bs = list()
        self.network_element = list()
        self.env = env
        self.evaluation = dict(satisfaction=0.0, sumrate=0.0, medianrate=0.0)

    def add_bs(self, bs):
        if bs.type == 'MBS':
            bs.power = self.env.mbs_power
            bs.tx_gain = self.env.mbs_gain
        else:
            bs.power = self.env.sbs_power
            bs.tx_gain = self.env.sbs_gain
        bs.resouce_blocks = 100
        bs.hetnet = self
        self.list_bs.append(bs)

    def add_ue(self, ue):
        self.list_ue.append(ue)

    def __get_ne(self):
        for ue in self.list_ue:
            linha_network_element = list()
            for bs in self.list_bs:
                linha_network_element.append(NetworkElement(ue, bs))
            self.network_element.append(linha_network_element)

    def run(self):

        # Constructs the NetworkElement structure only once
        if HetNet.flag is False:
            self.__get_ne()
            HetNet.flag = True

            # Compute SINR
            self.__get_sinr()

        else:
            self.__reset()

        # Compute UE x BS Association
        self.__get_association()

        # Compute Radio Resource Allocation
        self.__get_resource_allocation()

        # Compute UE Data Rate
        self.__get_ue_datarate()

        # Compute Performance Evaluation
        self.__get_metrics()

    def __get_sinr(self):
        bw = self.env.bandwidth * (10**6)
        sigma = (10.0 ** (-3.0)) * (10.0 ** (self.env.noise_power / 10.0))
        total_thermal_noise = bw * sigma

        for linha in self.network_element:
            for element in linha:
                element.sinr = element.bs.power - get_pathloss(element.bs.type, element.distance, element.bs.tx_gain)
                element.sinr = (10 ** (-3.0)) * (10 ** (element.sinr/10.0))
                other_elements = [x for x in linha if x != element]
                interference = 0.0
                for o_element in other_elements:
                    o_element_i = o_element.bs.power - get_pathloss(o_element.bs.type, o_element.distance, o_element.bs.tx_gain)
                    interference += ((10 ** (-3.0)) * (10 ** (o_element_i/10.0)))
                element.sinr = element.sinr/(interference + total_thermal_noise)
                element.sinr = 10.0 * np.log10(element.sinr)
                element.biased_sinr = element.sinr

    def __get_association(self):
        for linha in self.network_element:
            ne = max(linha, key=attrgetter('biased_sinr'))
            ne.coverage_status = True

    def __get_resource_allocation(self):
        for coluna in map(list, zip(*self.network_element)):
            output = [element for element in coluna if element.coverage_status is True]
            bs_load = len(output)
            if bs_load > 0:
                output[0].bs.load = bs_load
                rbs_per_ue = math.floor(output[0].bs.resouce_blocks / bs_load)
                for element in output:
                    element.ue.resource_blocks = rbs_per_ue

    def __get_ue_datarate(self):
        bitrate = self.env.number_subcarriers * self.env.number_ofdm_symbols
        for linha in self.network_element:
            ne = [element for element in linha if element.coverage_status is True]
            sinr = ne[0].sinr
            efficiency = get_efficiency(sinr)
            rbs = ne[0].ue.resource_blocks
            bitrate_ue = (rbs * efficiency * bitrate)/self.env.subframe_duration
            bitrate_ue = (bitrate_ue * 1000.0)/1000000.0
            ne[0].ue.datarate = bitrate_ue

    def __get_metrics(self):
        satisfaction = 0.0
        sumrate = 0.0
        datarates = np.zeros(len(self.list_ue))
        for index, ue in enumerate(self.list_ue):
            if ue.evaluation:
                satisfaction = satisfaction + 1
            datarates[index] = ue.datarate
            sumrate += ue.datarate
        self.evaluation['satisfaction'] = (satisfaction/len(self.list_ue)) * 100
        self.evaluation['medianrate'] = np.median(datarates)
        self.evaluation['sumrate'] = sumrate

    def __reset(self):
        for linha in self.network_element:
            for ne in linha:
                ne.coverage_status = False
                ne.ue.resource_blocks = 0.0
                ne.bs.load = 0.0
                ne.ue.evaluation = False

    def debug(self):
        get_visual(self)
        print(self.evaluation)
