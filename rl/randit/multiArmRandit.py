from cProfile import label
from cmath import inf, sqrt
import numpy as np
import random
import matplotlib.pyplot as plt
from math import log
from math import sqrt

def getAverageReward(rewards):
	areward = []
	nowsum = 0
	for i, r in enumerate(rewards):
		nowsum += r
		areward.append(nowsum/(i+1))
	return areward

def drawReward(stepNum, rewards1, rewards2, tp):
	stepNums = [x for x in range(1, stepNum+1)]
	plt.plot(stepNums, getAverageReward(rewards1), '.', label='egreedy', markersize=2)
	plt.plot(stepNums, getAverageReward(rewards2), '.', label='UCB', markersize=2)
	plt.xlabel('steps')
	plt.ylabel('rewards')
	plt.legend()
	plt.savefig(tp)



class EGreedy():
	def __init__(self, randitnum, e, delta):
		self.e = e
		self.delta = delta
		self.randitnum = randitnum
		self.Q = {k:0 for k in range(1, randitnum+1)}
		self.aNums = {k:0 for k in range(1, randitnum+1)}
		self.action = None
		self.reward = None
		self.step = 0
	def getReward(self):
		return np.random.normal(self.action, self.delta)
	def greedy(self):
		return np.argmax([self.Q[k] for k in self.Q]) + 1
	def getAction(self):
		action = 0
		if random.random() < self.e:
			action = random.randint(1, self.randitnum)
		else:
			action = self.greedy()
		return action
	def updateQ(self):
		self.Q[self.action] = self.Q[self.action] + 1/self.aNums[self.action] * (self.reward - self.Q[self.action])
	def run(self, run_step):
		rewards = []
		actions = []
		for step in range(1, run_step+1):
			# print(self.Q)
			self.step += 1
			action = self.getAction()
			self.aNums[action] += 1
			self.action = action
			actions.append(action)
			self.reward = self.getReward()
			rewards.append(self.reward)
			self.updateQ()
		return rewards
		# return actions
	def reset(self):
		self.Q = {k:0 for k in range(1, self.randitnum+1)}
		self.aNums = {k:0 for k in range(1, self.randitnum+1)}
		self.action = None
		self.reward = None
		self.step = 0


class UCB():
	def __init__(self, randitnum, c, delta):
		self.c = c
		self.delta = delta
		self.randitnum = randitnum
		self.Q = {k:1e10 for k in range(1, randitnum+1)}
		self.aNums = {k:0 for k in range(1, randitnum+1)}
		self.action = None
		self.reward = None
		self.step = 0
	def getReward(self):
		return np.random.normal(self.action, self.delta)
	def ucb(self):
		return np.argmax([self.Q[k] + self.c*sqrt(log(self.step/max(self.aNums[k], 0.0001))) for k in self.Q]) + 1
	def getAction(self):
		action = self.ucb()
		return action
	def updateQ(self):
		if self.aNums[self.action] == 0:
			self.Q = self.reward
		else:
			self.Q[self.action] = self.Q[self.action] + 1/self.aNums[self.action] * (self.reward - self.Q[self.action])
	def run(self, run_step):
		rewards = []
		actions = []
		for step in range(1, run_step+1):
			# print(self.Q)
			self.step += 1
			action = self.getAction()
			self.aNums[action] += 1
			self.action = action
			self.reward = self.getReward()
			actions.append(action)
			rewards.append(self.reward)
			self.updateQ()
		return rewards
		# return actions
	def reset(self):
		self.Q = {k:0 for k in range(1, self.randitnum+1)}
		self.aNums = {k:0 for k in range(1, self.randitnum+1)}
		self.action = None
		self.reward = None
		self.step = 0






if __name__ == "__main__":
	steps = 1000
	randitnum = 15
	med1 = EGreedy(randitnum, 0.1, 1)
	rewards1 = med1.run(steps)
	med2 = UCB(randitnum, 0.1, 1)
	rewards2 = med2.run(steps)
	drawReward(steps, rewards1=rewards1, rewards2=rewards2, tp='test.jpg')
