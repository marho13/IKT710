import random


class LriEnv():
    def __init__(self, c1, c2, numAction):
        self.actions = numAction
        self.c1 = c1
        self.c2 = c2

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

class Lri():
    def __init__(self, startState, numActions, F, Kr, numStatePerAction):
        self.F = F
        self.Range = []
        self.Kr = Kr
        self.state = startState
        self.numAction = numActions
        self.nSPA = numStatePerAction
        self.action = 0
        self.reward = False

    def rewMovement(self):
        if self.state == 1: pass #do nothing or move to the same position
        elif self.state == 2*self.nSPA: pass #do nothing or move to the same position
        else: self.state -= 1

    def penMovement(self):
        if self.state == self.nSPA: self.state = self.nSPA*2 #it is 3
        elif self.state == 2*self.nSPA: self.state = self.nSPA #it is 6
        else: self.state+= 1

    def moveState(self):
        if self.reward: self.rewMovement()
        else: self.penMovement()

    def makeAction(self, env):
        # Find out which action to take
        self.makeRange()
        rand = random.random()
        if rand > self.Range[self.state][0]:action = 1
        else: action = 0

        self.reward =  env.penalty(action)
        if not self.reward: self.rewardUpdate(self.state)


L = Lri(3, 2, [0.5,0.5], 0.98, 3)
