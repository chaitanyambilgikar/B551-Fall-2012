"""This module defines some methods and variables useful for handling the
voting data in the text files accompanying the assignment.

Each text file contains one voter record per line.  The voter record contains
several values separated by commas -- these represent the voter attributes.

For instance, a single line of a polling file might read "M,W,2,P,SB,D".  This
voter is a white male between 45 and 59, whose political leaning is progressive,
who lives in suburbia, and voted Democratic.  (Further explanation of the
file format is given in the assignment.)

The three global variables defined in this module are as follows:
-politicsVars:  A list of variable names for the voter attributes.  The variable
names appear in the same order as the attribute values in the text files.
-politicsVals:  A list of lists.  Each sub-list contains all possible values
for the corresponding voter attribute.  (i.e., politicsVars[0] is 'Gender';
politicsVals[0] is a list of all possible values for the gender attribute,
namely ['M','F'].
-politicsVarDict:  A dict mapping variable names from politicsVars to the
corresponding lists of values from politicsVals.  Thus politicsVarDict['Gender']
evaluates to the list ['M','F'].

The functions most likely to be of use in completing the assigment are
load_samples_training() and load_samples_testing().
"""


politicsVars = ['Gender', 'Race', 'Age', 'Ideology', 'Population',
				'Vote']
"""A list of variable names for the values on a line of a polling-data file,
in the order the values appear."""
politicsVals = [['M','F'], ['W','B','H','A','O'], ['0','1','2','3'],
				['P','M','C'], ['LC','SC','SB','ST','RU'],
				['D','R','I']]
"""A list of lists; each sub-list contains possible values for the corresponding
variable in politicsVars"""
politicsVarDict = dict(zip(politicsVars, politicsVals))
"""A dict mapping variable names (from politicsVars) to a list of possible
values (from politicsVals)"""

def load_samples(fname):
	"""Returns a list of individual samples read out of file 'fname'.  Samples
	appear one per line, and each sample is a list of comma-separated values.
	The values are assumed to correspond in order to the variables in
	politicsVars.  Each sample is represented as a sub-list containing the
	values in order they were read."""
	
	with open(fname) as fin:
		lines = fin.readlines()
	samples = [[v.strip() for v in l.split(',')] for l in lines]
	return samples

def load_samples_training(fname):
	"""Returns a list of dicts.  Each dict corresponds to a single voter record
	and contains a mapping of all voter variables to that voter's attributes.
	Voter records are loaded from the file named by 'fname' using load_samples().
	
	The list returned by this function may be passed directly to the train_ml()
	method of an appropriately constructed bayesnet.DiscreteBayesNet (i.e.,
	one containing nodes named for the variables defined in politicsVars)."""
	
	samples = load_samples(fname)
	samples = [dict([ (v, s[i]) for i,v in enumerate(politicsVars) ]) \
				for s in samples]
	return samples
	
def load_samples_testing(fname):
	"""Returns a list of tuples.  Each tuple corresponds to a single voter
	record and contains two items.  Voter records are loaded from the file
	named by 'fname' using load_samples().
	
	The first item in each voter tuple is a dict mapping voter variables
	to that voter's attributes, but it is missing the 'Vote' variable.  This
	dict can be passed directly as evidence to the enumerate_ask() method of an
	appropriately constructed bayesnet.DiscreteBayesNet, in order to obtain
	probability estimates for the voter's Vote value based on the voter's
	other attributes.
	
	The second item in each voter tuple is the actual Vote value for that voter.
	This value can be compared to your network's estimate for the Vote value
	for correctness.  The percentage of samples correctly estimated is an estimate
	of the network's accuracy."""
	
	samples = load_samples(fname)
	samples = [ (dict([ (v, s[i]) for i,v in enumerate(politicsVars[:-1]) ]), \
					s[-1]) \
				for s in samples]
	return samples
	
def load_conditional_report(fname):
	"""Loads conditional probability table out of a file.  The file must be
	have the line format:
	
	V1 | V2,V3,V4: PROB
	
	where PROB is a floating-point value, V1 is a value of the dependent
	variable, and V2-V4 are values of the conditions.
	
	Returns a dict suitable for use as the probTable argument when creating a
	bayesnet.DiscreteCPT"""
	
	with open(fname) as fin:
		lines = fin.readlines()
	lines = [[v.strip() for v in l.split(':')] for l in lines]
	lines = [[l[0].split('|'), float(l[1])] for l in lines]
	lines = [[l[0][0], l[0][1].split(','), l[1]] for l in lines]
	table = dict([(p, [ [t[2] for t in table \
							if (t[1]==list( p ) and t[0]==v)][0] \
						for v in set([t[0] for t in table]) ]) \
					for p in set([tuple(t[1]) for t in table])])
	return table