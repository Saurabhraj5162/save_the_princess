import numpy as np
from Environment import Town
import matplotlib.pyplot as plt

class QLearning(Town):

    def __init__(self, rows, cols, height, width, background_color) -> None:
        super().__init__(rows, cols,height, width, background_color)

        self.goal_state = self.getStateNum(self.castle_pos)
        self.enemy_states = {}
        for enm_pos in self.enemy_pos:
            self.enemy_states[self.getStateNum(enm_pos)] = 1


    def isValidState(self,state):
        r,c = state
        return r>=0 and r<self.rows and r >= 0 and c<self.cols

    def getStates(self,):
        s_map = {}
        idx = 1
        for i in range(self.rows):
            for j in range(self.cols):
                s_map[idx] = (i,j)
                idx += 1
        return s_map
    
    def getActions(self,):
        a_map = {}
        a_map['up'] = (-1,0)
        a_map['down'] = (1,0)
        a_map['left'] = (0,-1)
        a_map['right'] = (0,1)
        a_map['stay'] = (0,0)

        return a_map
    
    # def reset__R_matrix_old(self,):
    #     state_map = self.getStates()
    #     action_map = self.getActions()
    #     R = np.empty((len(action_map), len(state_map)))
    #     R[:] = np.nan

    #     #defining rewards for the states:

    #     for i, action_vect in enumerate(action_map.values()):
    #         for j, cur_state in enumerate(state_map.values()):
            
    #             #print(i,j)
    #             #we will check if the action leads to favourable state then we will reward positively:
    #             #self.enemy_pos = [(0,4), (1,4), (4,3), (3,1), (2,2)]
    #             next_state = (cur_state[0] + action_vect[0], cur_state[1] + action_vect[1])

    #             if self.isValidState(next_state):
    #                 if next_state in self.enemy_pos:
    #                     R[i][j] = -300
    #                 elif next_state == self.princess_start:
    #                     R[i][j] = 100
    #                 elif next_state == self.restaurant_pos:
    #                     R[i][j] = 70
    #                 elif next_state == self.pub_pos:
    #                     R[i][j] = 40
    #                 elif next_state == self.castle_pos:
    #                     R[i][j] = 20
    #                 elif next_state == cur_state:
    #                     R[i][j] = -1
    #                 else:
    #                     R[i][j] = 0

    #     print(R)
    #     print(action_map)
    #     print(state_map)
    #     return R

    
    def reset_R_matrix(self,):
        state_map = self.getStates()
        action_map = self.getActions()
        self.R = np.empty((len(state_map), len(state_map)))
        self.R[:] = np.nan

        for cur_state, cur_state_pos in enumerate(state_map.values()):
            for action, action_vect in action_map.items():
                next_state_pos = (cur_state_pos[0] + action_vect[0], cur_state_pos[1] + action_vect[1])

                if self.isValidState(next_state_pos):
                    next_state = self.cols*next_state_pos[0] + next_state_pos[1]

                    if next_state_pos in self.enemy_pos:
                        self.R[next_state][cur_state] = -300
                    elif next_state_pos == self.princess_start:
                        self.R[next_state][cur_state] = 100
                    elif next_state_pos == self.restaurant_pos:
                        self.R[next_state][cur_state] = 70
                    elif next_state_pos == self.pub_pos:
                        self.R[next_state][cur_state] = 40
                    elif next_state_pos == self.castle_pos:
                        self.R[next_state][cur_state] = 20
                    elif next_state_pos == cur_state_pos:
                        self.R[next_state][cur_state] = -1
                    else:
                        self.R[next_state][cur_state] = 0

        print(self.R)


                    
    def reset_Q_matrix(self):
        self.Q = np.zeros(self.R.shape)

    def getStateNum(self,pos):
        """
        This function takes a grid position (i,j) and convertes it into absoulte state index (0 to 35).
        """
        return self.cols*pos[0] + pos[1]

    def run(self,n_episodes,time_steps, epsilon, alpha, gamma):
        self.reset_R_matrix()
        self.reset_Q_matrix()
        
        R_total = []
        castle_hits, enemey_hits= 0, 0
        for episode in range(n_episodes):
            s = self.getStateNum(self.prince_start)
            R_tot_cur_episode = 0
            for t in range(time_steps): 
                #find all the available choices of states considering all the actions:
                available_actions = np.where(~np.isnan(self.R[s]))[0]
                #print(available_actions)
                #print(self.R[s])
                #get q value corresponding to each available actions:
                available_q_values = [self.Q[s,idx] for idx in available_actions]
                #print(available_q_values)
                #now we calculate the best action based on greed of q value:
                best_actions = available_actions[np.where(available_q_values == max(available_q_values))]
                #print(best_actions)
                best_action_q_vals = [self.Q[s,x] for x in best_actions]

                #choosing action based on epsilon-greedy policy
                if np.random.uniform() > epsilon:
                    a = np.random.choice(available_actions)
                else:
                    a = np.random.choice(best_actions)

                #updating the environment:
                r = self.R[s,a]
                s_old = s
                s = a

                 # Q value updating
                error = self.R[s_old,a] + gamma*(max(self.Q[s]) - self.Q[s_old,a])
                q_updated= self.Q[s_old,a] + alpha*(error)

                self.Q[s_old,a] = q_updated

                #accumualting the rewards:
                R_tot_cur_episode += self.R[s_old,a]

            
                if s == self.goal_state:
                    #print('REACHED TO THE CASTLE!')
                    castle_hits += 1
                    break

                if s in self.enemy_states:
                    enemey_hits +=1
                    break

            R_total.append(R_tot_cur_episode)
            print('Episode {} finished. Q matrix values:\n{}'.format(episode,self.Q.round(1)))
        print(f'Reached Castle {castle_hits} times.')
        print(f'Hit Enemey {enemey_hits} times.')
        return R_total
    
    def plot_rewards(self, R_total):
        plt.plot(range(len(R_total)), R_total)
        plt.xlabel('Episodes')
        plt.ylabel('Total Rewards')
        plt.show()


 
epsilon = 0.9
time_steps = 2000
alpha = 1
gamma = 0.8

Q = QLearning(6,6,600,600,(0,100,0))

R_total = Q.run(10000,time_steps,epsilon, alpha, gamma)
Q.plot_rewards(R_total)


