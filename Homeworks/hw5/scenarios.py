from agent import *
from multiagent import *
from policy import *

class Scenario(object):
	NAME = 'Base Scenario'
	
	# Should return map,sim,continue_condition when overridden
	# continue_condition can be None, an integer, or a boolean test
	# if it is None, the sim will run forever.
	# if it is an int n, the sim will run for exactly n iterations
	# if it is a boolean test (taking parameter 'sim')
	def make_sim(cls):
		return None

#self.map = [[True]*6]*6
		#starts = {'A':(0,0,'n'),'B':(5,5,'s'),'C':(0,5,'n')}
		#goals = {'A':(5,5),'B':(0,0),'C':(5,0)}
		##starts = {'A':(0,5,'n')}
		##goals = {'A':(5,0)}
		#self.sim = MultiAgentSimulator(self.map,starts,goals)
		#self.sim.agents['A'].policy = AgentOpenLoopPolicy(self.map,['f']*3+['r']*4)
		#self.sim.agents['B'].policy = AgentOpenLoopPolicy(self.map,['f']*3+['r']*4)
		#self.sim.agents['C'].policy = AgentGoalPursuingPolicy(self.map, 0.05)

class GoalTestScenario(Scenario):
	NAME = 'Goal Update Test 1'
	
	def make_sim(cls):
		map = [[True]*3]*7
		starts = {'A':(4,0,'n')}
		goals = {'A':(0,0)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentOpenLoopPolicy(map,['stay']+
								['r']*2+['l']*4+['r']*2+['f']*2+ \
								['l']*4+['r']*2+['f']*2+['l']*2+ \
								['r']*2+['f']*2+['l']*2+['f']*2+ \
                                                                ['l']*2+['f']*3, False)
		return map,sim,lambda(sim):not sim.agents['A'].policy.done()

class ObjSenseScenario1(Scenario):
	NAME = 'Object Update Test 1'
	
	def make_sim(cls):
		map = [[True]*5]*9
		starts = {'A':(3,0,'n'), 'B':(0,2,'e')}
		goals = {'A':(3,0), 'B':(0,0)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentOpenLoopPolicy(map, [])
		sim.agents['B'].policy = AgentOpenLoopPolicy(map, ['f','f','l','l','f','r','r']+['f']*6 + ['stay']*10)
		return map,sim,lambda(sim):not sim.agents['B'].policy.done()

class ObjSenseScenario2(Scenario):
	NAME = 'Object Update Test 2'
	
	def make_sim(cls):
		map = [[True]*5]*7
		starts = {'A':(0,2,'e'), 'B':(6,3,'w')}
		goals = {'A':(6,2), 'B':(0,3)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentOpenLoopPolicy(map, ['stay']+['f']*6)
		sim.agents['B'].policy = AgentOpenLoopPolicy(map, ['stay']+['f']*6)
		return map,sim,10

class ObjSenseScenario3(Scenario):
	NAME = 'Object Update Test 3'
	
	def make_sim(cls):
		map = [[True]*5]*9
		starts = {'A':(3,0,'n'), 'B':(8,3,'w') ,'C':(0,0,'e')}
		goals = {'A':(3,0), 'B':(0,0), 'C':(0,0)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentOpenLoopPolicy(map, [])
		sim.agents['B'].policy = AgentOpenLoopPolicy(map, ['stay']+['f']*8+['l']*2+['f']*2+['stay']*10)
		sim.agents['C'].policy = AgentOpenLoopPolicy(map, ['stay']*11 + ['f','f','l','l','f','r','r']+['f']*6 + ['stay']*10)
		return map,sim,lambda(sim):not sim.agents['C'].policy.done()

class GoalSeekScenario1(Scenario):
	NAME = 'Goal Seeking Scenario 1'
	
	def make_sim(cls):
		map = [[True]*3]*7
		starts = {'A':(4,0,'n')}
		goals = {'A':(0,0)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentGoalPursuingPolicy(map,0.05)
		return map,sim,None

class GoalSeekScenario2(Scenario):
	NAME = 'Goal Seeking Scenario 2'
	
	def make_sim(cls):
		map = [[True]*3]*7
		starts = {'A':(4,0,'n')}
		goals = {'A':(0,0)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentGoalPursuingPolicy(map,0.0)
		return map,sim,None

class GoalSeekScenario3(Scenario):
	NAME = 'Goal Seeking Scenario 3'
	
	def make_sim(cls):
		map = [[True]*3]*7
		starts = {'A':(4,0,'n')}
		goals = {'A':(5,2)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentGoalPursuingPolicy(map,0.0)
		return map,sim,None


class AvoidScenario1(Scenario):
	NAME = 'Avoidance Scenario 1'
		
	def make_sim(cls):
		map = [[True]*3]*5
		starts = {'A':(0,1,'e'), 'B':(4,1,'w')}
		goals = {'A':(4,1), 'B':(0,1)}
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentObstacleAvoidingPolicy(map)
		#sim.agents['B'].policy = AgentOpenLoopPolicy(map, ['f']*4 + ['stay']*4 + ['r']*4,True)
		sim.agents['B'].policy = AgentSubgoalPolicy(map, [(0,0),(0,2),(4,2),(4,0)],True)
		return map,sim,100
		
class AvoidScenario2(Scenario):
	NAME = 'Avoidance Scenario 2'
		
	def make_sim(cls):
		map = [[True]*5]*5
		starts = {'A':(0,2,'e'), 'B':(4,2,'w'), 'C':(2,2,'n')}
		goals = {'A':(4,2), 'B':(0,2), 'C':(2,2) }
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentObstacleAvoidingPolicy(map)
		sim.agents['B'].policy = AgentObstacleAvoidingPolicy(map)
		#sim.agents['C'].policy = AgentRandomObstacleAvoidingPolicy(map)
		#sim.agents['C'].policy = AgentOpenLoopPolicy(map,['f']*4 + ['stay']*4 + ['l']*2,True)
		sim.agents['C'].policy = AgentSubgoalPolicy(map,[(0,0),(4,4),(0,4),(4,0)],True)
		return map,sim,100

class HallwayScenario1(Scenario):
	NAME = 'Hallway Scenario 1'
		
	def make_sim(cls):
		map = [[True]*3 for i in xrange(7)]
		map[0][0] = map[1][0] = False
		map[0][2] = map[1][2] = False
		map[5][0] = map[6][0] = False
		map[5][2] = map[6][2] = False
		starts = {'A':(0,1,'e'), 'B':(6,1,'w')}
		goals = {'A':(6,1), 'B':(0,1) }
		sim = MultiAgentSimulator(map, starts, goals)
		sim.agents['A'].policy = AgentStudentPolicy(map)
		sim.agents['B'].policy = AgentStudentPolicy(map)
		return map,sim,100
