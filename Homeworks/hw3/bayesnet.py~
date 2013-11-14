#!/usr/bin/env python

"""Discrete Bayesian networks and supporting structures.
Based on code for binary Bayesian networks by Stuart Russell
(http://aima-python.googlecode.com).

Please read the documentation carefully.  It is probably easiest to start with
the documentation for DiscreteCPT, then read about DiscreteBayesNode, and
finally DiscreteBayesNet.

Furthermore, please see the source code for
examples of using this code to build and query the burglary
network from the book."""

import random
import math
import copy

def cumsum(ls):
	"""Returns a list containing the cumulative sums at every element of
	ls.
	
	i.e., cumsum([1,2,3]) = [1,3,6]."""
	
	acc = 0
	r = [0 for v in ls]
	for i,v in enumerate(ls):
		acc += v
		r[i] = acc
	return r
	
def extend(d, k, v):
	"""Returns a new dict containing elements of d and the new key,value pair
	indicated by k,v"""
	n = d.copy()
	n[k] = v
	return n
	
def cut(d, k):
	"""Returns a new dict containing elements of d, excepting the key,value
	pair with key k (if it exists in d).
	
	If d is a sequence, returns a new list containing all elements of d not
	equal to k."""
	if isinstance(d, dict):
		n = d.copy()
		if k in n:
			del n[k]
		return n
	return [v for v in d if v != k]
	
def normalize(dist):
	"""Normalizes a probability distribution so it sums to 1.  The distribution
	may be a list or a dictionary of value,probability pairs.
	
	This function modifies the original object."""
	
	if isinstance(dist, dict):
		# Make sure our keys/values line up in their lists
		keys = dist.keys()
		vals = [dist[k] for k in keys]
		normalize(vals)
		for k,v in zip(keys,vals):
			dist[k] = v
		return
	fdist = [float(d) for d in dist]
	s = sum(fdist)
	if s == 0:
		return
	fdist = [d/s for d in fdist]
	for i,d in enumerate(fdist):
		dist[i] = d
	
# weights should sum to 1
def pick_weighted(weights, vals, eps=1.0e-4):
	"""Selects a value from vals with probability expressed by the corresponding
	value in weights.
	
	weights should sum to 1.  If sum(weights) is not within eps of 1, an
	exception is raised."""
	
	weightSum = cumsum(weights)
	if weightSum[-1] == 0:
		return random.choice(vals)
	if abs(weightSum[-1]-1.0) > eps:
		raise RuntimeError("Weights don't sum to 1")
	r = random.uniform(0.0,1.0)
	for v,w in zip(vals, weightSum):
		if r > w:
			continue
		return v
	return vals[-1]
	
def bayes_thm(likelihood, priorOutcome, priorCondition):
	return likelihood * priorOutcome / priorCondition

def enumerate_domains(domainList):
        """Returns a list of all values the cartesian product of domains
        in domainList.  If each of n domains has k values, this takes k^n
        time."""
        if len(domainList) == 0:
                yield ()
                raise StopIteration()
        for v in domainList[0]:
                for rest in enumerate_domains(domainList[1:]):
                        yield (v,)+rest
        raise StopIteration()

       
	
class DiscreteCPT(object):
	"""A conditional probability table for a variable with discrete values."""
	def __init__(self, vals, probTable):
		"""vals is a list of discrete values the variable can assume.
		probTable should be a dictionary whose keys are tuples representing
		possible combinations of values for all the conditions; the corresponding
		value for each key is a list giving the probabilities corresponding
		to each of the values in vals.
		
		If the variable has no conditions -- that is, the node has no parents
		in the network -- probTable may be a list giving the
		prior distribution over the values in val.
		
		Ex 1:  candy = DiscreteCPT(['Lemon', 'Lime', 'Cherry'], [0.4,0.2,0.4])
		gives us a discrete variable representing the probability of various
		flavors of candy drawn from a bin.  This has no conditions.  Lemon
		and Cherry have probabilities of 40%, and Lime has a probability of
		20%.
		
		Ex 2:  candy = DiscreteCPT(['Lime', 'Cherry'],
					{('b1',): [1.0, 0.0], 
					('b2',): [0.75, 0.25], 
					('b3',): [0.5, 0.5],
					('b4',): [0.25, 0.75],
					('b5',): [0.0, 1.0]})
		gives us a discrete variable representing the probability of flavors of
		candy, conditioned on which bin we draw the candy from.  (See B351 class
		slides for an illustration.)  Here bin 1 is composed of 100% lime
		candies, and bin 4 is composed of 25% Lime and 75% Cherry."""
		
		self.myVals = vals
		if isinstance(probTable, list) or isinstance(probTable, tuple):
			self.probTable = {(): probTable}
		else:
			self.probTable = probTable
			
	def values(self):
		"""Returns the list of values the variable can take."""
		return self.myVals
		
	def prob_dist(self, parentVals):
		"""Returns a dictionary giving a value:probability mapping for each
		value the variable can assume, given a tuple with values for all the
		conditions.
		
		Ex:  Uses the CPT defined in example 2 from __init__().
			candyProb3 = candy.prob_dist( ('b3',) )
		returns this dict:
			{'Lime': 0.5, 'Cherry': 0.5}
		"""
		if isinstance(parentVals, list):
			parentVals = tuple(parentVals)
		return dict([(self.myVals[i],p) for i,p in \
					enumerate(self.probTable[parentVals])])
		
	def rand_result(self, parentVals):
		"""Returns a randomly-selected value for the variable, based on the
		probability of each value given a tuple specifying values for all the
		conditions.
		
		Ex:  Uses the CPT defined in example 2 from __init__().
			flavor = candy.rand_result( ('b4',) )
		will return 'Lime' approximately 25% of the time, and 'Cherry'
		approximately 75% of the time."""
		dist = self.probTable[parentVals]
		return pick_weighted(dist,self.myVals)		
		
class DiscreteBayesNode(object):
	"""A node in a Bayesian network of discrete-valued variables."""
	def __init__(self, name, parents, cpt):
		"""name is a string giving the name of this node's variable.  parents
		is a list of strings giving the names of this node's parent nodes (empty
		if the node has no parents).  cpt is a DiscreteCPT representing this
		node's conditional probability table -- i.e., the probabilities of
		outcomes for this variable conditioned on the values of the node's
		parents' values.
		
		One thing to be careful of:  the node's parents are, of course, the
		conditions in the CPT.  The names of the parents should be given in
		the same order here as their values are specified in the probability
		table of the CPT.  See DiscreteBayesNet.__init__() for examples."""
		self.parents = parents
		self.name = name
		self.cpt = cpt

def node_to_factor(node,evidence):
        whole = dict()
        for (k,pnode) in node.cpt.probTable.iteritems():
                for v,p in zip(node.cpt.values(),pnode):
                        whole[k+(v,)] = p
        outorder = sorted((n,i) for i,n in enumerate(node.parents+[node.name]) if n not in evidence)
        evidenceOrder = [(n,i) for i,n in enumerate(node.parents+[node.name]) if n in evidence]
        res = dict()
        for (k,v) in whole.iteritems():
                outk = tuple([k[i] for (n,i) in outorder])
                if all(k[i]==evidence[n] for (n,i) in evidenceOrder):
                        res[outk] = v
        return tuple(n for (n,i) in outorder),res
		
class DiscreteBayesNet(object):
	"""A Bayesian network of discrete-valued variables."""
	def __init__(self, nodes):
		"""nodes is a list of DiscreteBayesNodes objects containing the nodes in
		the network.
		
		Example 1 (the burglar-alarm network from the textbook):
		burglarNet = DiscreteBayesNet(
				[ DiscreteBayesNode('Burglary', [],
					DiscreteCPT(['T','F'], [0.001, 0.999])),
				DiscreteBayesNode('Earthquake', [],
					DiscreteCPT(['T','F'], [0.002, 0.998])),
				DiscreteBayesNode('Alarm', ['Burglary', 'Earthquake'],
					DiscreteCPT(['T','F'],
						{('T','T'):[0.95, 0.05],
						('T','F'):[0.94, 0.06],
						('F','T'):[0.29, 0.71],
						('F','F'):[0.001, 0.999]})),
				DiscreteBayesNode('JohnCalls', ['Alarm'],
					DiscreteCPT(['T','F'],
						{('T',):[0.9, 0.1],
						('F',):[0.05, 0.95]})),
				DiscreteBayesNode('MaryCalls', ['Alarm'],
					DiscreteCPT(['T','F'],
						{('T',):[0.7, 0.3],
						('F',):[0.01, 0.99]})) ])
		See the source code of this module for examples of how to use this
		network.
		
		Example 2 (candy probabilities from equally-likely bins):
		candyNet = DiscreteBayesNet(
				[ DiscreteBayesNode('Bin', [],
					DiscreteCPT(['b1','b2','b3','b4','b5'],
								[0.2, 0.2, 0.2, 0.2, 0.2])),
				DiscreteBayesNode('Candy', ['Bin'],
					DiscreteCPT(['Lime', 'Cherry'],
					{('b1',): [1.0, 0.0], 
					('b2',): [0.75, 0.25], 
					('b3',): [0.5, 0.5],
					('b4',): [0.25, 0.75],
					('b5',): [0.0, 1.0]})) ])"""
		
		self.variables = dict([(n.name, n) for n in nodes])
		self.roots = [n for n in nodes if not n.parents]
		self.nodes = nodes
		
	def enumerate_ask(self, var, e):
		"""Returns a dict giving the posterior P(var|e) for the variable
		var given some known values e in the network.  Uses the enumerate-ask
		algorithm (see the R&N textbook), which is simple but slow.
		
		var is the string giving the target variable's name.  e is a dict giving
		variable:value mappings for known values in the network."""
		
		vals = self.variables[var].cpt.values()
		dist = {}
		if var in e:
			for v in vals:
				dist[v] = 1.0 if e[var]==v else 0.0
			return dist

		for v in vals:
                    dist[v] = self.enumerate_all(self.variables,extend(e, var, v))
		normalize(dist)
		return dist
	
	def enumerate_all(self, vars, e, v=None):
		"""A helper method for the enumerate_ask method.  Gives the probability
		of the evidence in e over the variables named in vars.  Optionally can
		use v to specify a variable to use as the starting point for the 
		summation (otherwise, starting point is arbitrary)."""
		
		if len(vars) == 0:
			return 1.0
			
		if v:
			Y = v
		else:
			Y = vars.keys()[0]
		Ynode = self.variables[Y]
		parents = Ynode.parents
		cpt = Ynode.cpt
		
		# Work up the graph if necessary
		for p in parents:
			if p not in e:
				return self.enumerate_all(vars, e, p)
		
		if Y in e:
			y = e[Y]
			# P(y | parents(Y))
			cp = cpt.prob_dist([e[p] for p in parents])[y]
			result = cp * self.enumerate_all(cut(vars,Y), e)
		else:
			result = 0
			for y in Ynode.cpt.values():
				# P(y | parents(Y))
				cp = cpt.prob_dist([e[p] for p in parents])[y]
				result += cp * self.enumerate_all(cut(vars,Y),
													extend(e, Y, y))

		return result

        def top_down_ask(self, var, e, order):
                """Uses top-down reasoning to compute the probability
                distribution P(var|e) given the elimination order in the
                'order' list.

                order should contain var and should not overlap with e.
                Evidence must only be given on ancestor nodes of var, otherwise
                the answer will be incorrect.
                """
                #modify copies of the node CPTs
                cpttemp = dict((v,copy.deepcopy(self.variables[v].cpt)) for v in order)
                cpttemp[var] = copy.deepcopy(self.variables[var].cpt)
                #set evidence nodes to be 100% certain
                for (v,val) in e.iteritems():
                        assert(v not in order),"Elimination order cannot include evidence variables"
                        cpttemp[v] = DiscreteCPT([val],[1.0])
                assert(var in order),"Elimination order must include query variable"
                for X in order:
                        parents = self.variables[X].parents
                        #store summation result here
                        newdist = dict()
                        for v in cpttemp[X].values():
                                sump = 0.0
                                for p in parents:
                                        assert isinstance(cpttemp[p],dict),"Incorrect elimination order?"
                                #sum together all combinations of parents
                                for ptuple in enumerate_domains([cpttemp[p].keys() for p in parents]):
                                        #probability of parent value...
                                        pprobability = 1.0
                                        for p,pv in zip(parents,ptuple):
                                                pprobability *= cpttemp[p][pv]
                                        #times conditional probability
                                        sump += cpttemp[X].prob_dist(ptuple)[v]*pprobability
                                newdist[v] = sump
                        normalize(newdist)
                        if X == var: return newdist
                        cpttemp[X] = newdist
                return

        def variable_elimination_ask(self, var, e, order):
                """Uses variable elimination to compute the probability
                distribution P(var|e) given the elimination order in the
                'order' list.

                order should contain var and should not overlap with e.
                """
                for v,val in e.items():
                        assert(not v in order),"Elimination order cannot include evidence variables"
                assert(var in order),"Elimination order must include query variable"
                #get node factors (map domain to probability distribution)
                factors = dict()
                #map variables to affecting factor domains
                affectingFactors = dict((v,set()) for v in self.variables.iterkeys())
                for v,node in self.variables.iteritems():
                        factor = None
                        (domain,factor) = node_to_factor(node,e)
                        if domain in factors:
                                existing = factors[domain]
                                for v in factor.keys():
                                        existing[v] *= factor[v]
                        else:
                                factors[domain] = factor
                        for v in domain:
                                affectingFactors[v].add(domain)
                for X in order:
                        Xfactors = affectingFactors[X]
                        if X == var:
                                #multiply out the factors to get the result
                                for domain in Xfactors:
                                        assert(domain==(X,)),"Incomplete elimination order?"
                                res = dict()
                                for v in self.variables[var].cpt.values():
                                        res[v] = factors[(X,)][(v,)]
                                normalize(res)
                                return res
                        #compute the factor product
                        joindomain = set()
                        for domain in Xfactors:
                                joindomain = joindomain | set(domain)
                        joindomain = tuple(sorted(joindomain))
                        #print "Eliminate",X,"Join",joindomain,"with",len(Xfactors),"factors"
                        indexdict = dict((n,i) for i,n in enumerate(joindomain))
                        dindices = []
                        for domain in Xfactors:
                                dindices.append([indexdict[d] for d in domain])
                        joindist = dict()
                        for vals in enumerate_domains([self.variables[v].cpt.values() for v in joindomain]):
                                prob = 1.0
                                for indices,domain in zip(dindices,Xfactors):
                                        dval = tuple([vals[i] for i in indices])
                                        prob *= factors[domain][dval]
                                joindist[vals] = prob
                        #now eliminate X from the distribution through summing
                        cutdomain = tuple(cut(joindomain,X))
                        xpos = joindomain.index(X)
                        dist = dict()
                        for vals in enumerate_domains([self.variables[v].cpt.values() for v in cutdomain]):
                                sump = 0.0
                                for v in self.variables[X].cpt.values():
                                        vind = vals[:xpos]+(v,)+vals[xpos:]
                                        sump += joindist[vind]
                                dist[vals] = sump
                        for domain in Xfactors:                               
                                del factors[domain]
                                for v in domain:
                                        if v!=X: affectingFactors[v].remove(domain)
                        if cutdomain in factors:
                                #multiply dist into existing factor
                                existing = factors[cutdomain]
                                for v in dist.keys():
                                        existing[v] *= dist[v]
                        else:
                                factors[cutdomain] = dist
                                for v in cutdomain:
                                        affectingFactors[v].add(cutdomain)
                        affectingFactors[X] = None
                return
	
	def prob(self, e):
		"""Gives the probability over the entire graph of the evidence in e.
		Good for deciding the likelihood of a dataset given a network."""
		return self.enumerate_all(self.variables, e)
		
	def topological_sort(self):
		"""Returns an iterator over the nodes in top-down order, such
		that no node appears before its parents"""
		#detect leaves
		numChildren = dict((n.name,0) for n in self.variables.values())
		for n in self.variables.itervalues():
			for p in n.parents:
			      numChildren[p]+=1
		#do a BFS from leaves to get the reverse topological sort
		topo = []
		queue = [n for (n,c) in numChildren.iteritems() if c==0]
		if len(queue)==0:
			raise ValueError("Bayes net is not acyclic?")
		while len(queue)>0:
			n = self.variables[queue.pop(0)]
			topo.append(n)
			for p in n.parents:
                            assert numChildren[p]>0
                            numChildren[p] -= 1
                            if numChildren[p]==0:
                                queue.append(p)
		#now reverse it to get the top down ordering
                assert len(topo)==len(self.variables)
		return reversed(topo)
					
	def monte_carlo_sample(self):
		"""Performs a Monte-carlo sampling of all the nodes in the network.
		Returns a dict of variable:value pairs where the values are
		sampled according to the true joint distribution"""
		result = dict()
		for n in self.topological_sort():
			pvals = tuple(result[p] for p in n.parents)
			result[n.name] = n.cpt.rand_result(pvals)
		return result
        
	def importance_sample(self,e,sampling_weights = 'uniform'):
		"""Performs an importance sampling of all the nodes in the
		network given evidence and a sampling_weights variable.
		sampling_weights can either be 'uniform', 'proportional',
		or a dict that maps variable names to DiscreteCPT's.
		Returns a (likelihood_weight,assignment) pair"""
		result = dict()
		likelihood = 1.0
		for n in self.topological_sort():
			pvals = tuple(result[p] for p in n.parents)
			if n.name in e:
				#evidence variable
				result[n.name] = e[n.name]
				likelihood *= n.cpt.prob_dist(pvals)[e[n.name]]
			else:
				#not an evidence variable
				#likelihood weight of the chosen value for n
				w = 1.0
				#chosen value
				nvalue = None
				if sampling_weights=='uniform':
					nvalue = random.choice(n.cpt.values())
					w = 1.0/len(n.cpt.values())
                                elif sampling_weights=='proportional':
					nvalue = n.cpt.rand_result(pvals)
					w = n.cpt.prob_dist(pvals)[nvalue]
				else:
					nvalue = sampling_weights[n.name].rand_result(pvals)
					w = sampling_weights[n.name].prob_dist(pvals)[nvalue]
				result[n.name] = nvalue
				likelihood *= (n.cpt.prob_dist(pvals)[nvalue]/w)
		return (likelihood,result)


	def monte_carlo_estimate(self,var,e,n):
		"""Performs an estimate of the probability distribution P(var|e)
                using plain Monte-carlo sampling."""
		ncpt = self.variables[var].cpt
		ncount = dict((value,0) for value in ncpt.values())
		esum = 0
		for iter in xrange(n):
                        sample = self.monte_carlo_sample()
                        if all(sample[key]==value for (key,value) in e.iteritems()):
                                #sample agrees with e
                                ncount[sample[var]] += 1
                                esum += 1
                if esum==0: return 'Undefined'
                for value in ncount.iterkeys():
                        ncount[value] = float(ncount[value])/float(esum)
                return ncount

	def likelihood_weighting_estimate(self,var,e,n,sampling_weight='uniform'):
		"""Performs an estimate of the probability distribution P(var|e)
                using likelihood weighting Monte-carlo sampling."""
		ncpt = self.variables[var].cpt
		ncount = dict((value,0.0) for value in ncpt.values())
		wsum = 0.0
		for iter in xrange(n):
                        (w,sample) = self.importance_sample(e,sampling_weight)
                        assert all(sample[key]==value for (key,value) in e.iteritems())
                        
                        ncount[sample[var]] += w
                        wsum += w
                if wsum==0: return 'Undefined'
                for value in ncount.iterkeys():
                        ncount[value] = float(ncount[value])/float(wsum)
                return ncount
        
	def train_ml(self, samples, priorCount=0):
		"""Trains all variables in the network using the provided samples.
		Employs a maximum-likelihood estimation, which estimates probabilities
		directly from frequencies in the data.  Simple and fast but requires
		a fairly large amount of complete data.
		
		samples is assumed to be a list of dicts.  Each dict represents a data
		point and provides variable:value mappings for the variables in the
		network."""
		
		for node in self.nodes:
			parents = node.parents
			for pv in node.cpt.probTable:
				parentSamples = [s for s in samples if False not in \
								[s[p] == pv[i] for i,p in enumerate(parents)]]
				for i,val in enumerate(node.cpt.values()):
					if len(parentSamples) == 0:
						node.cpt.probTable[pv][i] = 0
						continue
					valSamples = [s for s in parentSamples if s[node.name]==val]
					node.cpt.probTable[pv][i] = float(len(valSamples)+priorCount) / \
												(len(parentSamples)+\
													priorCount*len(node.cpt.values()))
						
	def train_em(self, vars, samples, max_iters, eps=1.0e-5):
		"""Trains the indicated variables in the network using the provided
		samples.  Employs an expectation-maximization algorithm.  Presently
		uses enumerate_ask to estimate probabilities for each of the trained
		variables on every iteration, so is fairly slow (but robust to missing
		data).
		
		vars is a list of names for variables to be trained.  samples is a list
		of dicts (see train_ml).  max_iters is the maximum number of iterations
		to run, and the optional parameter eps (defaults to 1.0e-5) specifies
		a threshold of change in the log-likelihood at which the training
		terminates."""
		
		def mul(a,b):
			return a*b
		samples_noweight = [cut(s,'Weight') for s in samples]
		sampleWeights = [s['Weight'] if 'Weight' in s else 1.0 for s in samples]
		parentVals = [self.variables[v].cpt.probTable.keys() for v in vars]
		vals = [self.variables[v].cpt.values() for v in vars]
		oldll = sum([math.log(self.prob(s)) for s in samples_noweight])
		for iter_c in range(max_iters):
			print "Iter", iter_c
			parentDists = [[[self.enumerate_ask(p,s) \
								for p in self.variables[v].parents] \
							for v in vars]
						for s in samples_noweight]
			varDists = [[self.enumerate_ask(v,s) for v in vars] \
					for s in samples_noweight]
					
			# In theory a fast(er) way to do this, but consumes huge
			# amounts of memory quickly
#			parentCounts = [[[sampleWeights[i]*reduce(mul,
#											[parentDists[i][j][k][pv[k]] \
#												for k in range(len(pv))]) \
#										for i in range(len(samples))]
#									for pv in parentVals[j]] \
#								for j,v in enumerate(vars)]
#			valParentCounts = [[[[varDists[i][j][vv]*parentCounts[j][k][i] \
#											for i in range(len(samples))] \
#										for vv in vals[j]] \
#									for k in range(len(parentVals[j]))] \
#								for j,v in enumerate(vars)]

			# This seems to provide a good tradeoff between list-comprehension
			# speed and memory consumption (YMMV)
			for j,v in enumerate(vars):
				for h,pv in enumerate(parentVals[j]):
					pc = [sampleWeights[i]*reduce(mul, 
												[parentDists[i][j][k][pv[k]] \
													for k in range(len(pv))]) \
									for i in range(len(samples))]
					vpc = [[varDists[i][j][vv]*pc[i] \
										for i in range(len(samples))] \
									for vv in vals[j]]
					pcSum = sum(pc)
					for i in range(len(vals[j])):
						vpcSum = sum(vpc[i])
						self.variables[v].cpt.probTable[pv][i] = vpcSum / pcSum
			
			ll = sum([math.log(self.prob(s)) for s in samples_noweight])
			if abs(ll-oldll) < eps:
				return
			oldll = ll
		
		
if __name__ == "__main__":
	# The burglary node has no parents
	burglary = DiscreteBayesNode('Burglary', [],
						# Mapping probabilities to T,F values for the variable
						DiscreteCPT(['T','F'], [0.001, 0.999]))
	
	# The earthquake node has no parents
	earthquake = DiscreteBayesNode('Earthquake', [],
						DiscreteCPT(['T','F'], [0.002, 0.998]))
						
	# The alarm node depends on burglary and earthquake
	alarm = DiscreteBayesNode('Alarm', ['Burglary', 'Earthquake'],
						DiscreteCPT(['T','F'],
							# Mapping values of B,E to T,F values for the
							# alarm
							{('T','T'):[0.95, 0.05],
							('T','F'):[0.94, 0.06],
							('F','T'):[0.29, 0.71],
							('F','F'):[0.001, 0.999]}))
	
	# The JohnCalls node depends on the alarm
	john = DiscreteBayesNode('JohnCalls', ['Alarm'],
						DiscreteCPT(['T','F'],
							# Mapping values of Alarm to T,F values for
							#  John calling
							{('T',):[0.9, 0.1],
							('F',):[0.05, 0.95]}))
									
	# The MaryCalls node depends on the alarm
	mary = DiscreteBayesNode('MaryCalls', ['Alarm'],
						DiscreteCPT(['T','F'],
							{('T',):[0.7, 0.3],
							('F',):[0.01, 0.99]}))
							
	burglarynet = DiscreteBayesNet([burglary, earthquake, alarm, john, mary])
	
	# Evidence can be empty (gives us the overall probability of something
	#  occurring, without prior knowledge)
	evidence = {}
	print "Prob. of earthquake:", \
			burglarynet.enumerate_ask('Earthquake', evidence)

        print "Prob. of alarm:", \
			burglarynet.enumerate_ask('Alarm', evidence)

        print "Prob. of earthquake [top down]:", \
		burglarynet.top_down_ask('Earthquake', evidence, ['Earthquake','Alarm'])

        print "Prob. of alarm [top down]:", \
		burglarynet.top_down_ask('Alarm', evidence, ['Earthquake','Burglary','Alarm'])

	print "Prob. of earthquake [VE]:", \
			burglarynet.variable_elimination_ask('Earthquake', evidence, ['JohnCalls','MaryCalls','Alarm','Burglary','Earthquake'])

        print "Prob. of alarm [VE]:", \
			burglarynet.variable_elimination_ask('Alarm', evidence, ['JohnCalls','MaryCalls','Burglary','Earthquake','Alarm'])
			
	# Evidence can contain mappings of variables to legal values
	evidence = {'JohnCalls':'T', 'MaryCalls':'T'}
	print "Prob. of burglary, given John and Mary call:", \
		burglarynet.enumerate_ask('Burglary', evidence)

	print "Prob. of burglary, given John and Mary call [VE]:", \
		burglarynet.variable_elimination_ask('Burglary', evidence, ['Earthquake','Alarm','Burglary'])
	
	print "MC estimate of burglary, given John and Mary call:", \
		burglarynet.monte_carlo_estimate('Burglary', evidence,10000)

	print "LW estimate of burglary, given John and Mary call:", \
		burglarynet.likelihood_weighting_estimate('Burglary', evidence,10000,'proportional')

	print "LW(2) estimate of burglary, given John and Mary call:", \
		burglarynet.likelihood_weighting_estimate('Burglary', evidence,10000,'uniform')

        ptrue = burglarynet.enumerate_ask('Earthquake', evidence)['T']
        n = 100
        ssq = 0.0
        undefs = 0
        for i in xrange(n):
            res = burglarynet.monte_carlo_estimate('Burglary', evidence,1000)
            if res != 'Undefined': ssq += math.pow(res['T']-ptrue,2.0)
            else: undefs += 1
        print "Variance for MC:",ssq/n,"with",undefs,"undefined"
        ssq = 0.0
        undefs = 0
        for i in xrange(n):
            res = burglarynet.likelihood_weighting_estimate('Burglary', evidence,1000,'proportional')
            if res != 'Undefined': ssq += math.pow(res['T']-ptrue,2.0)
            else: undefs += 1
        print "Variance for LW:",ssq/n,"with",undefs,"undefined"
        ssq = 0.0
        undefs = 0
        for i in xrange(n):
            res = burglarynet.likelihood_weighting_estimate('Burglary', evidence,1000,'uniform')
            if res != 'Undefined': ssq += math.pow(res['T']-ptrue,2.0)
            else: undefs += 1
        print "Variance for LW(2):",ssq/n,"with",undefs,"undefined"
