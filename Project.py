import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import math


def normpdf(x, mean, sd):
    var = float(sd)**2
    pi = 3.1415926
    denom = (2*pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return (num/denom)/4

class Tsetlin:
    def __init__(self, numAction, c1, c2):
        self.actions = numAction
        self.c1 = c1
        self.c2 = c2
        self.name="Tsetlin"

    def penalty(self, action):
        if action == 1:
            if random.random() > self.c2:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True
        elif action == 0:
            if random.random() > self.c1:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True

class Lri:
    def __init__(self, numAction, c1):
        self.actions = numAction
        self.c1 = c1
        self.name="Lri"

    def penalty(self, action):
        if action == 1:
            if random.random() > self.c2:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True
        elif action == 0:
            if random.random() > self.c1:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True



class agent: #statebased agent
    def __init__(self, startState, numActions, numStatePerAction, name):
        self.state = startState
        self.numAction = numActions
        self.nSPA = numStatePerAction
        self.action = 0
        self.reward = False
        self.name = name

    def rewMovement(self):
        if self.state == 1: pass
        elif self.state == 2*self.nSPA: pass
        else: self.state -= 1

    def penMovement(self):
        if self.state == self.nSPA: self.state = self.nSPA*2 #it is 3
        elif self.state == 2*self.nSPA: self.state = self.nSPA #it is 6
        else: self.state+= 1

    def moveState(self):
        if self.reward: self.penMovement()
        else: self.rewMovement()

    def makeAction(self):
        if self.state < self.nSPA+1:
            self.action = 0

        else:
            self.action = 1

    def rew(self, reward):
        self.reward = reward
        self.moveState()

class estimator:
    def __init__(self, numActions, name, penNum = 0.90):
        self.numAction = numActions
        self.action = 0
        self.reward = False
        self.name = name
        self.actionProb = []
        self.actionList = []
        self.penNum = penNum

        self.initTable()

    def initTable(self):
        num = 0
        for a in range(self.numAction):
            self.actionProb.append(1/self.numAction)
            self.actionList.append(num + 1/self.numAction)
            num+=1/self.numAction

    def penaltyUpdate(self):
        num = self.actionProb[self.action] - self.actionProb[self.action]*self.penNum
        if self.action == 1:
            self.actionProb[self.action] = self.actionProb[self.action]*self.penNum
            self.actionProb[0] = self.actionProb[0] + num

        else:
            self.actionProb[self.action] = self.actionProb[self.action]*self.penNum
            self.actionProb[1] = self.actionProb[1] + num

    def rewardUpdate(self):
        num = self.actionProb[self.action] - self.actionProb[self.action] * self.penNum
        if self.action == 1:
            self.actionProb[0] = self.actionProb[0] * self.penNum
            self.actionProb[1] = self.actionProb[1] + num

        else:
            self.actionProb[1] = self.actionProb[1] * self.penNum
            self.actionProb[0] = self.actionProb[0] + num

    def makeAction(self):
        rand = random.uniform(0,1)
        if rand > self.actionProb[0]:
            self.action = 1
        else:
            self.action = 0

    def rew(self, reward):
        if reward == True: self.penaltyUpdate()
        else: self.rewardUpdate()


class gooreEnv:
    def __init__(self, percent, precision, numActors, name):
        self.rewardProbability = None
        self.precision = precision
        self.percentage = percent
        self.actors = numActors
        self.percentYes = 0.0
        self.std = precision
        self.agentList = []
        self.name = name
        self.randRange()

        # self.actionList = [0,0,1,0,1,0,1,0,1,1]
        self.actionList = [0]*self.actors

        self.agentCreation()

        if "{:.{}}".format(1%precision, self.precision) == str(precision):
            pass
        else:
            print("1 is not divisible by precision number")
            sys.exit()

    def agentCreation(self):
        if self.name != "LRI":
            for _ in range(self.actors):
                self.agentList.append(agent(4, 2, 3, self.name))
        else:
            for _ in range(self.actors):
                self.agentList.append(estimator(2, self.name, 0.90))

    def randRange(self):
        val = 0
        nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        listy = []
        stringy = str(self.precision)

        for a in range(len(stringy)):
            if stringy[a] in nums:
                val += 1

        val -= 1
        self.precision = val

    def rewardProb(self): #calculate the reward probability
        self.percentYes = self.actionList.count(1)/self.actors
        rewardProbability = normpdf(self.percentYes, self.percentage, self.std)
        self.rewardProbability = rewardProbability
        #calculate the reward here (does not need the tsetlin or LRI env anymore)

    def makeActions(self):
        for a in range(len(self.agentList)):
            agent = self.agentList[a]
            agent.makeAction()

        self.rewardProb()
        for b in range(len(self.agentList)):
            agnt = self.agentList[b]
            # print(self.agentList[b].actionProb)
            if (random.uniform(0,1) > self.rewardProbability): agnt.rew(True)
            else: agnt.rew(False)
            self.actionList[b] = agnt.action

    def yesVote(self):
        self.percentYes = self.actionList.count(1)/self.actors
        return self.percentYes


def runner(env, iter):
    num = 0
    listy = {0.0: 0, 0.1: 0, 0.2: 0, 0.3: 0, 0.4: 0, 0.5: 0, 0.6: 0, 0.7: 0, 0.8: 0, 0.9: 0, 1.0:0}
    for x in range(iter):
        env.makeActions()
        listy[env.yesVote()] += 1
        num += 1

    return listy

g = gooreEnv(0.6, 0.1, 10, "LRI")
listy = runner(g, 10000000)
print(listy)