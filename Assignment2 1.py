import random
#a) Test krylov for c2=0.7 and c1 going from 0.05 to 0.65
#b) use the exact expression for the limiting p1(inf.) and a binary search to determine minimum number of states
#   necessary to obtain 95% accuray
#c) Submit the exact value of P1(inf.) and the simulated value

random.seed(1)

class calcVal:
    def getSteps(self, c2=0.7):
        self.steps = []
        r = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65]
        for item in r:
            self.steps.append([item, c2])
        return self.steps

    def getStationaryProb(self, c, N, automata):
        c1 = c[0]
        c2 = c[1]
        if automata == 'krylov':
            c1 = c1 / 2
            c2 = c2 / 2

        d1 = 1 - c1
        d2 = 1 - c2

        t1 = (c1 / c2) ** N

        t2 = (c1 - d1) / (c2 - d2)
        t3_1 = c2 ** N - d2 ** N
        t3_2 = c1 ** N - d1 ** N

        if t3_2 == 0:
            t3 = 0
        else:
            t3 = t3_1 / t3_2

        return 1 / (1 + t1 * t2 * t3)


    def getNumberOfTimes(self, c, accuracyWanted=0.95, maxruns=2000, automata='krylov'):
        first = 3
        last = maxruns
        number = 0
        mid = (first + last) // 2
        while (first < last and first != mid):
            number = mid
            accuracy = self.getStationaryProb(c, mid, automata)

            if accuracy < accuracyWanted:
                first = mid
            else:
                last = mid

            mid = int((first + last) / 2)
        if accuracy < accuracyWanted and (last - first == 1):
            # some bug...  get next state
            number = number + 1
        return number

r = calcVal()
method = "krylov"
for i,e in enumerate(r.getSteps()):
    number = r.getNumberOfTimes(e, 0.95, 200000, method)
    accuracy = r.getStationaryProb(e, number, method)
    print("Method used was: {}, with C-values{}- it needs to run {} times on average to get acc {:1.2f}".format(method, e, number, accuracy))

class KrylovEnv:
    def __init__(self, numAction, c1, c2):
        self.actions = numAction
        self.c1 = c1
        self.c2 = c2

    def penalty(self, action):
        if action == 1:
            if random.random() > self.c2/2:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True

        elif action == 0:
            if random.random() > self.c1/2:
                # print("Reward")
                return False
            else:
                # print("Penalty")
                return True

class TsetlinEnv:
    def __init__(self, numAction, c1, c2):
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


class Krylov:
    def __init__(self, startState, numActions, numStatePerAction):
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
        if self.reward: self.penMovement()
        else: self.rewMovement()

    def makeAction(self, env):
        # Find out which action to take
        # self.makeRange()
        if self.state < self.nSPA+1:
            self.action = 0

        else:
            self.action = 1

        self.reward = env.penalty(self.action)
        self.moveState()

statePerAction = 3
numActions = 2
startState = 0#3 or 4

def startStateR():
    if random.random() < 0.5: startState = statePerAction
    else: startState = statePerAction+1
    return startState

def calcAcc(dicty):
    sum = 0
    for d in dicty:
        sum += dicty[d]
    return dicty[0]/sum

wantedAccuracy = 0.95
print("Krylov: ")
for c1 in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65]:
    minIter = 0
    maxIter = 100000
    booly = True
    simDict = {0: 0, 1: 0}
    startState = startStateR()
    # startState = 3
    accuracy = 0

    env = KrylovEnv(numActions, c1, 0.7)
    k = Krylov(startState, numActions, statePerAction)

    while accuracy < wantedAccuracy or booly:
        k.makeAction(env)
        simDict[k.action] += 1
        if simDict[0]>1: accuracy = calcAcc(simDict)
        if minIter > 10 and minIter<maxIter: booly = False
        minIter+=1
        if minIter > maxIter: break
    print(simDict, accuracy, minIter, c1)


print()
print()
print("Tsetlin: ")
for c1 in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65]:
    minIter = 0
    maxIter = 100000
    booly = True
    simDict = {0: 0, 1: 0}
    startState = startStateR()
    # startState = 3
    accuracy = 0

    env = TsetlinEnv(numActions, c1, 0.7)
    k = Krylov(startState, numActions, statePerAction)

    while accuracy < wantedAccuracy or booly:
        k.makeAction(env)
        simDict[k.action] += 1
        if simDict[0]>1: accuracy = calcAcc(simDict)
        if minIter > 10 and minIter < maxIter: booly = False
        minIter+=1
        if minIter > maxIter: break
        # print(c1, k.reward, k.action)
    print(simDict, accuracy, minIter, c1)