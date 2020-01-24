from entities.hetnet import HetNet


tiers_density = {'UE': 0.000002, 'MBS': 0.000002, 'SBS-1': 0.000002, 'SBS-2': 0.000002}
hn = HetNet(1000000.0, tiers_density)

print(hn.ue[0].profile.value['latency'])
