import enum

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_distance(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2 + (self.z - point.z)**2)**(0.5)

    def __str__(self):
        return '[x={}, y={}, z={}]'.format(self.x, self.y, self.z)

class ApplicationProfile(enum.Enum):
    virtual_reality = {'latency': 10.0, 'bandwidth': 100.0, 'compression_factor': 0.6}
    factory_automation = {'latency': 20.0, 'bandwidth': 1.0, 'compression_factor': 0.8}
    data_backup = {'latency': 1000.0, 'bandwidth': 1.0, 'compression_factor': 0.8}
    smart_grid = {'latency': 5.0, 'bandwidth': 0.4, 'compression_factor': 0.03}
    smart_home = {'latency': 60.0, 'bandwidth': 0.001, 'compression_factor': 1.0}
    medical = {'latency': 40.0, 'bandwidth': 0.2, 'compression_factor': 0.2}
    environmental_monitoring = {'latency': 1000.0, 'bandwidth': 1.0, 'compression_factor': 0.1}
    tactile_internet = {'latency': 1.0, 'bandwidth': 120.0, 'compression_factor': 0.8}
