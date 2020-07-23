class BS:

    def __init__(self, id_, type_, point):
        self.id = id_
        self.type = type_
        self.point = point
        self.load = 0.0
        self.power = 0.0
        self.tx_gain = 0.0
        self.resouce_blocks = 0.0

    def __str__(self):
        return 'BS id={}, type={}, load={}'.format(self.id, self.type, self.load)
