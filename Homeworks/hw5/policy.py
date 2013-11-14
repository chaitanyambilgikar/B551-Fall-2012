from agent import *

class AgentRandomPolicy(AgentPolicyBase):
	"""A uniform random policy"""
	
	def __init__(self,map):
		AgentPolicyBase.__init__(self,map)

	def evaluate(self,beliefState):
		return random.choice(actionNames)

class AgentRandomObstacleAvoidingPolicy(AgentPolicyBase):
	"""A policy that selects uniformly from actions that don't bump into
	walls or other objects"""
	def __init__(self,map):
		AgentPolicyBase.__init__(self,map)
		
	def evaluate(self,beliefState):
		return random.choice(valid_actions(self.map,beliefState.mypose))

class AgentSubgoalPolicy(AgentPolicyBase):
	"""A policy that seeks one subgoal after another, greedily"""
	
	def __init__(self,map,goallist,repeat=False):
		AgentPolicyBase.__init__(self,map)
		self.goallist = goallist
		self.progression = 0
		self.repeat = repeat
		self.hit = False

	def evaluate(self,beliefState):
		if self.progression < len(self.goallist):
                        #advance subgoal
                        if self.goallist[self.progression] == beliefState.mypose[:2]:
                                self.progression += 1
                                if self.repeat and self.progression >= len(self.goallist):
                                        self.progression=0
                                else:
                                        return 'stay'
                        goal = self.goallist[self.progression]
                        #Get closer to the subgoal
                        abest = 'r'
                        best = distance2(beliefState.mypose,goal)
                        for a in actionNames:
                                snext = next_pose(self.map,beliefState.mypose,a)
                                if distance2(snext,goal) < best:
                                        best = distance2(snext,goal)
                                        abest = a
                        return abest
		return actionNames[0]
                        
        def done(self):
                return self.progression >= len(self.goallist)

def steer_toward(pose,target):
        #TODO (HW6): a function like this might be useful to implement...
        pass

class AgentGoalPursuingPolicy(AgentPolicyBase):
	def __init__(self, map, prand):
		AgentPolicyBase.__init__(self,map)
		self.prand = prand
		self.prevturn = None
	
	def evaluate(self, beliefState):
		pos = beliefState.mypose[:2]
		goals = [pgoal for pgoal in beliefState.b_goal]
		if not goals:
			return random.choice(valid_actions(self.map, beliefState.mypose))
		path = search_path(self.map, pos, goals)
		if not path or random.random() < self.prand:
 			return random.choice(valid_actions(self.map, beliefState.mypose))

                #TODO (HW6 Question 1): replace this line with something more
 		#sensible
                return 'stay'


class AgentObstacleAvoidingPolicy(AgentPolicyBase):
	"""A policy that avoids obstacles within some range"""
	def __init__(self,map):
		AgentPolicyBase.__init__(self,map)
		self.repulsive_range = 3

        def local_search(self,beliefState):
                successors = []
		for a in valid_actions(self.map,beliefState.mypose):
                        snext = next_pose(None,beliefState.mypose,a)
                        potential = self.potential_field_eval(beliefState,snext)
                        successors.append((potential,snext,a))
                return min(successors)[2]
	
	def evaluate(self,beliefState):
                #TODO (HW6 Question 2): replace this line with your own code
                return self.local_search(beliefState)
        
        def potential_field_eval(self,beliefState,mypose):
                psum = 0.0
                for b_obj in beliefState.b_objects.itervalues():
                        for (o,p) in b_obj.iteritems():
                                d = abs(o[0]-mypose[0])+abs(o[1]-mypose[1])
                                if d < self.repulsive_range:
                                        psum += p*pow(self.repulsive_range-d,2)
                return psum


# TODO (HW6 question 3): Implement your own policy class
class AgentStudentPolicy(AgentPolicyBase):
	"""You should implement this!"""
	
	def __init__(self,map):
		AgentPolicyBase.__init__(self,map)
	
	def evaluate(self, beliefState):
		pass
	
	def advance(self):
		pass

