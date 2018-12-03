import random
import numpy as np

class binaryIndex:
    def __init__(self, nodeProb=[[1, 0, 0, 0],[0.1, 0.5, 0.4, 0], [0, 0.6, 0.2, 0.2], [0, 0, 0, 1]], startState=[0.1, 0.5, 0.9, 1.0]):
        self.startMatrix = nodeProb
        self.prob = []
        self.probStart = startState
        self.state = 1
        self.high = len(nodeProb)
        self.guessInd = (len(nodeProb)//2)
        self.low = 0
        self.prevGuess = 0
        self.direction = None
        print(self.guessInd)
        for s in self.startMatrix:
            probMatrix = []
            prev = 0
            for x in s:
                if prev == 1.0:
                    probMatrix.append(1.1)
                else:
                    probMatrix.append(float(prev+x))
                    prev = float(prev+x)
            self.prob.append(probMatrix)
        self.state = self.startSearch()
        self.checkArr(self.startMatrix, self.probStart)

    def calcRange(self, startMatrix):
        if isinstance(startMatrix[0], list): print("It is a list!")
        for s in self.startMatrix:
            probMatrix = []
            prev = 0
            for x in s:
                if prev == 1.0:
                    probMatrix.append(1.1)
                else:
                    probMatrix.append(float(prev+x))
                    prev = float(prev+x)
            self.prob.append(probMatrix)

    def checkArr(self, arr1, arr2):
        for r in arr1:
            if sum(r) != 1.0: return False
        if sum(arr2) != 1.0: return False
        if self.lenChecker(arr1, arr2): return True


    def lenChecker(self, arr1, arr2):
        if not (len(arr1)==len(arr2)): return False
        for x in range(len(arr1)):
            if not (len(arr1[x]) == len(arr2)): return False
        return True

    def startSearch(self):
        booly = True
        while booly:
            booly = self.startingPointFound(0.5, self.probStart)
        self.state = self.guessInd

    def binarySearch(self):
        booly = True
        while booly:
            booly = self.indexFound(0.7)
        print(self.guessInd+1, self.prob[self.state][self.guessInd])
        self.state = self.guessInd

    def indexFound(self, val=0.5):
        guess = self.prob[self.state][self.guessInd]
        boolDir = self.checkVal(guess, val)
        dirChange = self.changeDir(boolDir)
        amount = self.changeAmount()
        self.updateValues(boolDir)

        if dirChange and amount: return True
        else: return False

    def startingPointFound(self, val=0.5, prob=[0, 0.5, 0.5, 0]):
        # This is the value of the guess at index[self.guessInd]
        guess = prob[self.guessInd]
        boolDir = self.checkVal(guess, val)
        dirChange = self.changeDir(boolDir)
        amount = self.changeAmount()
        self.updateValues(boolDir)

        if dirChange and amount: return True
        else: return False

    def checkVal(self, guess, val):
        # Checks if the value is larger than the guess
        if val > guess:
            return True
        elif val < guess:
            return False

    def changeAmount(self):
        # Checks the direction, and given a direction
        # it checks if the previous guess was 1 away
        # as this means that the value is between
        # the previous and the new value
        # which means the largest value is the correct one
        if self.direction == "Pluss":
            if self.guessInd == self.prevGuess-1:
                return True
        elif self.direction == "Minus":
            if self.guessInd == self.prevGuess+1:
                return True

        return False

    def changeDir(self, boolDir):
        #Checking the previous direction, and the new one
        #If they are different(if elif) return True
        if self.direction=="Pluss" and not boolDir:
            return True
        elif self.direction=="Minus" and boolDir:
            return True

        #If you keep going in the same direction return False
        else:
            return False

    def updateValues(self, boolDir):
        #Update the necessary values
        #if bool means it is checking higher values
        if boolDir:
            self.prevGuess = self.guessInd
            self.low = self.guessInd
            self.direction = "Pluss"
            pluss = (self.guessInd+self.high)//2
            if pluss < 1:pluss = 1
            self.guessInd += pluss

        #else checking lower values
        else:
            self.prevGuess = self.guessInd
            self.high = self.guessInd
            self.direction = "Minus"
            minus = (self.guessInd+self.low)//2
            if minus < 1:minus = 1
            self.guessInd += minus