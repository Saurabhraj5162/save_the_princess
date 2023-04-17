import numpy as np
from Environment import Town
import matplotlib.pyplot as plt
from sarsa_learning import SARSA


epsilon = 0.9
time_steps = 2000
alpha_lst = [0.4]
gamma_lst = [0.4]
colors= ['r', 'b', 'g', 'y', 'c']
Q = SARSA(6,6,600,600,(0,100,0))

alpha_rewards = {}
gamma_rewards = {}

# Loop over different alpha values
for alpha in alpha_lst:
    R_total = Q.run(10000,time_steps,epsilon, alpha, gamma=0.9)
    alpha_rewards[alpha] = R_total

# Plot average total reward for different alpha values
plt.figure(figsize=(10,6))
for i, alpha in enumerate(alpha_lst):
    R_total = alpha_rewards[alpha]
    Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
    plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha={alpha},gamma=0.4, epsilon={epsilon}', color=colors[i])
plt.legend(loc="lower right")
plt.xlabel('Episodes')
plt.ylabel('Average total reward')
plt.title('Average total reward with SARSA algorithm', fontsize=12, pad=20)
plt.show()

# Loop over different gamma values
for gamma in gamma_lst:
    R_total = Q.run(10000,time_steps,epsilon, 0.9, gamma)
    gamma_rewards[gamma] = R_total

# Plot average total reward for different gamma values
plt.figure(figsize=(10,6))
for i, gamma in enumerate(gamma_lst):
    R_total = gamma_rewards[gamma]
    Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
    plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha=0.4,gamma={gamma}', color=colors[i])
plt.legend(loc="lower right")
plt.xlabel('Episodes')
plt.ylabel('Average total reward')
plt.title('Average total reward with different gamma values', fontsize=12, pad=20)
plt.show()
