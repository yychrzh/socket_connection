import gym

env = gym.make("Humanoid-v2")

for i in range(1000):
    a = env.action_space.sample()
    [o, r, d, _] = env.step(a)
    if d:
        env.reset()

