from agents import agent
from metaAgent import metaAgent
from strategies import strategy, strategyTypes
import matplotlib.pyplot as plt
import random

agentType = {
	'Meta': 0,
	'Learner': 1,
}

class generation():
	
	def __init__(self, iterations, strategiesList, agentTypes):

		self.payoffMatrix = {"DD":1, "CC":3, "CD":0, "DC":5}
		self.agents = [self.createAgent(x) for x in agentTypes]
		self.opponents = [strategy(x) for x in strategiesList]
		self.iterations = iterations
		self.learntPolicies = []
		

	def createAgent(self, agentType):
		if agentType == 'Learner':
			iterations_exploring = 1000
			T = pow(.01, 1.0/iterations_exploring)
			alpha = .5
			gamma = .95
			numHistoryMoves = random.choice([1,2,3])
			numHistoryMoves = 1
			agentx = agent(numHistoryMoves, alpha, gamma, T, self.payoffMatrix)
		elif agentType == 'Meta':
			agentx = metaAgent(self.learntPolicies, self.payoffMatrix)
		
		return agentx

	def runOneMove(self, agentx, opponentx, iterationNumber):
		agentsMove = agentx.agentsMove(iterationNumber)
		responseMove = opponentx.next()

		agentx.updateAgent(agentsMove, responseMove)
		opponentx.addAgentsMove(agentsMove)


	def runIteration(self, i):
		for agentx, opponentx in zip(self.agents, self.opponents):
			self.runOneMove(agentx, opponentx, i)

	def runGeneration(self):
		for i in range(self.iterations):
			self.runIteration(i)

	def addLearntPolicies(self):
		for agentx in self.agents:
			if agentx.agentType == "Learner":
				self.learntPolicies.append([agentx.packQTable(), agentx.numHistoryMoves])

	def nextGeneration(self, iterations, strategiesList, agentTypes):
		self.agents = [self.createAgent(x) for x in agentTypes]
		self.opponents = [strategy(x) for x in strategiesList]
		self.iterations = iterations

	def afterSimulationAnalysis(self):
		for mAgent in [x for x in self.agents if x.agentType == 'Meta']:
			mAgent.printRewards()





def runOneToOne():
	stra = 'TFT'
	opponentx = strategy(stra)

	iterations_exploring = 5000
	T = pow(.01, 1.0/iterations_exploring)
	alpha = .5
	gamma = .95
	numHistoryMoves = 2
	payoffMatrix = {"DD":1, "CC":3, "CD":0, "DC":5}
	agentx = agent(numHistoryMoves, alpha, gamma, T, payoffMatrix)

	for i in range(5000):
		agentsMove = agentx.agentsMove(i)
		responseMove = opponentx.next()

		agentx.updateAgent(agentsMove, responseMove)
		opponentx.addAgentsMove(agentsMove)
		
	agentx.interpretResults()
	iterations, diffs = zip(*agentx.agentsConvergence)

	# plt.plot(iterations, diffs)
	# plt.show()


def main():
	# PSEUDO-CODE
	populationSize = 100
	# strategiesList = [random.choice(strategyTypes.keys()) for x in range(populationSize)]
	strategiesList = strategyTypes.keys()
	agentTypesList = ['Learner' for i in range(9)]
	g = generation(10000, strategiesList, agentTypesList)
	g.runGeneration()
	g.addLearntPolicies()
	
	strategiesList = ['TFTT']
	agentTypesList = ['Meta']
	print len(g.learntPolicies)
	g.nextGeneration(20, strategiesList, agentTypesList)
	g.runGeneration()

	# # g.afterSimulationAnalysis()
	# for ma in g.agents:
	# 	for pa in ma.proxyAgents:
	# 		print pa.rewardSequence, pa.suggestedMoves
	# 		# plt.plot(pa.rewardSequence)
	# # plt.show()

	# next generation of only meta-agents



	




if __name__ == '__main__':
	# main()
	runOneToOne()
