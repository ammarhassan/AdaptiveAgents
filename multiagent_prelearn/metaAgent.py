import copy
import random
from operator import itemgetter
import matplotlib.pyplot as plt

class metaAgent():

	def __init__(self, policyPool, payoffMatrix):
		self.agentType = 'Meta'
		self.proxyAgents = [proxyAgent(policy, depth, 1.0 / len(policyPool)) for policy, depth in policyPool]
		self.payoffMatrix = payoffMatrix


	def agentsMove(self, iteration):
		allMoves = [pa.expectedReturn() for pa in self.proxyAgents]
		
		bestAgent = max(enumerate(allMoves), key = itemgetter(1))[0]
		nextMove = self.proxyAgents[bestAgent].agentsMove()
		nextMoves = [pa.agentsMove() for pa in self.proxyAgents]
		# nextMove = random.choice(['C', 'D'])
		print nextMove, self.proxyAgents[0].currentState, zip(nextMoves, [int(x) for x in allMoves])
		return nextMove


	def updateAgent(self, agentsMove, opponentsMove):
		evidence = [1 if pa.predictedOpponentsMove()==opponentsMove else 0 for pa in self.proxyAgents]
		
		for pa, ev in zip(self.proxyAgents, evidence):
			if ev == 0:
				pa.setProbability(0)

			pa.updateCurrentState(agentsMove, opponentsMove)
			pa.updateRewardSequence(self.payoffMatrix[agentsMove+opponentsMove])

		# print agentsMove + '-' + opponentsMove

	def printRewards(self):
		for pa in self.proxyAgents:
			plt.plot(pa.rewardSequence)
			plt.show()


class proxyAgent():

	def __init__(self, qtable, numHistoryMoves, probability):

		self.qtable = copy.deepcopy(qtable) # a doubly linked list; a dict of dicts in python terms
		self.numHistoryMoves = numHistoryMoves

		self.actions = ['D', 'C'] # not used anywhere yet!
		self.currentState = ''
		self.rewardSequence = []
		self.suggestedMoves = []
		self.probability = probability

	def agentsMove(self):
		move = max(self.qtable[self.currentState].items(), key = itemgetter(1))[0][0]
		self.suggestedMoves.append(move)
		return move

	def updateRewardSequence(self, reward):
		self.rewardSequence.append(reward)

	def updateCurrentState(self, agentsMove, responseMove):

		# update the current state of the agent
		if self.currentState:
			agentsHist, opponentHist = self.currentState.split('-')
		else:
			agentsHist, opponentHist = '', ''
		agentsHist = (agentsHist + agentsMove)[-self.numHistoryMoves:]
		opponentHist = (opponentHist + responseMove)[-self.numHistoryMoves:]
		self.currentState = agentsHist + '-' + opponentHist
		
	
	def expectedReturn(self):
		return max(self.qtable[self.currentState].values()) * self.probability

	def predictedOpponentsMove(self):
		return max(self.qtable[self.currentState].items(), key = itemgetter(1))[0][1]

	def setProbability(self, p):
		self.probability = p

	