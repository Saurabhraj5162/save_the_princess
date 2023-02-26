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
        self.princess_start_state = self.getStateNum(self.princess_start)
        self.restaurant_state = self.getStateNum(self.restaurant_pos)
        self.pub_state = self.getStateNum(self.pub_pos)
        


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

    def checkWalls(self, pos):
        """
        This function check if the current position is at boundary and return the type of boundary:
        """
        if pos[0] == 0:
            return 'top_wall'
        
        if pos[0] == self.rows -1:
            return 'bottom_wall'
        
        if pos[1] == self.cols-1:
            return 'right_wall'
        
        if pos[1] == 0:
            return 'left_wall'
        else:
            return 'no_wall'
    
    def reset_R_matrix(self,):
        state_map = self.getStates()
        action_map = self.getActions()
        self.R = np.empty((len(state_map), len(state_map)))
        self.R[:] = np.nan

        for cur_state, cur_state_pos in enumerate(state_map.values()):
            #print(f'cur state pos : {cur_state_pos}')
            wall = self.checkWalls(cur_state_pos)
            for action, action_vect in action_map.items():

                #we will check if walls are encountered and will skip the corresponding indoable action:
                if wall=='top_wall' and action == 'up': continue
                if wall=='bottom_wall' and action == 'down': continue
                if wall=='left_wall' and action == 'left': continue
                if wall=='right_wall' and action == 'right': continue

                next_state_pos = (cur_state_pos[0] + action_vect[0], cur_state_pos[1] + action_vect[1])

                if self.isValidState(next_state_pos):
                    next_state = self.cols*next_state_pos[0] + next_state_pos[1]

                    if next_state_pos in self.enemy_pos:
                        self.R[next_state][cur_state] = -1
                    elif next_state_pos == self.princess_start:
                        self.R[next_state][cur_state] = 100

                    #Note: Initially we are penalizing the prince for reaching bar, restaurant and castle. 
                    #       Because we want prince to come to these states only when first he gets the princess
                    #       from prison. So these rewards will be updated in run function when prince gets the princess.
                    elif next_state_pos == self.restaurant_pos:
                       self.R[next_state][cur_state] = -1
                    elif next_state_pos == self.pub_pos:
                       self.R[next_state][cur_state] = -1
                    elif next_state_pos == self.castle_pos:
                       self.R[next_state][cur_state] = -1
                    elif next_state_pos == cur_state_pos:
                        self.R[next_state][cur_state] = -1
                    else:
                        self.R[next_state][cur_state] = 0

        #penalizing -1 for staying in the same position:
        for i in range(len(state_map.values())):
            for j in range(len(state_map.values())):
                if i == j:
                    self.R[i,j] = -1

        
        

        #print(self.R)


                    
    def reset_Q_matrix(self):
        self.Q = np.zeros(self.R.shape)

    def getStateNum(self,pos):
        """
        This function takes a grid position (i,j) and convertes it into absoulte state index (0 to 35).
        """
        return self.cols*pos[0] + pos[1]
    
    def deactivatePrison(self,a,R_copy):
        adj_cells = self.getAdjacentCells(a)
        for cell in adj_cells:
            R_copy[cell,a] = -1

    def activateBarRestCastle(self,R_copy):
        
        adj_cells = self.getAdjacentCells(self.pub_state)
        for cell in adj_cells:
            R_copy[cell,self.pub_state] = 40

        adj_cells = self.getAdjacentCells(self.restaurant_state)
        for cell in adj_cells:
            R_copy[cell,self.restaurant_state] = 70

        adj_cells = self.getAdjacentCells(self.goal_state)
        for cell in adj_cells:
            R_copy[cell,self.goal_state] = 20

    def deactivateBar(self,R_copy):
        
        adj_cells = self.getAdjacentCells(self.pub_state)
        for cell in adj_cells:
            R_copy[cell,self.pub_state] = -1

    def deactivateRestaurant(self,R_copy):
        
        adj_cells = self.getAdjacentCells(self.restaurant_state)
        for cell in adj_cells:
            R_copy[cell,self.restaurant_state] = -1


    
    def getAdjacentCells(self, cell):
        #returns all teh adjacent cells of a cell in the R matrix:
        cells = np.where([~np.isnan(self.R[cell,])])[1]
        return cells

    def run(self,n_episodes,time_steps, epsilon, alpha, gamma):
        self.reset_R_matrix()
        self.reset_Q_matrix()
        
        R_total = []
        castle_hits, enemey_hits= 0, 0
        for episode in range(n_episodes):
            s = self.getStateNum(self.prince_start)
            R_tot_cur_episode = 0
            R_copy = self.R.copy()
            for t in range(time_steps): 
                #find all the available choices of states considering all the actions:
                available_actions = np.where(~np.isnan(R_copy[s]))[0]
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
                r = R_copy[s,a]
                s_old = s
                s = a

                 # Q value updating
                error = R_copy[s_old,a] + gamma*(max(self.Q[s]) - self.Q[s_old,a])
                q_updated= self.Q[s_old,a] + alpha*(error)

                self.Q[s_old,a] = q_updated

                #accumualting the rewards:
                R_tot_cur_episode += R_copy[s_old,a]

                #logic to check the agent does not try to reach princess_prison again:
                #also We need to activate bar and restaurant only when prince has gotten the princess:
                if a == self.princess_start_state:
                    self.deactivatePrison(a,R_copy)
                    self.activateBarRestCastle(R_copy)
                
                
                #logic to check the agent does not try to reach restaurant again:
                if a == self.restaurant_state:
                    self.deactivateRestaurant(R_copy)
                if a == self.pub_state:
                    self.deactivateBar(R_copy)

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
    
    def plot_rewards(self, R_total, alpha, epsilon, gamma):
        R_total_avg = np.array(R_total).cumsum() / np.arange(1, len(R_total) + 1)
        plt.plot(range(50,len(R_total)), R_total_avg[50:])
        plt.xlabel('Episodes')
        plt.ylabel('Total Rewards')
        plt.title(f'Epsilon : {epsilon} | gamma : {gamma} | alpha {alpha}')
        plt.show()


 

