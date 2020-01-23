import numpy as np

from mobilitymodel.basic import ApplicationProfile
from utils.teste import get_hppp
from builtins import RuntimeError

class BS:

    def __init__(self, point, power, tx_gain, rx_gain, tier, online=True, load=0, resource_blocks=100):
        self.power = power
        self.point = point
        self.tx_gain = tx_gain
        self.rx_gain = rx_gain
        self.online = online
        self.load = load
        self.tier = tier
        self.resouce_blocks = resource_blocks
        self.ues = []


class UE:

    def __init__(self, point, profile, bitrate_per_channel=0.0, resource_blocks=0):
        self.point = point
        self.bitrate_per_channel = bitrate_per_channel
        self.resource_blocks = resource_blocks
        self.profile = profile
        self.bs = []


class NetworkElement:

    def __init__(self, ue, bs, sinr, delay, efficiency=0.15, coverage_status=False):
        self.ue = ue
        self.bs = bs
        self.sinr = sinr
        self.delay = delay
        self.efficiency = efficiency
        self.coverage_status = coverage_status


class HetNet:

    def __init__(self, simulation_area, tier_density):
        self.ue = []
        self.bs = []
        self.simulation_area = simulation_area
        self.tier_density = tier_density

        if (len(self.tier_density) < 2):
            raise RuntimeError('HetNet tiers should greater or equal than 2')

        ue_points = get_hppp(self.tier_density['UE'], self.simulation_area, 1.5)
        for point in ue_points:
            profile = np.random.choice(list(ApplicationProfile))
            self.ue.append(UE(point, profile))

        macro_points = get_hppp(self.tier_density['MBS'], self.simulation_area, 30.0)
        for point in macro_points:
            self.bs.append(BS(point, 46.0, 0.0, 0.0, 'MBS'))

        small_points = get_hppp(self.tier_density['SBS-1'], self.simulation_area, 10.0)
        for point in small_points:
            self.bs.append(BS(point, 30.0, 0.0, 0.0, 'SBS-1'))

        small_points = get_hppp(self.tier_density['SBS-2'], self.simulation_area, 1.0)
        for point in small_points:
            self.bs.append(BS(point, 23.0, 0.0, 0.0, 'SBS-2'))


    def print(self):
        print(self.ue[-1].point)
        print(self.bs)

tiers_density = {'UE': 0.000002, 'MBS': 0.000002, 'SBS-1': 0.000002, 'SBS-2': 0.000002}
hn = HetNet(1000000.0, tiers_density)
hn.print()
