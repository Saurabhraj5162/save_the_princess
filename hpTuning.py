import numpy as np
from Environment import Town
import matplotlib.pyplot as plt
from q_learning import QLearning


epsilon = 0.9
time_steps = 2000
alpha_lst = [1, 0.9, 0.6, 0.4, 0.1]
gamma_lst = [0.9, 0.7, 0.5, 0.3, 0.1]
colors= ['r', 'b', 'g', 'y', 'c']
Q = QLearning(6,6,600,600,(0,100,0))
#Q.reset_R_matrix()
#print(Q.princess_start_state)
#print(Q.R[5])

alpha_rewards = {}
gamma_rewards = {}

# for alpha in alpha_lst:
#     R_total = Q.run(10000,time_steps,epsilon, alpha, gamma=0.9)
#     alpha_rewards[alpha] = R_total


# for alpha, R_total in alpha_rewards.items():

#     Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
#     plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha={alpha},gamma=0.9,eps=0.9')
#     plt.legend(loc="lower right")

# plt.xlabel('episodes')
# plt.ylabel('R')
# plt.title('Average total reward with different alpha values', fontsize=12, pad=20)
# plt.show()

for gamma in gamma_lst:
    R_total = Q.run(10000,time_steps,epsilon, 0.9, gamma)
    gamma_rewards[gamma] = R_total

for gamma, R_total in gamma_rewards.items():

    Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
    plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha=0.9,gamma={gamma},eps=0.9')
    plt.legend(loc="lower right")
    
plt.xlabel('episodes')
plt.ylabel('R')
plt.title('Average total reward with different gamma values', fontsize=12, pad=20)
plt.show()

