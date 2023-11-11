import gymnasium as gym
import numpy as np
from gymnasium import spaces
from circuit_analysis import simulate
import random

upper_bound=8000e-9
lower_bound=200e-9
unit=(upper_bound-lower_bound)*0.1
penalty_weight=1e9
class CustomEnv(gym.Env):
    
    def __init__(self):
        super(CustomEnv, self).__init__()
        # self.w1=random.uniform(200E-6, 3000E-6)
        # self.w2=random.uniform(200E-6, 3000E-6)
        # self.w3=random.uniform(200E-6, 3000E-6)
        self.action_space = spaces.Box(-1, +1, (3,), dtype=np.float32)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=lower_bound, high=upper_bound, shape=(3,),dtype=float)
    def step(self, action):

        self.w1+=action[0]*unit
        self.w2+=action[1]*unit
        self.w3+=action[2]*unit
        self.penalty=0
        if(self.w1>upper_bound):
            self.done=True
            self.penalty+= penalty_weight*abs(self.w1 - upper_bound)
            self.w1=upper_bound
        elif(self.w1<lower_bound): 
            self.done=True
            self.penalty+= penalty_weight*abs(self.w1 - lower_bound)
            self.w1=lower_bound
        if(self.w2>upper_bound):
            self.done=True
            self.penalty+= penalty_weight*abs(self.w2 - upper_bound)
            self.w2=upper_bound
        elif(self.w2<lower_bound): 
            self.done=True
            self.penalty+= penalty_weight*abs(self.w2 - lower_bound)
            self.w2=lower_bound
        if(self.w3>upper_bound):
            self.done=True
            self.penalty+= penalty_weight*abs(self.w3-upper_bound)
            self.w3=upper_bound
        elif(self.w3<lower_bound): 
            self.done=True
            self.penalty+=penalty_weight*abs(self.w3 - lower_bound)
            self.w3=lower_bound

        self.observation=np.array([self.w1, self.w2,self.w3])
        # self.total_reward= float(simulate(self.w1, self.w2, self.w3)[0])
        try:
            self.total_reward= float(simulate(self.w1, self.w2, self.w3)[0])
        except Exception as ex:
            print(ex, end='')
            print(self.w1, self.w2, self.w3)
            self.total_reward=-1000
            pass
        self.reward = self.total_reward - self.prev_reward - self.penalty
        self.prev_reward = self.total_reward

        
        if(self.show_log):
            # strFormat='%-20s%-20s%-40s[ %-30s, %-30s, %-30s]\n'
            strFormat='>> %s %s [ %s, %s, %s]\n'

            print(strFormat%(str(self.total_reward), str(action), str(self.w1),str(self.w2),str(self.w3)))

        info={}
        truncated=False
        
       
        return self.observation, self.reward, self.done, truncated, info

    def reset(self, seed=None, options=None):
        self.done=False
        self.reward=0
        self.prev_reward=0
        self.w1=random.uniform(lower_bound, upper_bound)
        self.w2=random.uniform(lower_bound, upper_bound)
        self.w3=random.uniform(lower_bound, upper_bound)  
        self.observation= np.array([self.w1,self.w2,self.w3])
        self.show_log=False ## could be modified
        info={}
        return self.observation, info

