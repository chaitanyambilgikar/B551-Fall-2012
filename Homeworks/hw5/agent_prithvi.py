from gridmap import *
from distribution import *
import copy
import random
import itertools
from collections import deque
import copy

################
## Useful global values
################

# Actions an agent can perform -- three directional motions, 
# two turns, or remain still
actionNames = ['stay','f','fl','fr','l','r']
# Directions an agent can be facing
directions = ['e','ne','n','nw','w','sw','s','se']
# Map of direction values to their indices in the list
directionMap = zip(directions,range(len(directions)))
# Dict providing direction -> vector mappings to corresponding x,y vectors
directionVectors = {'e':(1,0),'ne':(1,1),'n':(0,1),'nw':(-1,1),'w':(-1,0),'sw':(-1,-1),'s':(0,-1),'se':(1,-1)}
directionVectorMap = dict((v,k) for (k,v) in directionVectors.iteritems())
# If I turn left while facing X, I will be facing Y
directionLeft = {'e':'ne','ne':'n','n':'nw','nw':'w','w':'sw','sw':'s','s':'se','se':'e'}
# Same but reversed
directionRight = dict((v,k) for (k,v) in directionLeft.iteritems())

def next_pose(pose,action):
        """A deterministic action model for a single agent, mapping a
        pose,action pair to next pose.  Poses are tuples (x,y,d)."""
        if action == 'f':
                d = directionVectors[pose[2]]
                candidate = (pose[0]+d[0],pose[1]+d[1],pose[2])
        elif action == 'fl':
                return next_pose(map,next_pose(map,pose,'l'),'f')
        elif action == 'fr':
                return next_pose(map,next_pose(map,pose,'r'),'f')
        elif action == 'l':
                return (pose[0],pose[1],directionLeft[pose[2]])
        elif action == 'r':
                return (pose[0],pose[1],directionRight[pose[2]])
        return pose

def next_pose(map,pose,action):
        """A deterministic action model for a single agent, mapping a
        pose,action pair to next pose.  Poses are tuples (x,y,d)."""
        if action == 'f':
                d = directionVectors[pose[2]]
                candidate = (pose[0]+d[0],pose[1]+d[1])
                if map == None or valid_cell(map,candidate):
                        return (candidate[0],candidate[1],pose[2])
        elif action == 'fl':
                return next_pose(map,next_pose(map,pose,'l'),'f')
        elif action == 'fr':
                return next_pose(map,next_pose(map,pose,'r'),'f')
        elif action == 'l':
                return (pose[0],pose[1],directionLeft[pose[2]])
        elif action == 'r':
                return (pose[0],pose[1],directionRight[pose[2]])
        return pose

def next_pose_with_objects(map,pose,action,objects):
        """The deterministic action model, taking into account that
        the agent might hit another oject"""
        next = next_pose(map,pose,action)
        if (next[0],next[1]) in [(o[0],o[1]) for o in objects.itervalues()]:
                #stay still
                return pose
        return next

def valid_actions(map,pose):
        """Returns a list of actions from actionNames which may be
        taken in the given pose on the given map -- does not take other
        objects into account, just obstacles"""
        res = []
        for a in actionNames:
                if next_pose(None,pose,a) == next_pose(map,pose,a):
                        res.append(a)
        return res

def distance2(a,b):
        return math.sqrt(pow(a[0]-b[0],2) + pow(a[1]-b[1],2))

class AgentState:
        """A class representing the true pose, goal, and other-object poses (?)
        of an agent"""
        def __init__(self,mypose=None,mygoal=None,objectPoses={}):
                self.mypose = mypose
                self.mygoal = mygoal
                self.objectPoses = objectPoses

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
                if (next[0],next[1]) in [(o[0],o[1]) for o in prevstate.objectPoses.itervalues()]:
                        return -self.hitAgentCost
                if not valid_cell(self.map,(next[0],next[1])):
                        print "Going off map?",prevstate.mypose,action
                        return -self.hitWallCost
                if (next[0],next[1])==prevstate.mygoal:
                        return self.reachGoalReward
                return -self.motionCost

def position_visible(pose,position,maxrange):
        """Returns True if the given x,y position is in the agent's
        viewing angle and maxrange at the given pose"""
        l = directionVectors[directionLeft[pose[2]]]
        r = directionVectors[directionRight[pose[2]]]
        d = (position[0]-pose[0],position[1]-pose[1])
        dp_left = l[0]*d[0] + l[1]*d[1]
        dp_right = r[0]*d[0] + r[1]*d[1]
        d_norm2 = d[0]*d[0]+d[1]*d[1]
        return dp_left >= 0 and dp_right > 0 and d_norm2 <= maxrange*maxrange


class GoalSensorModel:
        """Models the probability that an agent senses a goal"""
        def __init__(self,maxrange=100,p_error=0.0):
                """Sets the maximum range and uncertainty of the sensor"""
                self.maxrange = maxrange
                self.p_error = p_error

        def probability_raw(self,pose,goal,value):
                """Given a pose and goal, returns the probability that the
                agent correctly reports seeing or not seeing the goal from
                that pose."""
                if position_visible(pose,goal,self.maxrange) != value:
                        return self.p_error
                return 1.0-self.p_error

        def probability(self,state,value):
                """Same as probability_raw() but with an AgentState
                for pose and goal"""
                if position_visible(state.mypose,state.mygoal,self.maxrange) != value:
                        return self.p_error
                return 1.0-self.p_error

        def sample(self,state):
                """Given an AgentState with goal and pose, returns correct goal sensing
                with probability p_error and incorrect goal sensing with probability
                1 - p_error."""
                trueval = position_visible(state.mypose,state.mygoal,self.maxrange)
                if random.random() < self.p_error:
                        return not trueval
                return trueval

class ObjectSensorModel:
        """Same as GoalSensorModel but for other objects.  Proximity and a view
        sensor."""
        def __init__(self,name,proximity=2,p_view_fp=0.05,p_view_fn=0.05,p_prox_fp=0.1,p_prox_fn=0.1):
                self.name = name
                self.proximity = proximity
                self.view_dist = {True:{True:1.0-p_view_fn,False:p_view_fn},False:{True:p_view_fp,False:1.0-p_view_fp}}
                self.prox_dist = {True:{True:1.0-p_prox_fn,False:p_prox_fn},False:{True:p_prox_fp,False:1.0-p_prox_fp}}         

        def probability_raw(self,pose,opose,value):
                trueprox = (distance2(opose,pose) <= self.proximity)
                trueview = position_visible(pose,(opose[0],opose[1]),100)
                return self.view_dist[trueview][value[0]]*self.prox_dist[trueprox][value[1]]
                
        def probability(self,state,value):
                return self.probability_raw(state.mypose,state.objectPoses[self.name])

        def sample(self,state):
                pose = state.mypose            
                opose = state.objectPoses[self.name]
                trueprox = distance2(opose,pose) <= self.proximity
                trueview = position_visible(pose,(opose[0],opose[1]),100)
                view = sample_distribution(self.view_dist[trueview])
                prox = sample_distribution(self.prox_dist[trueprox])
                return (view,prox)

class AgentObservation:
        """Records a pose, whether a goal is visible in the pose, and
        object->visible mappings for all other objects."""
        def __init__(self,mypose,goalvisible=False,objectvisible={}):
                self.mypose = mypose
                self.goalvisible = goalvisible
                self.objectvisible = objectvisible

class AgentSensorModel:
        """Combines GoalSensorModel and ObjectSensorModel to report
        on the likelihood of AgentObservations."""
        def __init__(self,goalSensor,objectSensors={}):
                self.goalSensor = goalSensor
                self.objectSensors = objectSensors
        
        def probability(self,state,observation):
                """Given an AgentState and AgentObservation, returns the likelihood
                of that observation in that state."""
                if state.mypose != observation.mypose: return 0.0
                Pviewed = 1.0
                Pviewed *= self.goalSensor.probability(state,observation.goalvisible)
                for obj,vis in observation.objectvisible:
                        Pviewed *= self.objectSensors[obj].probability(state,vis)
                return Pviewed
        
        def sample(self,state):
                """Samples an AgentObservation randomly using given AgentState"""
                obs = AgentObservation(state.mypose)
                obs.goalvisible = self.goalSensor.sample(state)
                obs.objectvisible = dict((name,val.sample(state)) for (name,val) in self.objectSensors.iteritems())
                return obs


class SingleAgentBehaviorModel:
        """By default, a simple state-independent markovian behavior model.
        The distribution is specified as a dict mapping action names to action
        probabilities.  It can also vary by pose"""
        def __init__(self,map,p_action = 'uniform'):
                self.map = map
                # the self.p_action is the dict mapping actions to probs
                if p_action == 'uniform':
                        self.p_action = uniform_distribution(actionNames)
                else:
                        self.p_action = p_action

        def action_distribution(self,pose):
                actions = valid_actions(self.map,pose)
                dist = {}
                for a in actions:
                        dist[a] = self.p_action[a]
                normalize(dist)
                return dist
                        

        def next_state_distribution(self,pose):
                dist = dict()
                for a,p in self.action_distribution(pose).iteritems():
                        ns = next_pose(self.map,pose,a)
                        dist[ns] = dist.get(ns,0.0) + p
                return dist


class AgentBeliefState:
        """Provides current pose, cell->prob mappings for goal beliefs,
        object->[(cell,direction)->prob] mappings for beliefs about object
        locations and directional headings"""
        def __init__(self,pose):
                self.mypose = pose
                self.b_goal = None
                self.b_objects = None

        def init_uniform_goals(self,map):
                self.b_goal = uniform_distribution(enumerate_map_cells(map))
                
        def init_uniform_objects(self,map,names):
                self.b_objects = {}
                for oname in names:
                        self.b_objects[oname] = uniform_distribution( \
                                                cartesian_product(iterate_map_cells(map),directions))

        def sample_true_state(self):
                """Returns a sample of the true underlying state, based on
                current beliefs"""
                s = AgentState()
                s.mypose = self.mypose
                # BUGFIX?: Was originally "b_goals"
                if self.b_goal:
                        s.mygoal = sample_distribution(self.b_goal)
                if self.b_objects:
                        s.objectposes = dict((name,sample_distribution(bo)) \
                                                                for (name,bo) in self.b_objects.iteritems())
                return s

class AgentPolicyBase:
        """A policy defining actions given current beliefs and time"""
        def __init__(self,map):
                self.map = map

        def evaluate(self,beliefState):
                """Subclasses should override this"""
                pass

        def advance(self):
                """Indicates a timestep has elapsed.  Subclasses may override this."""
                pass

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


class AgentOpenLoopPolicy(AgentPolicyBase):
        """A fixed path policy"""
        
        def __init__(self,map,actionlist,repeat=False):
                AgentPolicyBase.__init__(self,map)
                self.actionlist = actionlist
                self.progression = 0
                self.repeat = repeat

        def evaluate(self,beliefState):
                if self.progression < len(self.actionlist):
                        return self.actionlist[self.progression]
                return actionNames[0]
        
        def advance(self):
                self.progression += 1
                if self.repeat and self.progression >= len(self.actionlist):
                        self.progression=0
                        
        def done(self):
                return self.progression >= len(self.actionlist)

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
        #TODO: a function like this might be useful to implement...
        return next_pose(self.map,pose,search_path(map,pose,target))
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

                #TODO (Question 2): replace this line with something more
                #sensible
                #return 'l'
                successors = []
                for a in valid_actions(self.map,beliefState.mypose):
                        snext = next_pose(None,beliefState.mypose,a)
                        potential = self.potential_field_eval(beliefState,snext)
                        successors.append((potential,snext,a))
		b = random.choice(search_path(self.map, beliefState.mypose, goals))
                #return steer_toward(beliefState.mypose,self.local_search(e))
		return max(successors[2])

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
                #TODO (Question 3): replace this line with your own code
                return steer_toward(beliefState.mypose,self.local_search(beliefState))
        
        def potential_field_eval(self,beliefState,mypose):
                psum = 0.0
                for b_obj in beliefState.b_objects.itervalues():
                        for (o,p) in b_obj.iteritems():
                                d = abs(o[0]-mypose[0])+abs(o[1]-mypose[1])
                                if d < self.repulsive_range:
                                        psum += p*pow(self.repulsive_range-d,2)
                return psum


# TODO (question 4): Implement your own policy class
class AgentStudentPolicy(AgentPolicyBase):
        """You should implement this!"""
        
        def __init__(self,map):
                AgentPolicyBase.__init__(self,map)
		self.repulsive_range = 3
                self.goallist = goallist
                self.progression = 0
                self.repeat = repeat
                self.hit = False

        def local_search(self,beliefState):
                successors = []
                for a in valid_actions(self.map,beliefState.mypose):
                        snext = next_pose(None,beliefState.mypose,a)
                        potential = self.potential_field_eval(beliefState,snext)
                        successors.append((potential,snext,a))
                return min(successors)[2]
        def evaluate(self, beliefState):
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
        
        def advance(self):
                pass



class Agent:
        def __init__(self,name,map):
                self.name = name
                self.map = map
                self.policy = None
                self.currentBelief = None
                self.sensorModel = None
                self.agentBehaviorModels = None

        def set_policy(self,policy):
                self.policy = policy

        def set_sensor_model(self,sensorModel):
                self.sensorModel = sensorModel

        def set_behaviors(self,numagents,behavior_model):
                self.agentBehaviorModels = [behavior_model]*numagents
        
        def update_belief(self,b,lastAction,observation):
                bnext = AgentBeliefState(observation.mypose)
                #update goal belief
                bnext.b_goal = self.update_goal_belief(bnext.mypose,b.b_goal,observation.goalvisible)
                #update object beliefs
                bnext.b_objects = dict()
                for (o,bo) in b.b_objects.iteritems():
                        bnext.b_objects[o] = self.update_object_belief(bnext.mypose,o,bo,observation.objectvisible[o])
                return bnext

        def update_goal_belief(self,mypose,bgoal,goalvisible):
                """Given the new pose of the agent and the belief bgoal over goal
                positions on the prior step, return an updated distribution on goals
                given the observation goalvisible
                """
                #TODO (Question 1): fill this in -- you may want to use
                i = self.sensorModel.goalSensor.probability_raw(self.mypose,self.bgoal,self.goalvisible)
                return bgoal.copy()
                
        
        def update_object_belief(self,mypose,objname,bobject,obsvisible):
                """Given the new pose of the agent and the belief bobject on
                object pose in the prior step, return an updated distribution
                on the object pose, given the observation obsvisible.
                """
                #TODO (Question 1): fill this in -- you may want to use
                self.sensorModel.objectSensors[objname].probability_raw(self.mypose,self.bobject,self.obsvisible)
                self.agentBehaviorModels[self.objname]
                return bobject.copy()

        def sense(self,lastAction,obs,rewards):
                """Observation/reward update."""
                b0 = self.currentBelief
                bnext = self.update_belief(b0,lastAction,obs)
                self.currentBelief = bnext
        
        def act(self):
                """Return the chosen action and update internal state if necessary."""
                a = self.policy.evaluate(self.currentBelief)
                self.policy.advance()
                return a
                
