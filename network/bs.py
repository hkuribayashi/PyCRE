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

    def __change_bias(self, bias):
        for coluna in map(list, zip(*self.hetnet.network_element)):
            if coluna[0].bs.id == self.id:
                for ne in coluna:
                    if bias > 0:
                        threshold = self.hetnet.env.max_bias
                    else:
                        threshold = self.hetnet.env.min_bias
                    if abs(ne.sinr - ne.biased_sinr) < abs(threshold):
                        ne.biased_sinr += bias

    def decrease_bias(self):
        self.__change_bias(-10.0)

    def increase_bias(self):
        self.__change_bias(20.0)

    def maintain_bias(self):
        pass

    def __str__(self):
        return 'BS id={}, type={}, load={}'.format(self.id, self.type, self.load)
