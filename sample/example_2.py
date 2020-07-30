import numpy as np

from config.network import Network
from mobility.basic import Point
from network.bs import BS
from network.hetnet import HetNet
from network.ue import UE

h = HetNet(Network.DEFAULT)

# Deploy a MBS
p1 = Point(0.0, 0.0, 35.0)
mbs = BS(1, 'MBS', p1)

# Deploy a SBS
p2 = Point(50.0, 50.0, 5.0)
sbs_1 = BS(2, 'SBS', p2)

# Add each BS in the Hetnet
h.add_bs(mbs)
h.add_bs(sbs_1)

# Deploy 20 UEs
for i in range(10):
    x = np.random.randint(-60, 60)
    y = np.random.randint(-60, 60)
    p_i = Point(x, y, 1.0)
    ue = UE(i, p_i)
    h.add_ue(ue)

h.run()
h.debug()

# Passo 1: SINR 5 Usuários (linha) x 2 BS (colunas)
# Passo 2: User Association
# Passo 3: BS Load: MBS = 9, SBS = 1
# Passo 4: RBs: MBS (100) = 100/9 = 10, SBS (100) = 100/1
# Passo 5: Datarate Data-rate (Qtd de RBs de cada UE, SINR, Modulação)

sbs_1.increase_bias(20.0)
h.run()
h.debug()

sbs_1.increase_bias(20.0)
h.run()
h.debug()
