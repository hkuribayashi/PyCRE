import enum
import numpy as np

from builtins import RuntimeError
from mobilitymodel.basic import get_hppp


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
        self.ne = []


class ApplicationProfile(enum.Enum):
    virtual_reality = {'latency': 10.0, 'bandwidth': 100.0, 'compression_factor': 0.6}
    factory_automation = {'latency': 20.0, 'bandwidth': 1.0, 'compression_factor': 0.8}
    data_backup = {'latency': 1000.0, 'bandwidth': 1.0, 'compression_factor': 0.8}
    smart_grid = {'latency': 5.0, 'bandwidth': 0.4, 'compression_factor': 0.03}
    smart_home = {'latency': 60.0, 'bandwidth': 0.001, 'compression_factor': 1.0}
    medical = {'latency': 40.0, 'bandwidth': 0.2, 'compression_factor': 0.2}
    environmental_monitoring = {'latency': 1000.0, 'bandwidth': 1.0, 'compression_factor': 0.1}
    tactile_internet = {'latency': 1.0, 'bandwidth': 120.0, 'compression_factor': 0.8}


class UE:

    def __init__(self, point, profile, bitrate_per_channel=0.0, resource_blocks=0):
        self.point = point
        self.bitrate_per_channel = bitrate_per_channel
        self.resource_blocks = resource_blocks
        self.profile = profile
        self.ne = []


class NetworkElement:

    def __init__(self, ue, bs, distance=0.0, sinr=0.0, delay=0.0, efficiency=0.15, coverage_status=False):
        self.ue = ue
        self.bs = bs
        self.sinr = sinr
        self.distance = distance
        self.delay = delay
        self.efficiency = efficiency
        self.coverage_status = coverage_status
        self.distance = distance


class HetNet:

    def __init__(self, simulation_area, tier_density):
        self.ue = []
        self.bs = []
        self.simulation_area = simulation_area
        self.tier_density = tier_density

        if len(self.tier_density) != 4:
            raise RuntimeError('HetNet tiers should be equal 4')

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

        for u in self.ue:
            for b in self.bs:
                n = NetworkElement(u, b)
                n.distance = u.point.get_distance(b.point)
                u.ne.append(n)
                b.ne.append(u)

    def __str__(self):
        return 'HetNet '
