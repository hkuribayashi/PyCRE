from gym.envs.registration import register

register(
    id='pycre-v0',
    entry_point='gym_pycre.envs:PyCREEnv',
)
