# https://medium.com/swlh/simulating-a-parallel-queueing-system-with-simpy-6b7fcb6b1ca1

from simpy import *
import random
import numpy as np
from math import log

# maxNumber = 30      # Max number of demands
maxTime = 40000.0     # Runtime limit

timeInBank = 20.0   # Mean time in bank
mu = 1.0 / timeInBank
arrivalMean = 10.0  # Mean of arrival process
lambda_ = 1.0 / arrivalMean

seed = 1        # Seed for simulation
random.seed(seed)

def Customer(env, name, server:Resource, mu):
    arrive = env.now
    times[0].append(arrive)
    print(f"{env.now:.4f} {name}: поступило в систему; очередь: {len(server.put_queue) + len(server.users)} требований")
    
    with server.request() as request:
        # Wait for the server
        yield request
        wait = env.now - arrive
        # We got to the server
        times[1].append(env.now)
        print(f'{env.now:.4f} {name}: находилось в очереди {wait:.4f}')
        tib = -log(random.random()) / mu
        # tib = random.expovariate(mu)
        print(f'--> обслуживание завершится через {tib}')
        yield env.timeout(tib)
        times[2].append(env.now)
        print(f'{env.now:.4f} {name}: обслужилось и вышло из системы')

def Source(env, lambda_, server, mu):
    # for i in range(number):
    i = 0
    while True:
        c = Customer(env, f'Требование {i:02d}', server, mu)
        env.process(c)
        t = -log(random.random()) / lambda_
        i += 1
        # t = random.expovariate(lambda_)
        yield env.timeout(t)

def main():
    # хранение моментов
    # поступления, начало обслуживания, завершение обслуживания
    global times
    times = [[], [], []]

    # Setup and start the simulation
    env = Environment()

    server = Resource(env)
    env.process(Source(env, lambda_, server, mu))
    env.run(until=maxTime)

    # добавить сбор моментов в коллекции
    # анализ моментов
    times[0] = np.array(times[0][:len(times[2])])
    times[1] = np.array(times[1][:len(times[2])])
    times[2] = np.array(times[2])

    # v -- обслуживание, w -- ожидание, u -- пребывание
    v = np.mean(times[2] - times[1]) 
    w = np.mean(times[1] - times[0])
    u = np.mean(times[2] - times[0])

    return v, w, u

v = []
w = []
u = []

# число прогонов
n = 1

for _ in range(n):
    tmp_1, tmp_2, tmp_3 = main()
    v.append(tmp_1)
    w.append(tmp_2)
    u.append(tmp_3)

print(f'\nv = {np.mean(v)}\nw = {np.mean(w)}\nu = {np.mean(u)}')