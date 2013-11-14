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

class AgentSuicidalPolicy(AgentPolicyBase):
	def __init__(self, map):
		AgentPolicyBase.__init__(self,map)

	def closest_average_distance(self,beliefState,s):
                closestDist = 1e100
                for b_obj in beliefState.b_objects.itervalues():
                        #compute the average distance to this object
                        dobj = 0.0
                        for (o,p) in b_obj.iteritems():
                                dobj += p*max(abs(s[0]-o[0]),abs(s[1]-o[1]))
                        closestDist = min(closestDist,dobj)
                return closestDist
	
	def evaluate(self, beliefState):
                best = ('stay',self.closest_average_distance(beliefState,beliefState.mypose))
		for a in valid_actions(self.map,beliefState.mypose):
                        snext = next_pose(self.map,beliefState.mypose,a)
                        d = self.closest_average_distance(beliefState,snext)
                        if d < best[1]:
                                best = (a,d)
                if best[0]=='stay':
                        return 'l'
                return best[0]

class AgentBlockingPolicy(AgentPolicyBase):
	def __init__(self, map, targets=[]):
                self.targets = targets
		AgentPolicyBase.__init__(self,map)

	def closest_blocking_distance(self,beliefState,s):
                closestDist = 1e100
                hitProb = 0
                if self.targets==[]:
                        self.targets = beliefState.b_objects.keys()
                for b_obj in [beliefState.b_objects[t] for t in self.targets]:
                        #compute the distance to the spot right in front of the obstacle
                        dobj = 0.0
                        for (o,p) in b_obj.iteritems():
                                if o[0] == s[0] and o[1] == s[1]:
                                        hitProb += p
                                fwdpos = next_pose(None,o,"f")
                                dobj += p*max(abs(s[0]-fwdpos[0]),abs(s[1]-fwdpos[1]))
                        closestDist = min(closestDist,dobj)
                return closestDist + hitProb*10
	
	def evaluate(self, beliefState):
                best = ('stay',self.closest_blocking_distance(beliefState,beliefState.mypose))
		for a in valid_actions(self.map,beliefState.mypose):
                        snext = next_pose(self.map,beliefState.mypose,a)
                        d = self.closest_blocking_distance(beliefState,snext)
                        if d < best[1]:
                                best = (a,d)
                if best[0]=='stay':
                        return 'l'
                return best[0]

def steer_toward(pose,target):
        #TODO (HW6): a function like this might be useful to implement...
        x = pose[0] - target[0]
        y = pose[1] - target[1]
        iface = pose[2]
        #start checking

        if (x > 0 and y > 0):
                #he is to our southwest
                if (iface == 'e' or iface == 'se'):
                        return 'r'
                elif (iface =='s'):
                        return 'fr'
                elif (iface == 'sw'):
                        return 'f'
                elif (iface == 'w'):
                        return 'fl'
                elif (iface == 'nw' or iface == 'n' or iface == 'ne'):
                        return 'l'
        elif (x > 0 and y == 0):
                #target to west
                if (iface == 'w'):
                        return 'f'
                elif (iface == 'nw'):
                        return 'fl'
                elif (iface == 'sw'):
                        return 'fr'
                elif (iface == 's' or iface == 'se' or iface == 'e'):
                        return 'r'
                elif (iface == 'n' or iface == 'ne'):
                        return 'l'
        elif ( x > 0 and y < 0 ):
                #target to nw
                if (iface == 'nw'):
                        return 'f'
                elif (iface == 'n'):
                        return 'fl'
                elif (iface == 'w'):
                        return 'fr'
                elif (iface == 'ne' or iface == 'e' or iface == 'se'):
                        return 'l'
                elif (iface == 's' or iface == 'sw'):
                        return 'r'
        elif (x == 0 and y > 0):
                #target to south
                if (iface == 's'):
                        return 'f'
                elif (iface == 'se'):
                        return 'fr'
                elif (iface == 'sw'):
                        return 'fl'
                elif (iface =='w' or iface == 'nw'):
                        return 'l'
                elif (iface == 'n' or iface == 'ne' or iface == 'e'):
                        return 'r'
        elif (x ==0 and y == 0):
                return 'stay'
        elif (x == 0 and y < 0):
                #target to north
                if (iface == 'n'):
                        return 'f'
                elif (iface == 'nw'):
                        return 'fr'
                elif (iface == 'ne'):
                        return 'fl'
                elif (iface == 'w' or iface == 'sw'):
                        return 'r'
                elif (iface == 'e' or iface == 'se' or iface == 's'):
                        return 'l'
        elif (x < 0 and y > 0):
                #target at south east
                if (iface == 'se'):
                        return 'f'
                elif (iface == 'e'):
                        return 'fr'
                elif (iface == 's'):
                        return 'fl'
                elif (iface == 'ne' or iface == 'n' or iface == 'nw'):
                        return 'r'
                elif (iface == 'w' or iface == 'sw'):
                        return 'l'
        elif (x < 0 and y == 0):
                #target to east
                if (iface == 'e'):
                        return 'f'
                elif (iface == 'ne'):
                        return 'fr'
                elif(iface == 'se'):
                        return 'fl'
                elif (iface == 'n' or iface == 'nw' or iface == 'w'):
                        return 'r'
                elif (iface == 'sw' or iface == 's'):
                        return 'l'
        elif ( x < 0 and y < 0):
                #target to northeast
                if (iface == 'ne'):
                        return 'f'
                elif (iface == 'n'):
                        return 'fr'
                elif (iface == 'e'):
                        return 'fl'
                elif (iface == 'nw' or iface == 'w' or iface == 'sw'):
                        return 'r'
                elif (iface == 's' or iface == 'se'):
                        return 'l'
        

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
                dist = {}

                for x in goals:
                        dist[x] = distance2(beliefState.mypose,x)
                if len(path) > 1:
                        return steer_toward(beliefState.mypose,path[1])
                else:
                        return steer_toward(beliefState.mypose,min(dist))
                #TODO (HW6 Question 1): replace this line with something more
 		#sensible
                

class AgentCollisionAvoidingPolicy(AgentPolicyBase):
	"""A policy that avoids collisions with objects within some range"""
	def __init__(self,map):
		AgentPolicyBase.__init__(self,map)
		self.repulsive_range = 4
                self.sum = 0

        def local_search(self,beliefState):
                successors = []
                
		for a in enumerate_map_cells(self.map):
                        potential = self.potential_field_eval(beliefState,a)
                        successors.append((potential,a))
                self.sum += self.potential_field_eval(beliefState,(beliefState.mypose[0],beliefState.mypose[1]))
                print self.sum
                return min(successors)[1]
	
	def evaluate(self,beliefState):
                #TODO (HW6 Question 2): replace this line with your own code
                
                return steer_toward(beliefState.mypose,self.local_search(beliefState))
        
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
                self.prand = 0.05

                self.prevturn = None
                self.repulsive_range = 4

	
	def evaluate_for_goal(self,beliefState):
                pos = beliefState.mypose[:2]
                
                goals = [pgoal for pgoal in beliefState.b_goal]
                
                if not goals:
                        #return random.choice(valid_actions(self.map, beliefState.mypose))
                        choice = random.choice(valid_actions(self.map, beliefState.mypose))
                        nextst = next_pose(beliefState.mypose,choice)
                        dist = distance2(beliefState.mypose,nextst)
                        return (dist,choice)
                path = search_path(self.map, pos, goals)
                if not path or random.random() < self.prand:
                        #return random.choice(valid_actions(self.map, beliefState.mypose))
                        ch = random.choice(valid_actions(self.map, beliefState.mypose))
                        #nxt = next_pose(beliefState.mypose,ch)
                        #d = distance2(beliefState.mypose,nxt)
                        #return (d,ch)
                dist = {}
                for x in goals:
                        dist[x] = distance2(beliefState.mypose,x)
                if len(path) > 1:
                        return (dist[path[1]],steer_toward(beliefState.mypose,path[1]))
                else:
                        return (dist[min(dist)],steer_toward(beliefState.mypose,min(dist)))
        def local_search(self,beliefState):
                successors = []
        
                for a in enumerate_map_cells(self.map):
                        potential = self.potential_field_eval(beliefState,a)
                        successors.append((potential,a))
                return (min(successors)[0],min(successors)[1])

        def potential_field_eval(self,beliefState,mypose):
                psum = 0.0
                
                for b_obj in beliefState.b_objects.itervalues():

                        for (o,p) in b_obj.iteritems():

                                d = abs(o[0]-mypose[0])+abs(o[1]-mypose[1])
                                if d < self.repulsive_range:
                                        psum += p*pow(self.repulsive_range-d,2)
                return psum
        def evaluate_for_collision(self,beliefState):
                
                (a,b) = self.local_search(beliefState)
                return (a,steer_toward(beliefState.mypose,b))

        def evaluate(self, beliefState):
		for_goal = self.evaluate_for_goal(beliefState)
                for_collision = self.evaluate_for_collision(beliefState)
                
                if (for_goal[0] > for_collision[0]):
                        return for_goal[1]
                else:
                        return for_collision[1]
	
	def advance(self):
		pass

