from gridmap import *
from agent import *
from reward import *

def print_map(map, state, goals):
	for row in range(len(map[0])):
		for col in range(len(map)):
			printed = False
			for agent in state:
				if state[agent][:2] == (row,col):
					print agent+' ',
					printed = True
					break
			if printed:
				continue
			for agent in goals:
				if goals[agent] == (row,col):
					print 'G'+agent,
					printed = True
					break
			if printed:
				continue
			if map[row][col]:
				print '__',
			else:
				print '--',
		print
	print

class MultiAgentSimulator:
	def __init__(self,map,agentStarts,agentGoals):
		self.map = map
		self.agents = dict()
		self.agentSensors = dict()
		self.agentRewardFunctions = dict()
		#initialize agents
		for name,startpose in agentStarts.iteritems():
			self.agents[name] = Agent(name,map)
			b0 = AgentBeliefState(startpose)
			b0.init_uniform_goals(map)
			names = agentStarts.keys()
			names.remove(name)
			#initialize starting belief
			b0.init_uniform_objects(map,names)
			self.agents[name].currentBelief = b0
			#unform agent behavior models
			self.agents[name].agentBehaviorModels = dict((n,SingleAgentBehaviorModel(map)) for n in names)
			#be nice and let every agent's sensor model be identical to the true sensor model
			sensorModel = AgentSensorModel(GoalSensorModel(),dict((n,ObjectSensorModel(n)) for n in names))
			self.agentSensors[name] = sensorModel
			self.agents[name].set_sensor_model(sensorModel)
			#be nice and let every agent have the same reward model
			self.agentRewardFunctions[name] = AgentRewardModel(map)
		#store true state, which is unknown to agents
		self.currentState = agentStarts.copy()
		#store true goals, which are unknown to agents
		self.agentGoals = agentGoals.copy()
		#pick an arbitrary move order
		self.moveorder = agentStarts.keys()
		#store history of state,action,observations,rewards in order for each agent
		self.histories = dict((name,[]) for name,state in agentStarts.iteritems())

	def step(self):
		for agent in self.moveorder:
			others = self.currentState.copy()
			del others[agent]
			if len(self.histories[agent]) > 0:
				#simulate sensing for this agent using true state
				truestate = AgentState(self.currentState[agent],self.agentGoals[agent],others)
				obs = self.agentSensors[agent].sample(truestate)
				#compute reward
				prevothers = self.histories[agent][-2].copy()
                                del prevothers[agent]
				prevstate = AgentState(self.histories[agent][-2][agent],self.agentGoals[agent],prevothers)
				reward = self.agentRewardFunctions[agent].reward(prevstate,self.histories[agent][-1],truestate)
				#perform sensing input
				self.agents[agent].sense(obs,reward)
				assert (self.currentState[agent] == self.agents[agent].currentBelief.mypose)
				assert (self.agentGoals[agent] in self.agents[agent].currentBelief.b_goal)
				self.histories[agent].append(obs)
				self.histories[agent].append(reward)
			#store current state in the agent history
			self.histories[agent].append(self.currentState.copy())
			#run agent program 
			a = self.agents[agent].act()
			self.histories[agent].append(a)
			#simulate actuation for this agent
			nextpose = next_pose_with_objects(self.map,self.currentState[agent],a,others)
			self.currentState[agent] = nextpose

        def give_omniscient_state(self,agent):
                #give goal cell
                self.agents[agent].currentBelief.b_goal = dict([(self.agentGoals[agent],1.0)])
                #give object states
                for (other,dist) in self.agents[agent].currentBelief.b_objects.items():
                        for k in dist.keys():
                                dist[k] = 0.0
                        dist[self.currentState[other]] = 1.0
                return
	
if __name__ == '__main__':
        import policy
	map = [[True]*6]*6
	starts = {'A':(0,0,'n'),'B':(5,5,'s'),'C':(0,5,'n')}
	goals = {'A':(5,5),'B':(0,0),'C':(5,0)}
	sim = MultiAgentSimulator(map,starts,goals)
	#sim.agents['A'].policy = AgentOpenLoopPolicy(map,['f']*3+['r']*4)
	sim.agents['A'].policy = policy.AgentGoalPursuingPolicy(map,0.8)
	sim.agents['B'].policy = AgentOpenLoopPolicy(map,['f']*3+['r']*4)
	#sim.agents['C'].policy = AgentGoalPursuingPolicy(map, 0.05)
	sim.agents['C'].policy = policy.AgentGoalPursuingPolicy(map, 0.8)
	for iters in range(100):
		if sim.currentState['C'][:2] == goals['C']:
			break
		print 'State'
		print_map(map,sim.currentState,goals)
		print 'A: Believed goals:',sorted(sim.agents['A'].currentBelief.b_goal.keys())
		sim.step()
		if len(sim.histories['A']) > 2:
			print 'A: Goal observed',sim.histories['A'][-4].goalvisible
			print 'A: Agent observed',sim.histories['A'][-4].objectvisible
