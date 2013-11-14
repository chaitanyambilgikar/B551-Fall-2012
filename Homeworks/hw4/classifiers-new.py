import os
import sys
import utils

########################################################################################
# Naive Bayesian Classifier
########################################################################################
class NaiveBayesClassifier():
	"""
	A Naive Bayes classifier.  
	Naive Bayes classifiers use two probability distributions: 
       - P(label) gives the probability that an input will receive each 
         label, given no information about the input's features. 
       - P(fname=fval|label) gives the probability that a feature 
         (fname) will be a value (fval), given the label (label). 
	"""
	def __init__(self):
		pass
		
	def train(self,examples,featureset):
		"""
                Implement this for Problem I
                
		featureset - set of features
			eg) set(['EXIST_to', 'EXIST_its', 'EXIST_of'])
		examples - list of examples
			An example is a tuple (features, label) while features is a dictionary of feature name:value pair
			eg)
			[
			({'EXIST_its': False, 'EXIST_of': True, 'EXIST_to': False}, 'cat1')
			({'EXIST_its': False, 'EXIST_of': True, 'EXIST_to': False}, 'cat2')
			({'EXIST_its': False, 'EXIST_of': False, 'EXIST_to': False}, 'cat1')
			({'EXIST_its': False, 'EXIST_of': False, 'EXIST_to': False}, 'cat1')
			({'EXIST_its': True, 'EXIST_of': True, 'EXIST_to': True}, 'cat1')
			({'EXIST_its': True, 'EXIST_of': True, 'EXIST_to': True}, 'cat1')
			({'EXIST_its': False, 'EXIST_of': False, 'EXIST_to': False}, 'cat1')
			({'EXIST_its': True, 'EXIST_of': True, 'EXIST_to': True}, 'cat2')
			({'EXIST_its': False, 'EXIST_of': True, 'EXIST_to': True}, 'cat2')
			({'EXIST_its': False, 'EXIST_of': True, 'EXIST_to': False}, 'cat1')
			...
			]

		This method constructs probability distributions for  P(label), P(fname=fval|label) 
		"""
		
		# Get the list of labels. eg) ['cat1','cat2','cat1','cat1','cat1',...]
		# Get a list of feature values for each (label,fname) values in the examples
		# 	which means for 2 labels and 10 features, we will have 2*10 probability distributions
		labels = []	
		vals = {}	# note this is a dictionary of the key:value pair (label,fname):list(fval)
		for features, label in examples: 
			labels.append(label)
			for fname, fval in features.items(): 
				if (label,fname) not in vals:
					vals[(label,fname)] = []
				vals[(label,fname)].append(fval)
		
		# save the label list for possible future use
		self.labelset = set(labels)
		
		# get P(label)
		# construct a ProbDist (probability distribution) with the list 'labels'
		# e.g.
		#   self.p_label = utils.ProbDist()
		#   self.p_label.dict('val1') = p1
		#   self.p_label.dict('val2') = p2
		#   etc

		# Put your code	here
		 
		
		# get P(fname=fval|label)
		# construct probability distributions with the dictionary 'vals' whose values are lists of feature values
		# See 'utils.ProbDist.maximumLikelihood' for an example

		# Put your code here	


	def test_one(self,features):
		"""
                Implement this for Problem I

		Given a series of features corresponding to a text file,
		Compute log P(label|features) = log P(label) + log P(features|label) for each label
		and return the label that maximizes this expression.
		
		features is a dictory of feature_name:value pair
		eg) {'EXIST_its': True, 'EXIST_of': True, 'EXIST_to': True}
		"""
		
		# Replace the following line with your code.
		# For your convenience, 'utils.get_maxitem(dict)' returns the key whose value is the maximum in the dictionary
		return 'cat1'

				
########################################################################################
# Decision Tree Classifier
########################################################################################
class DTNode():
	"""
	Decision Tree node class
	For a branching node, self.name is the feature name and 
	self.branch is a dictionary from feature values -> subtree (a subtree is also a DTNode)
	For a leaf node, self.name represents the label
	"""
	def __init__(self,name=None,branch=None):
		self.name = name
		self.branch = branch

	def show(self,indent):
		"""
		This pretty prints the tree structure.
		Looks good for the feature value 'True/False' but works for others as well
		"""
		name = self.name
		if name == None:
			name = "None"
		elif isinstance(name,int):
			name = "%d" % name
		s = indent + name + "\n"
		if self.branch != None:
			for val in self.branch:
				if val == True:
					v = 't'
				elif val == False:
					v = 'f'
				else:
					v = '|'
				s += self.branch[val].show(indent+v+" ")
		return s

	def classify(self,features):
		"""
		Given a new example (dictionary of features:values), descend the tree
		until a leaf is reached.
		
		If a feature value of the example is missing from the node's branching structure
		(because it hasn't been seen before during training), then an arbitrary
		branch is taken instead.
		"""
		if self.branch != None:	
			fval =  features[self.name]
			if fval in self.branch:
				return self.branch[fval].classify(features)
			else:	# havn't seen this case in training examples
				anykey = self.branch.keys()[0]
				return self.branch[anykey].classify(features)
		else:	# leaf node. in this case, its name is a label not a feature name
			return self.name
			
class DecisionTreeClassifier():
	"""
	"""
	def __init__(self):
		pass
		
	def train(self,examples,featureset):
		"""
		"""
		self.tree = self.decision_tree_learning(examples,featureset.copy())
		print self.tree.show("")
	
	def decision_tree_learning(self,examples,featuresett):
		"""
                Implement this for Problem II
                
		examples - list of examples
		featureset - set of available features
		
		Return value is a DTNode.
		"""
		# get the list of labels from the examples 
		
		# if examples is empty then return default (e.g., 'cat1')
		# else if all examples have the same classification then return a Tree whose name is the classification
		# else if featureset is empty then return a Tree whose name is the majority label value from the list of labels
		# else # need to expand unlike the above three cases where we return leaf nodes having labels as their name
		# 	best_fname = self.choose_feature(featureset,examples)
		# 	tree = a Tree whose name is the best_fname
		# 	m = majority label value
		#
		# 	apply best_fname feature to all examples and split them into N subsets 
		#			where N is the number of best_fname values in the whole examples
		#			It would be easier to use a dictionary 'sub_examples' of the key:value pair
		#			a best_fname value : a list of examples
		#			so that sub_examples[best_fname value] returns a sub list of examples.
		#		for each best_fname value 'fval'
		#			subtree = self.decision_tree_learning(sub_examples[fval],featureset-set([best_fname]),m)
		#			assign the subtree to tree.branch[fval]
		# 	return tree
		
		# replace the following line with your code
		return DTNode(name='cat1')
		
			
	def choose_feature(self,featureset,examples):
		"""
                Implement this for Problem II
                
		Among the given featureset, return the feature that leads to the
		best split among the given list of examples.
		"""
		# replace the following line with your code
		return featureset.pop()	# simplest choice - take the first

	def test_one(self,features):
		"""
		"""		
		rlabel = self.tree.classify(features)
		return rlabel

########################################################################################
# Third Classifier
########################################################################################
# If you want to change the name of the class
# you also need to change the clasifier selection part (line 70) in the file 'classfiy.py'
class ThirdClassifier():
	"""
        Implement this for Problem III
	"""
	def train(self,examples,featureset):
		# replace the following line with your code
		pass

	def test_one(self,features):
		# replace the following line with your code
		return 'cat1'
				
