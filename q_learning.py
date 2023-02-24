import numpy as np
from Environment import Town

class QLearning(Town):

    def __init__(self, rows, cols, height, width, background_color) -> None:
        super().__init__(rows, cols,height, width, background_color)

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
    
    def reset__R_matrix(self,):
        state_map = self.getStates()
        action_map = self.getActions()
        R = np.empty((len(action_map), len(state_map)))
        R[:] = np.nan

        #defining rewards for the states:

        for i, action_vect in enumerate(action_map.values()):
            for j, cur_state in enumerate(state_map.values()):
            
                #print(i,j)
                #we will check if the action leads to favourable state then we will reward positively:
                #self.enemy_pos = [(0,4), (1,4), (4,3), (3,1), (2,2)]
                next_state = (cur_state[0] + action_vect[0], cur_state[1] + action_vect[1])

                if self.isValidState(next_state):
                    if next_state in self.enemy_pos:
                        R[i][j] = -300
                    elif next_state == self.princess_start:
                        R[i][j] = 100
                    elif next_state == self.restaurant_pos:
                        R[i][j] = 70
                    elif next_state == self.pub_pos:
                        R[i][j] = 40
                    elif next_state == self.castle_pos:
                        R[i][j] = 20
                    elif next_state == cur_state:
                        R[i][j] = -1
                    else:
                        R[i][j] = 0

        print(R)
        print(action_map)
        print(state_map)
        return R
    
    
    

Q = QLearning(6,6,600,600,(0,100,0))

Q.reset__R_matrix()


print((1,2) + (1,2))