# Анализ однородных открытых экспоненциальных сетей

import numpy as np
import matplotlib.pyplot as plt
import math


def expected_n(lmbd, mu):
    return lmbd / (mu - lmbd)

def expected_u(lmbd, mu):
    return 1 / (mu - lmbd)

def stationary_distribution(omega, theta, eps):
    while np.linalg.norm(omega.dot(theta) - omega) > eps:
        omega = omega.dot(theta)
    return omega

def get_lmbds(lmbd_0, omega):
    ans = [lmbd_0 * omega[1] / omega[0]]
    for i in range(2, L + 1):
        ans.append(lmbd_0 * omega[i] / omega[0])
    return ans

def get_psi(lmbds, kappa, mu):
    psi = np.zeros(L)
    for i in range(L):
        psi[i] = lmbds[i]/(kappa[i]*mu[i])
    return psi

def get_properties(L, lmbd_0, kappa, psi, lmbds, mu):
    P_i0 = np.zeros(L)
    b_i = np.zeros(L) # м.о. числа требований в очереди
    h_i = np.zeros(L) # м.о. числа занятых приборов
    n_i = np.zeros(L) # м.о. числа требований в системе
    u_i = np.zeros(L) # м.о. длительности пребывания требования в системе
    tau = 0 # длительность реакции
    tc = 0 # пропускная способность сети
    for i in range(L):
        summary = 0
        for j in range(kappa[i]):
            summary += (kappa[i]*psi[i])**j / math.factorial(j)
        P_i0[i] = ((((kappa[i]*psi[i])**kappa[i]) / (math.factorial(kappa[i]) * (1 - psi[i]))) + summary)**(-1)
        b_i[i] = P_i0[i] * (((kappa[i]**kappa[i])*(psi[i]**(kappa[i]+1))) / (math.factorial(kappa[i])*((1-psi[i])**2)))
        h_i[i] = psi[i] * kappa[i]
        n_i[i] = expected_n(lmbds[i], mu[i])
        u_i[i] = expected_u(lmbds[i], mu[i])
        tau += lmbds[i]*u_i[i]
    tau *= (1/lmbd_0)
    tc = sum(lmbds)
    return tau, P_i0, b_i, h_i, n_i, u_i, tc


L = 2
kappa = [1, 5]
lambda_0 = 10
mu = np.array([30, 3])
theta = np.array([[0, 1, 0],
                  [_, 0, _],
                  [0, 1, 0]])

# нахождение вектора omega
omega = np.array([1, 0, 0, 0])
eps = 0.0001
omega = stationary_distribution(omega, theta, eps)
print(f'Omegas: {omega},\nCheck (~1): {sum(omega)}')

lambda_ = get_lmbds(lambda_0, omega)
print(f'Lambdas: {lambda_}')

psi = get_psi(lambda_, kappa, mu)
print(f'Psis: {psi}')

tau, P_i0, b_i, h_i, n_i, u_i, tc = get_properties(L, lambda_0, kappa, psi, lambda_, mu)
print(f'tau: {tau}')
print(f'P_i0: {P_i0}')
print(f'b: {b_i}')
print(f'h: {h_i}')
print(f'n: {n_i}')
print(f'u: {u_i}')
print(f'tc: {tc}')

