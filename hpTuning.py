import numpy as np
from Environment import Town
import matplotlib.pyplot as plt
from q_learning import QLearning


#epsilon = 0.9
time_steps = 2000
alpha_lst = [0.4, 0.1]
gamma_lst = [0.4, 0.1]
temp_lst = [0.9]
epsilon_lst = [0.9]
epsilon_decay_lst = [0.999999]
colors= ['r', 'b', 'g', 'y', 'c']
Q = QLearning(6,6,600,600,(0,100,0))
#Q.reset_R_matrix()
#print(Q.princess_start_state)
#print(Q.R[5])

alpha_rewards = {} 
gamma_rewards = {} 
alpha_gamma_rewards  = {}
epsilon_rewards  = {}
epsilon_decay_rewards  = {}
temp_rewards = {}

# for epsilon_decay in epsilon_decay_lst:
#     R_total = Q.run(10000,time_steps,epsilon=0.9, alpha=0.4, gamma=0.4, epsilon_decay = 0.999999)
#     epsilon_decay_rewards[epsilon_decay] = R_total

# for temperature in temp_lst:
#     R_total = Q.run_softmax(10000,time_steps,temperature, alpha=0.4, gamma=0.4)
#     temp_rewards[temperature] = R_total


# for temperature, R_total in temp_rewards.items():

#     Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
#     plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha=0.4,gamma=0.4,temperature={temperature}')
#     plt.legend(loc="lower right")

# plt.xlabel('episodes')
# plt.ylabel('R')
# plt.title('Average total reward with softmax policy', fontsize=12, pad=20)
# plt.show()

for alpha in alpha_lst:
    for gamma in gamma_lst:
        R_total = Q.run(10000, time_steps, 0.9, alpha, gamma, 0.999999)
        alpha_gamma_rewards[(alpha, gamma)] = R_total

for alpha_gamma, R_total in alpha_gamma_rewards.items():
    alpha, gamma = alpha_gamma
    
    Rtot_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
    plt.plot(np.arange(500, len(Rtot_avg)), Rtot_avg[500:], label=f'alpha={alpha},gamma={gamma},eps=0.9')
    plt.legend(loc="lower right")
    
plt.xlabel('episodes')
plt.ylabel('R')
plt.title('Average total reward with different alpha/gamma values', fontsize=12, pad=20)
plt.show()


