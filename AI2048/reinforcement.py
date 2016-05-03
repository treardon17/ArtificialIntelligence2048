import util, pdb
import numpy as np
import copy


class agent:
    def __init__(self):
        self.weights = util.Counter()

        self.state = np.array([[1,0,0,1],[1,0,0,0],[1,0,1,0],[1,0,1,0]])
        self.actions = ['up', 'down', 'left', 'right']
        self.currScore = 0

        self.gamma = 0.8
        self.alpha = 0.2



    def printState(self, state):
        for x in state:
            for y in x:
                print '{0:3}'.format(y),
            print
        print "-------------------"



    def transition(self, state, action):
        score = 0
        mergeCount = 0
        newState = [[],[],[],[]]
        index = 0
        if action == "left" or action == "up":
            index = 3
        if action == "up" or action == "down":
            state = state.T


        i = 0
        for x in state:
            if index == 3:
                for y in x:
                    if y != 0:
                        if y in newState[i]:
                            newState[i][newState[i].index(y)] = 2*y
                            score += 2*y
                            mergeCount +=1
                        else:
                            newState[i].insert(index, y)
            else:
                for y in reversed(x):
                    if y != 0:
                        if y in newState[i]:
                            newState[i].reverse()
                            newState[i][newState[i].index(y)] = 2 * y
                            newState[i].reverse()
                            score += 2*y
                            mergeCount += 1
                        else:
                            newState[i].insert(index, y)
            i += 1

        for x in newState:
            while len(x) < 4:
                x.insert(index, 0)

        if action == 'up' or action == 'down':
            return (np.array(newState).T, score, mergeCount)
        else:
            return (np.array(newState), score, mergeCount)



    def isTerminal(self, state):
        for action in self.actions:
            newState = self.transition(state, action)
            if (newState != state).all():
                print "[+] Action:", action
                self.printState(self.transition(state, action))
                return True
        return False



    def getBest(self, state):
        bestAction = None
        maxVal = 0
        for action in self.actions:
            tempVal = self.transition(state, action)  #tempVal is a tuple (nextState, action)
            if tempVal[1] > maxVal:
                maxVal = tempVal[1]
                bestAction = action

        if bestAction == None:
            return (0,"Exit")
        else:
            return (maxVal, bestAction)



    def getFeatures(self, state):
        feats = util.Counter()
        oneDpos = np.argmax(state)

        feats["largestPos"] = (oneDpos/4, oneDpos%4)    #(row, col)
        feats["free"] = 16 - np.count_nonzero(state)

        sumMergeCount = 0
        #sumScore = 0
        for action in self.actions:
            things = self.transition(state, action)
            sumMergeCount += things[2]
            #sumScore += things[1]

        feats["mergeCount"] = sumMergeCount
        #feats["score"] = sumScore



    def getQValue(self, state):
        return self.weights.__mul__(self.getFeatures(state))



    def updateWeights(self, state, action, nextState, reward):
        features = self.getFeatures(state)
        #the score is the reward

        difference = (reward + self.gamma*self.getBest(state)[0]) - self.getQValue(state)

        for f in features.keys():
            self.weights[f] = self.weights[f] + (self.alpha*difference*features[f])


# features: number of free spaces on the board, location of the largest number, location of merged tiles, score == merged tiles