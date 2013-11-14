import random

def uniform_distribution(items):
    """Returns a dict representing a uniform distribution over the items"""
    return dict(zip(items,[1.0/len(items)]*len(items)))

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
def sample_weighted(weights, vals):
	"""Samples an item from vals with probability expressed by the
        corresponding value in weights."""
	
	weightSum = cumsum(weights)
	if weightSum[-1] == 0:
		return random.choice(vals)
	r = random.uniform(0.0,weightSum[-1])
	for v,w in zip(vals, weightSum):
		if r <= w:
			return v
	return vals[-1]

def sample_distribution(dist):
    """Given a dict from item -> p-val, samples an item with probability
    proportional to its p-val."""
    return sample_weighted(dist.values(),dist.keys())

def concatenate(a,b):
    if not isinstance(a,tuple):
        a = (a,)
    if not isinstance(b,tuple):
        b = (b,)
    return a+b

def cartesian_product(a,b):
    """Given sets a and b of either singletons or tuples, returns the
    cartesian product of a and b"""
    return [concatenate(ai,bi) for ai in a for bi in b]
