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
		# determining the best move
		allMoves = [pa.expectedReturn() for pa in self.proxyAgents]
		bestAgent = max(enumerate(allMoves), key = itemgetter(1))[0]
		nextMove = self.proxyAgents[bestAgent].agentsMove()

		stateValues = [pa.currentBestValue() for pa in self.proxyAgents]
		predictedOpponents = [pa.predictedOpponentsMove() for pa in self.proxyAgents]
		print nextMove, self.proxyAgents[0].currentState, zip(predictedOpponents, [int(x) for x in stateValues])

		return nextMove


	def updateAgent(self, agentsMove, opponentsMove):
		evidence = [1 if opponentsMove in pa.predictedOpponentsMove() else 0 for pa in self.proxyAgents]
		
		for pa, ev in zip(self.proxyAgents, evidence):
			if ev == 0:
				pa.setProbability(0)

			pa.updateCurrentState(agentsMove, opponentsMove)
			pa.updateRewardSequence(self.payoffMatrix[agentsMove+opponentsMove])
		print [pa.probability for pa in self.proxyAgents]
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

	def isFound(self):
		remaining = sum([ax.probability>0 for ax in self.agents])
		if remaining ==1:
			return 'Found'
		elif remaining ==0:
			return 'Unknown'
		else:
			return 'Searching'

	def isValid(self):
		# check for immature state
		if self.currentState not in self.qtable:
			return False

		# check for if this agent is 
		elif sum(self.qtable[self.currentState].values()) == 0:
			return False
		else:
			return True

	def agentsMove(self):
		if not self.isValid():
			return random.choice(['C', 'D'])
		else:
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
		if self.isValid():
			return max(self.qtable[self.currentState].values()) * self.probability
		else:
			return 0

	def currentBestValue(self):
		if self.isValid():
			return max(self.qtable[self.currentState].values())
		else:
			return 0

	def predictedOpponentsMove(self):
		if self.isValid():
			return [max(self.qtable[self.currentState].items(), key = itemgetter(1))[0][1]]
		else:
			return ['C', 'D']

	def setProbability(self, p):
		self.probability = p

	