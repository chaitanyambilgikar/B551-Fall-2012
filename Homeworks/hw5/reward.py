from agent import *

class AgentRewardModel:
	"""An action model mapping AgentState,action pairs to rewards.
	States are poses [x,y,z]"""
	def __init__(self,map):
		self.map = map
		self.motionCost = 1.0
		self.hitWallCost = 10.0
		self.hitAgentCost = 100.0
		self.reachGoalReward = 0.0

	def reward(self,prevstate,action,curstate):
                next = next_pose(None,prevstate.mypose,action)
        	if (next[0],next[1]) in [(o[0],o[1]) for o in prevstate.objectPoses.itervalues()]:
                        return -self.hitAgentCost
		if not valid_cell(self.map,(next[0],next[1])):
                        print "Going off map?",prevstate.mypose,action
                        return -self.hitWallCost
                if (next[0],next[1])==prevstate.mygoal:
                        return self.reachGoalReward
		return -self.motionCost
