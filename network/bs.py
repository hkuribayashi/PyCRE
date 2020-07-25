class BS:

    def __init__(self, id_, type_, point):
        self.id = id_
        self.type = type_
        self.point = point
        self.load = 0.0
        self.power = 0.0
        self.tx_gain = 0.0
        self.resouce_blocks = 0.0
        self.hetnet = None

    def increase_bias(self):
        for coluna in map(list, zip(*self.hetnet.network_element)):
            if coluna[0].bs.id == self.id:
                for ne in coluna:
                    ne.biased_sinr += 5.0

    def decrease_bias(self):
        for coluna in map(list, zip(*self.hetnet.network_element)):
            if coluna[0].bs.id != self.id:
                break
            for ne in coluna:
                ne.biased_sinr -= 5.0

    def maintain_bias(self):
        pass

    def __str__(self):
        return 'BS id={}, type={}, load={}'.format(self.id, self.type, self.load)
