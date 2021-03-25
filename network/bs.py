class BS:

    def __init__(self, id_, type_, point):
        self.id = id_
        self.type = type_
        self.point = point
        self.load = 0.0
        self.max_load = 0.0
        self.power = 0.0
        self.tx_gain = 0.0
        self.resouce_blocks = 100
        self.hetnet = None

    def increase_bias(self, bias):
        for coluna in map(list, zip(*self.hetnet.network_element)):
            if coluna[0].bs.id == self.id:
                # print('Increasing Bias')
                for ne in coluna:
                    # print('SINR: {}'.format(ne.sinr))
                    # print('Current Biased SINR: {}'.format(ne.biased_sinr))
                    if abs(ne.sinr - ne.biased_sinr) < self.hetnet.env.max_bias:
                        ne.biased_sinr += bias
                        # print('New Biased SINR: {}'.format(ne.biased_sinr))
                    # else:
                        # print('Limite Maximo')
                        # print('New Bias: {}'.format(ne.biased_sinr))
                    # print()

    def decrease_bias(self, bias):
        for coluna in map(list, zip(*self.hetnet.network_element)):
            if coluna[0].bs.id == self.id:
                # print('Decreasing Bias')
                for ne in coluna:
                    # print('SINR: {}'.format(ne.sinr))
                    # print('Current Biased SINR: {}'.format(ne.biased_sinr))
                    if abs(ne.sinr - ne.biased_sinr) < abs(self.hetnet.env.min_bias):
                        ne.biased_sinr += bias
                        # print('New Biased SINR: {}'.format(ne.biased_sinr))
                    # else:
                        # print('Limite Minimo')
                        # print('New Bias: {}'.format(ne.biased_sinr))
                    # print()

    def maintain_bias(self):
        pass

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        return 'BS id={}, type={}, load={}'.format(self.id, self.type, self.load)
