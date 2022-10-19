# допилить лог, сверить результаты -- почему расхождение?
# представление результатов -- в каком виде?
# показать сравнение результатов

import random
from math import log
import numpy as np

# описание требования
class Demand:
    def __init__(self, name, born, begin_service = 0, end_service = 0):
        self.name = name
        # момент генерации
        self.born = born
        # момент начала обслуживания
        self.begin_service = begin_service
        # момент окончания обслуживания
        self.end_service = end_service

# ввод параметров
t_modeling = 40000 # время моделирования
# cnt_demands = 30 # число требований
arrival_mean = 10.0
lambda_ = 1.0 / arrival_mean
time_in_bank = 20.0
mu =  1.0 / time_in_bank
random.seed(1)

def main():
    # начальные условия
    t_act_source = 0 # момент генерации требования
    t_act_server = t_modeling + .000001 # момент начала обслуживания
    queue = []
    serviced_demands = 0 # число обслуженных требований
    ind = 0 # номер текущего требования
    times = [0, 0, 0] # v, w, u

    t_now = 0 # текущее время
    server_free = True # индикатор занятости прибора на взлётке

    # процесс симуляция
    while t_now < t_modeling:
        indicator = False # индикатор активности какого-либо процесса
        # генерация требования
        if (t_act_source == t_now):
            queue.append(Demand(f'Требование {ind:02d}', t_now))
            ind += 1
            print(f"{t_now:.4f} {queue[-1].name}: поступило в систему; очередь: {len(queue) - 1} требований")
            indicator = True
            # t_act_source = t_modeling + .0000001 if ind >= cnt_demands else t_now + random.expovariate(lambda_)
            t_act_source = t_now - log(random.random()) / lambda_
        
        # начало обслуживания требования
        if server_free and len(queue) > 0:
            d = queue.pop(0)
            print(f"{t_now:.4f} {d.name}: находилось в очереди {t_now - d.born:.4f}")
            d.begin_service = t_now
            indicator = True
            server_free = False
            # t_act_server = t_now + random.expovariate(mu)
            t_act_server = t_now - log(random.random()) / mu
            print(f'--> обслуживание завершится через {t_act_server - t_now}')
            
        # завершение обслуживания требования
        if (t_act_server == t_now):
            d.end_service = t_now
            print(f"{t_now:.4f} {d.name}: обслужилось и вышло из системы")
            indicator = True
            server_free = True
            t_act_server = t_modeling + .0000001
            serviced_demands += 1
            times[0] += d.end_service - d.begin_service
            times[1] += d.begin_service - d.born
            times[2] += d.end_service - d.born
        
        # переход к следующему моменту
        if not indicator:
            t_now = min(t_act_server, t_act_source)
            # v -- обслуживание, w -- ожидание, u -- пребывание
            tmp = 1 if serviced_demands == 0 else serviced_demands
            w = times[1] / tmp
            v = times[0] / tmp
            u = times[2] / tmp
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