"""
    MDP:Value iteration
                    s1 s2 s3 s4 s5
                     o  o  o  o  o
                    s6 s7 s8 s9 s10
                     o  o  o  o  o
                    s...
                     o  o  o  o  o
                     o  o  o  o  o
                     o  o  o  o  o


                   | p 1-p 0.......0  |
                   | .  0 1-p 0....0  |
        P[0,:,:] = | .  .  0  .       |
                   | .  .        .    |
                   | .  .         1-p |
                   | p  0  0....0 1-p |

                 |  0  |
                 |  .  |
        R[:,0] = |  .  |
                 |  .  |
                 |  0  |
                 |  r1 |

                 0     'UP': [1, 0, 0],
                 1     'DOWN': [-1, 0, 0],
                 2     'LEFT': [0, 0, -1],
                 3     'RIGHT': [0, 0, 1],
                 4     'FORWARD': [0, 1, 0],
                 5     'BACKWARD': [0, -1, 0],
                 6     'SCAN':[0,0,0]

        S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25
    S01  0  0.5  0   0   0  0.5  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S02 0.3  0  0.3  0   0   0  0.3  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S03  0  0.3  0  0.3  0   0   0  0.3  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S04  0   0  0.3  0  0.3  0   0   0  0.3  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S05  0   0   0  0.5  0   0   0   0   0  0.5  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S06 0.3  0   0   0   0   0  0.3  0   0   0  0.3  0   0   0   0   0   0   0   0   0   0   0   0   0   0
    S07  0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0   0   0   0   0   0   0   0
    S08  0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0   0   0   0   0   0   0
    S09  0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0   0   0   0   0   0
    S10  0   0   0   0  0.3  0   0   0  0.3  0   0   0   0   0  0.3  0   0   0   0   0   0   0   0   0   0
    S11  0   0   0   0   0  0.3  0   0   0   0   0  0.3  0   0   0  0.3  0   0   0   0   0   0   0   0   0
    S12  0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0   0   0
    S13  0   0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0   0
    S14  0   0   0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0   0   0   0
    S15  0   0   0   0   0   0   0   0   0  0.3  0   0   0  0.3  0   0   0   0   0  0.3  0   0   0   0   0
    S16  0   0   0   0   0   0   0   0   0   0  0.3  0   0   0   0   0  0.3  0   0   0  0.3  0   0   0   0
    S17  0   0   0   0   0   0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0   0
    S18  0   0   0   0   0   0   0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0   0
    S19  0   0   0   0   0   0   0   0   0   0   0   0   0  1/4  0   0   0  1/4  0  1/4  0   0   0  1/4  0
    S20  0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.3  0   0   0  0.3  0   0   0   0   0  0.3
    S21  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.5  0   0   0   0   0  0.5  0   0   0
    S22  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.3  0   0   0  0.3  0  0.3  0   0
    S23  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.3  0   0   0  0.3  0  0.3  0
    S24  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.3  0   0   0  0.3  0  0.3
    S25  0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0  0.5  0   0   0  0.5  0

"""
import math
from gym import Env,spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
import time
from operator import add
import mdptoolbox

costMove = 1
costScan = 4
costBump = 5
r1=-1
r2=100
r3=-100

class Obstacles():
    def __init__(self):
        self.known = [[0,1,2]]#[0,4,3]
        self.unknown = [[1,1,1]]
        self.total = self.known+self.unknown

#add terrain and obstacle!
class Map():# static and dynamic
    def __init__(self,lay,row,col): #z,y,x!
        self.lay = lay #redundant!
        self.row = row
        self.col = col
        #self.shape = [lay, row, col]
        #self.range = [[[False for x in range(col)] for y in range(row)] for z in range(lay)] for some reason doesn't work

        self.obstacles = Obstacles()
        self.canvas = [[[(1 if ([z, y, x] in self.obstacles.known) else (2 if ([z, y, x] in self.obstacles.unknown) else 0)) for x in range(col)] for y in range(row)] for z in range(lay)]
        #0-empty;1-known;2-unknown

        """HEURISTIC!!!"""
        # self.h = [[[0 for x in r  ange(col)] for y in range(row)] for z in range(lay)]
        # for l in range(lay):
        #     for r in range(row):
        #         for c in range(col):
        #             self.h[l][r][c] = pow(
        #                         (pow(l-end[0],2)
        #                         +pow(r-end[1],2)
        #                         +pow(c-end[2],2))
        #                         ,0.5) #sqrt((a-a')^2+(b-b')^2+(c-c')^2)
        #print(self.h[0][0][0])
        """HEURISTIC!!!"""


class Robot():
    def __init__(self,lay,row,col,start=[0,0,0],end=[0,0,0]): #z,y,x!
        self.start = start
        self.end = end
        self.map = Map(lay,row,col)
        self.bump = False
        self.z,self.y,self.x = start
        self.state = [[self.z,self.y,self.x],self.bump,[[[(1 if ([z, y, x] in self.map.obstacles.known) else 0) for x in range(col)] for y in range(row)] for z in range(lay)]]
        self.action = {'UP': [1, 0, 0],
                       'DOWN': [-1, 0, 0],
                       'LEFT': [0, 0, -1],
                       'RIGHT': [0, 0, 1],
                       'FORWARD': [0, 1, 0],
                       'BACKWARD': [0, -1, 0],
                       'SCAN': [0, 0, 0]
                       }
        self.moveRecord=''
        self.pastPath = []

    def setStateReward(self,R,point:list[3],reward):
        if (0 <= point[0]+1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            R[(point[0]+1)*self.map.row*self.map.col+point[1]*self.map.row+point[2],1] = reward
        if (0 <= point[0]-1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            R[(point[0]-1)*self.map.row*self.map.col+point[1]*self.map.row+point[2],0] = reward
        if (0 <= point[0] < self.map.lay and 0 <= point[1]+1 < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+(point[1]+1)*self.map.row+point[2],5] = reward
        if (0 <= point[0] < self.map.lay and 0 <= point[1]-1 < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+(point[1]-1)*self.map.row+point[2],4] = reward
        if (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]-1 < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]-1,3] = reward
        if (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]+1 < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]+1,2] = reward
        return R

    def boundaryVoidReward(self,R,point:list[3],reward):
        if not (0 <= point[0]+1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],0] = reward
        if not (0 <= point[0]-1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],1] = reward
        if not (0 <= point[0] < self.map.lay and 0 <= point[1]+1 < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],4] = reward
        if not (0 <= point[0] < self.map.lay and 0 <= point[1]-1 < self.map.row and 0 <= point[2] < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],5] = reward
        if not (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]-1 < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],2] = reward
        if not (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]+1 < self.map.col):
            R[point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2],3] = reward
        return R

    def setLastStateReward(self,R,point:list[3],lastMove,reward):
        pass

    # def setEndTrap(self,R,point:list[3],reward):
    #     if  (0 <= point[0] + 1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 0] = reward
    #     if  (0 <= point[0] - 1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 1] = reward
    #     if  (0 <= point[0] < self.map.lay and 0 <= point[1] + 1 < self.map.row and 0 <= point[2] < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 4] = reward
    #     if  (0 <= point[0] < self.map.lay and 0 <= point[1] - 1 < self.map.row and 0 <= point[2] < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 5] = reward
    #     if  (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] - 1 < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 2] = reward
    #     if  (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] + 1 < self.map.col):
    #         R[point[0] * self.map.row * self.map.col + point[1] * self.map.row + point[2], 3] = reward
    #     return R

    def blockTransition(self,P,point:list[3],S):
        if (0 <= point[0]+1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            P[1,(point[0]+1)*self.map.row*self.map.col+point[1]*self.map.row+point[2],:]=[1 if x==(point[0]+1)*self.map.row*self.map.col+point[1]*self.map.row+point[2] else 0 for x in range(S)]
        if (0 <= point[0]-1 < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2] < self.map.col):
            P[0,(point[0]-1)*self.map.row*self.map.col+point[1]*self.map.row+point[2],:]=[1 if x==(point[0]-1)*self.map.row*self.map.col+point[1]*self.map.row+point[2] else 0 for x in range(S)]
        if (0 <= point[0] < self.map.lay and 0 <= point[1]+1 < self.map.row and 0 <= point[2] < self.map.col):
            P[5,point[0]*self.map.row*self.map.col+(point[1]+1)*self.map.row+point[2],:]=[1 if x==point[0]*self.map.row*self.map.col+(point[1]+1)*self.map.row+point[2] else 0 for x in range(S)]
        if (0 <= point[0] < self.map.lay and 0 <= point[1]-1 < self.map.row and 0 <= point[2] < self.map.col):
            P[4,point[0]*self.map.row*self.map.col+(point[1]-1)*self.map.row+point[2],:]=[1 if x==point[0]*self.map.row*self.map.col+(point[1]-1)*self.map.row+point[2] else 0 for x in range(S)]
        if (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]-1 < self.map.col):
            P[3,point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]-1,:]=[1 if x==point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]-1 else 0 for x in range(S)]
        if (0 <= point[0] < self.map.lay and 0 <= point[1] < self.map.row and 0 <= point[2]+1 < self.map.col):
            P[2,point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]+1,:]=[1 if x==point[0]*self.map.row*self.map.col+point[1]*self.map.row+point[2]+1 else 0 for x in range(S)]
        return P

    def endTransition(self,P,end:list[3],S):
        if (0 <= end[0]+1 < self.map.lay and 0 <= end[1] < self.map.row and 0 <= end[2] < self.map.col):
            P[0,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        if (0 <= end[0]-1 < self.map.lay and 0 <= end[1] < self.map.row and 0 <= end[2] < self.map.col):
            P[1,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        if (0 <= end[0] < self.map.lay and 0 <= end[1]+1 < self.map.row and 0 <= end[2] < self.map.col):
            P[4,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        if (0 <= end[0] < self.map.lay and 0 <= end[1]-1 < self.map.row and 0 <= end[2] < self.map.col):
            P[5,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        if (0 <= end[0] < self.map.lay and 0 <= end[1] < self.map.row and 0 <= end[2]-1 < self.map.col):
            P[2,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        if (0 <= end[0] < self.map.lay and 0 <= end[1] < self.map.row and 0 <= end[2]+1 < self.map.col):
            P[3,end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2],:]=[1 if x==end[0]*self.map.row*self.map.col+end[1]*self.map.row+end[2] else 0 for x in range(S)]
        return P

    def selectMovement(self,policy:list,localStart:list[3]):
        p = policy[localStart[0]*self.map.row*self.map.col+localStart[1]*self.map.row+localStart[2]]
        action = [x for x in self.action.keys()]
        nextMove = action[p]
        return nextMove

    def valueIteration(self, plist, r1=-1, r2=10000, r3=-5, p=1):  # 1*5*5=25 states, 8 actions
        S = self.map.lay * self.map.row * self.map.col
        S_2D = self.map.row * self.map.col
        assert S > 1, "The number of states S must be greater than 1."
        assert (r1, r3 <= 0) and (r2 > 0), "r1 is cost, r2 is reward."
        assert 0 <= p <= 1, "The probability p must be in [0; 1]."

        P = np.zeros((7, S, S))
        # up
        if self.map.lay>1:
            P[0, :, :] = np.add(np.diag(np.ones(S - S_2D), S_2D),[p if (x>=S-S_2D) else 0 for x in range(S)]*np.diag(np.ones(S)))
        else:
            P[0, :, :] = np.diag(np.ones(S))

        # down
        if self.map.lay>1:
            P[1, :, :] = np.add(np.diag(np.ones(S - S_2D),-S_2D),[p if (x<S_2D) else 0 for x in range(S)]*np.diag(np.ones(S)))
        else:
            P[1, :, :] = np.diag(np.ones(S))

        # left
        P[2, :, :] = np.add([(p if (x % self.map.row == 0) else 0) for x in range(S)] * np.diag(np.ones(S)),
                            [(0 if ((x + 1) % self.map.row == 0) else p) for x in range(S)] * np.diag(np.ones(S - 1), -1))

        # right
        P[3, :, :] = np.add([(p if ((x + 1) % (self.map.row) == 0) else 0) for x in range(S)] * np.diag(np.ones(S)),
                            [(0 if (x % self.map.row == 0) else p) for x in range(S)] * np.diag(np.ones(S - 1), 1))

        # forward
        for y in range(self.map.lay):
            for x in range(y * S_2D, y * S_2D + S_2D):
                if x < y * S_2D + S_2D - self.map.row:
                    P[4, x, x + self.map.row] = 1
                else:
                    P[4, x, x] = 1

        # backward
        for y in range(self.map.lay):
            for x in range(y * S_2D, y * S_2D + S_2D):
                if x < S_2D - self.map.row:
                    P[5, x, x] = 1
                else:
                    P[5, x, x - self.map.row] = 1

        # stay #scan
        P[6, :, :] = np.diag(np.ones(S))

        for point in self.map.obstacles.known:
            P = self.blockTransition(P,point,S)
        #no action for end state
        P = self.endTransition(P,self.end,S)
        #P = self.blockTransition(P,self.start,S)

        # set for normal
        R = r1 * np.ones((S, 7))
        # set for end
        R = self.setStateReward(R,self.end,r2)
        #R = self.setEndTrap(R,self.end,r3)
        # set for boundary
        # for l in range(self.map.lay):
        #     for r in range(self.map.row):
        #         for c in range(self.map.col):
        #             R = self.boundaryVoidReward(R,[l,r,c],r3)
        # set for obstacles
        for pp in self.map.obstacles.known:
            R = self.setStateReward(R,pp,r3)
        # set for last position
        # for ppp in plist:
        #     R = self.setStateReward(R, ppp, -10*plist.count(p))
            #print(ppp,end='')
            #print(plist.count(p))
        return (P, R)

class StartUp(Env):
    def __init__(self,lay=1,row=5,col=5,start=[0,0,0],end=[0,0,0]): #z y x
        self.r=Robot(lay,row,col,start,end)
        self.start = self.r.start
        self.end = self.r.end
        self.action_space = self.r.action
        # sum=0
        # for i in range(len(self.r.map.obstacles.unknown)):
        #     sum += math.comb(len(self.r.map.obstacles.unknown),i)
        self.observation_space = spaces.Discrete(lay*col*row)
        self.timeLengthMax = row*col*lay #!!to be changed
        self.g0 = 0



    def step(self):
        # gfinal = 0
        self.r.bump = False
        self.r.state[1] = False
        """HEURISTIC!!!"""
        # for x in self.r.action.keys():  # 访问键
        #     if x == "SCAN":
        #         g = costScan
        #     else:
        #         g = costMove
        #     test = np.add(self.r.state[0][:3], self.r.action['{}'.format(x)])
        #     test = test.tolist()
            #print(type(test)) nparray
            #print((test.tolist()[0]))
            #if (0 <= test[0] < self.r.map.lay and 0 <= test[1] < self.r.map.row and 0 <= test[2] < self.r.map.col ): #keep in the canvas
                #f = float(self.g0 + g + self.r.map.h[test[0]][test[1]][test[2]])
                #if fmin == 0 or f<=fmin:
                    # fmin = f
        """HEURISTIC!!!"""


        """Value iteration"""
        #print(self.pastPath)
        P, R = self.r.valueIteration(self.r.pastPath)
        vi = mdptoolbox.mdp.ValueIteration(P, R, 0.9, 0.01)
        vi.run()
        policy = list(vi.policy)
        """Value iteration"""
        """Qlearning"""
        # ql = mdptoolbox.mdp.QLearning(P, R, 0.96)
        # ql.run()
        # Q=list(ql.Q)
        # policy = Q
        """Qlearning"""

        nextMove = self.r.selectMovement(policy,self.r.state[0])
        for z in range(self.r.map.lay):
            print("layer {}".format(z+1))
            for y in range(self.r.map.row):
                for x in range(self.r.map.col):
                    print(" {} ".format(policy[x + self.r.map.row * y + self.r.map.row*self.r.map.col * z]), end='')
                    # print(vi.policy[1]<5)
                print()
            print()
        if nextMove == "SCAN":
            gfinal = costScan #delete
        else:
            gfinal = costMove

        last = self.r.state[0]
        self.r.state[0] = np.add(self.r.state[0][:3], self.r.action['{}'.format(nextMove)])
        self.r.state[0] = self.r.state[0].tolist()
        #self.r.state[0] = [nextState for nextState in nextState.tolist()]
        if self.r.state[0] in self.r.map.obstacles.total:
            self.r.bump = True #redundant!!!
            self.r.state[1] = True
            if self.r.state[0] not in self.r.map.obstacles.known:
                self.r.map.obstacles.known.append(self.r.state[0])
            self.r.state[0] = last
            self.g0 += costBump

        else:
            self.g0 += gfinal

        self.r.pastPath.append(self.r.state[0])
        self.r.moveRecord = nextMove  # to be extended for obstacles
        self.timeLengthMax -= 1
        """test!!"""
        #print(self.r.map.obstacles.known)


        if self.timeLengthMax <= 0 or self.r.state[0]==self.end:
            done = True
        else:
            done = False
        info = {}
        # time.sleep(1) #slow down to see the progress
        return self.r.state, self.g0, done, info

    def render(self, mode="human"):
        print("position: {}".format(self.r.state[0]))
        if self.r.state[1] == True:
            print("Bump!")
        for i in range(self.r.map.lay):
            print("layer {}".format(str(i+1)))
            for j in range(self.r.map.row):
                for k in range(self.r.map.col):
                    if self.r.state[0][0]==i and self.r.state[0][1]==j and self.r.state[0][2]==k: #robot
                        if self.r.bump == False: #redundant!!!
                            print(" r ",end='')
                        else:
                            print(" x ",end='')
                    #elif self.r.map.canvas[i][j][k] == 1: #known
                    elif [i,j,k] in self.r.map.obstacles.known:
                        print(" = ",end='')
                    elif [i,j,k] in self.r.map.obstacles.unknown: #unknown
                        print(" - ",end='')
                    elif [i,j,k] == self.end: #end
                        print(" 口 ",end='')
                    else: #empty
                        print(" o ",end='')
                print()
        print()

    def reset(self):
        self.r.bump = False #redundant!!!
        self.r.state[0:1] = [[self.start[0],self.start[1],self.start[2]],False]
        self.g0 = 0
        self.pastPath = []
        self.timeLengthMax = 100
        return self.r.state

env = StartUp(2,2,2,[0,1,0],[1,0,1])

episodes = 1
for episodes in range (1, episodes+1):
    state=env.reset()
    done = False
    print("------------------------")
    print("Episode: {}".format(episodes))
    #print(env.r.map.h)
    print("start position:{}".format(env.start))
    while not done:
        print("step:{}----".format(101-env.timeLengthMax))
        state,g0,done,info = env.step()
        env.render()
    print('cost:{}'.format(str(env.g0)))
    print("------------------------")
    print()
    env.close()
