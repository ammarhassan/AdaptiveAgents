import random

strategyTypes = {
			
			 "TFT" : 1, 
			 "TFTT" : 2,
			 "STFT" : 3,
			 "TTFT" : 4,
			 "RAND" : 5,
			 "ALLC" : 6,
			 "ALLD" : 7,
			 "GRIM" : 8,
			 "PAVLOV" :9,
		}

class strategy():
	def __init__(self, typ):
		
		self.playedHistory = []
		self.responseHistory = []
		try:
			strategyTypes[typ]
			self.typ = typ
			self.grimTrigger = 0
		except (KeyError):
			self.typ = "TFT"

	def next(self):
		self.checkErrors()
		if self.typ == "TFT":
			if len(self.responseHistory)==0:
				play = "C"
			else:
				play = self.responseHistory[-1]

		elif self.typ == "TFTT":
			if len(self.responseHistory) < 2:
				play = "C"
			else:
				play = "D" if self.responseHistory[-1] =="D" and self.responseHistory[-2] == "D" else "C"

		elif self.typ == "STFT":
			if len(self.responseHistory)==0:
				play = "D"
			else:
				play = self.responseHistory[-1]

		elif self.typ == "TTFT":
			if len(self.responseHistory)==0:
				play = "C"
			elif len(self.responseHistory)>1 and self.responseHistory[-2]=="D":
				play = "D"
			else:
				play = self.responseHistory[-1]

		elif self.typ == "RAND":
			play = random.choice(["D", "C"])

		elif self.typ == "ALLC":
			play = "C"

		elif self.typ == "ALLD":
			play = "D"

		elif self.typ == "GRIM":
			if self.grimTrigger:
				play = "D"
			elif len(self.responseHistory)> 0 and self.responseHistory[-1]=="D":
				self.grimTrigger = 1
				play = "D"
			else:
				play = "C"

		elif self.typ == "PAVLOV":
			if len(self.responseHistory) == 0:
				play = "C"
			elif self.responseHistory[-1] == "D":
				if self.playedHistory[-1] == "D":
					play = "C"
				else:
					play = "D"
			elif self.responseHistory[-1] == "C":
				play = self.playedHistory[-1]

		self.playedHistory.append(play)
		return play

				
	def addAgentsMove(self, response):
		self.responseHistory.append(response)

	def checkErrors(self):
		if len(self.responseHistory) == len(self.playedHistory):
			return 1
		elif len(self.responseHistory) == len(self.playedHistory) - 1:
			raise lenghtMismatch(1)
		elif len(self.responseHistory) != len(self.playedHistory):
			raise lenghtMismatch(len(self.responseHistory) - len(self.playedHistory))


class lenghtMismatch(Exception):
	def __init__(self, mismatch):
		self.value = mismatch
	def __str__(self):
		if self.value == 1:
			return repr("Please add the response move.")
		else:
			return repr("Difference of " + str(self.value) + "in length, please debug.")
	



if __name__ == '__main__':
	stra = 'TFT'
	s = strategy(stra)
	print 'strategy', stra

	for i in range(10):
		agentsMove = random.choice(['C', 'D'])
		opponentsMove = s.next()

		s.addAgentsMove(agentsMove)
		print agentsMove, opponentsMove





