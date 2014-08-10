from operator import itemgetter
import itertools
import copy
import sys
from myFunctions import weighted_choice
from math import exp, log


class agent():
	
	def __init__(self, numHistoryMoves, alpha, gamma, T, rewardStructure):
		self.agentType = 'Learner'
		self.numHistoryMoves = numHistoryMoves
		self.gamma = gamma
		self.alpha = alpha
		self.T = T

		self.numStates = 0
		self.states = {} # a two way hash map or reverse map<->
		self.initializeStates()

		self.qtable = {} # a doubly linked list; a dict of dicts in python terms
		self.initializeQTable()

		self.rewardStructure = copy.deepcopy(rewardStructure)
		self.checkRewardStructure()
		
		self.actions = ['D', 'C'] # not used anywhere yet!
		self.currentState = '0'
		self.nextState = '0'

		self.agentsConvergence = []
		self.pOptimalMax = dict([(str(i), 0) for i in range(self.numStates)])

	def packQTable(self):
		genericQTable = {}
		for i in range(self.numStates):
			state = self.states[str(i)]
			genericQTable[state] = copy.deepcopy(self.qtable[str(i)])
		return genericQTable

	def initializeStates(self):
		temp = []
		for i in range(self.numHistoryMoves+1):
			temp.extend(["".join(seq) for seq in itertools.product("CD", repeat=i)])

		count = 0
		for i, x in enumerate(temp):
			for j, y in enumerate(temp):
				if len(y)==len(x):
					if count == 0:
						self.states[''] = '0'
						self.states['0'] = ''
					else:
						self.states[x + '-' + y] = str(count)
						self.states[str(count)] = x + '-' + y
					count = count + 1
		self.numStates = len(self.states.keys())/2
		assert len(self.states.keys())%2==0


	def initializeQTable(self):
		for x in range(self.numStates):
			self.qtable[str(x)] = {}
			# add those moves in the qtable with 0 q-values
			self.qtable[str(x)]["CC"] = 0
			self.qtable[str(x)]["DC"] = 0
			self.qtable[str(x)]["CD"] = 0
			self.qtable[str(x)]["DD"] = 0

	def checkRewardStructure(self):
		try:
			self.rewardStructure['CC'] + self.rewardStructure['DD'] + self.rewardStructure['CD'] + self.rewardStructure['DC']
		except KeyError as e:
			print "Enter Correct Reward Structure", e, "not found."
			sys.exit()

	def getNextState(self, agentsMove, opponentsMove):
		# strCS is the internal representation string for Current State, e.g. 'CDCDCC-CDDDCD'
		strCS = self.states[self.currentState]
		try:
			agentsHist, opponentsHist = strCS.split('-')
		except ValueError as e:
			agentsHist = ''
			opponentsHist = ''
		agentsHist = (agentsHist + agentsMove)[-self.numHistoryMoves:]
		opponentsHist = (opponentsHist + opponentsMove)[-self.numHistoryMoves:]
		strNS = agentsHist + '-' + opponentsHist
		try:
			self.nextState = self.states[strNS]
		except KeyError as e:
			print 'KeyError Problem with nextState', e,'not found.'
			sys.exit()

	def updateAgent(self, agentsMove, opponentsMove):
		self.getNextState(agentsMove, opponentsMove)
		move = agentsMove+opponentsMove
		# print move
		# update the current state q-value
		# try:
		deltaValue = self.rewardStructure[move]
		deltaValue = deltaValue + self.gamma * max(self.qtable[self.nextState].values())
		# except KeyError as e:
			# print 'KeyError, please enter valid move from ["CC", "DD", "CD", "DC"]',e, 'not found in reward keys'
			# sys.exit()

		self.qtable[self.currentState][move] = (1-self.alpha)*(self.qtable[self.currentState][move]) + self.alpha*deltaValue
		self.currentState = self.nextState

	def agentsMove(self, n):

		keys = self.qtable[self.currentState].keys()
		values = self.qtable[self.currentState].values()
		if sum(values)>0:
			values = [x/sum(values) for x in values]

		# Boltzman Method for finding new probabilities
		t = pow(self.T, n)
		
		# this condition is taken from the paper #multi-agent reinforcment learning in the IPD
		if t > .01:
			values = [exp(x/t) for x in values]
			values = [x/sum(values) for x in values]
			nextMove = weighted_choice(zip(keys,values))
		else:
			nextMove = max(self.qtable[self.currentState].items(), key = itemgetter(1))[0]

		# fill agents Diagnostics
		if n%10==0:
			self.gaugeAgentsConvergence(n)

		return nextMove[0]

	def interpretResults(self):
		for i in range(self.numStates):
			if sum(self.qtable[str(i)].values()) > -10:
				print self.states[str(i)], 
				print max(self.qtable[str(i)].items(), key = itemgetter(1))[0][0],
				print self.qtable[str(i)],
				print '\n'

	def getOptimalPolicies(self):
		states = [self.states[str(i)] for i in range(self.numStates)]
		policies = [max(self.qtable[str(i)].items(), key = itemgetter(1))[0][0] for i in range(self.numStates)]
		return zip(states, policies)

	def getMaxValues(self):
		values = [(str(i), max(self.qtable[str(i)].values())) for i in range(self.numStates)]
		return dict(values)

	def gaugeAgentsConvergence(self, n):
		ndict = self.getMaxValues()
		diff = sum([abs(self.pOptimalMax[str(i)] - ndict[str(i)]) for i in range(self.numStates)])
		self.agentsConvergence.append([n, diff])
		self.pOptimalMax = copy.deepcopy(self.getMaxValues())


def testFunctions():
	iterations_exploring = 5000
	T = pow(.01, 1.0/iterations_exploring)
	alpha = .5
	gamma = .95
	numHistoryMoves = 1
	payoffMatrix = {"DD":1, "CC":3, "CD":0, "DC":5}
	a = agent(numHistoryMoves, alpha, gamma, T, payoffMatrix)
	# print a.states
	# a.qtable['0']['CC'] = 7
	# a.qtable['0']['DC'] = 10
	# a.qtable['0']['CD'] = 1
	# a.qtable['0']['DD'] = 1
	last_move = 'C'
	for i in range(a.numStates*1000):
		move = a.agentsMove(i)	
		a.updateQModel(move, last_move)
		last_move = move
	# a.interpretResults()

if __name__ == '__main__':
	import random
	testFunctions()