from operator import itemgetter
import math
import os
import random

PUNCTUATION = ['"', "''", '``', ';', ':', ',', '.', '--', '?', '!', '(', ')']
#STOPWORDS = set(stopwords.words('english'))

def load(filename):
	"""
	Open the given file and read all the words and return the list of words
	Punctuations listed above is removed and all letters are small
	"""
	f = open(filename, "r")
	wordlist = get_wordlist(f.read())	
	return wordlist
	

def get_frequent_words(wordlist,n=-1):
	"""
	Returns most frequent words (list of words, dict of (word,count))
	Note that the dict does not maintain the frequency order among them while the list does
	n: number of words to return, when < 0, return all in frequency descending order
	
	Remember this can be used for any list of values besides word
	For example, for a list of feature values, this return n most frequent feature values
	"""
	# get frequency for each word
	wfreq = {}	# dictionary (word, count)
	for word in wordlist:
		wfreq[word] = wfreq.get(word, 0) + 1
	
	# get list to sort
	wf_items = wfreq.items()
	# sort with values (item 1)
	wf_items.sort(key = itemgetter(1), reverse=True)
	if n >= 0:	# for positive n, return only n words
		return [w for w,f in wf_items[0:n]], dict(wf_items[0:n])
	else:	# return all words
		return [w for w,f in wf_items], dict(wf_items)
	
def get_wordlist(s):
	"""
	From a string, get a list of words
	"""
	#new_str = s
	# all letters become small
	new_str = s.lower()
	# remove punctuations
	for x in PUNCTUATION:
		new_str = new_str.replace(x,' ')
	# split the string with space, tab, newline to get a list of words
	wordlist = new_str.split()
	return wordlist

def remove_stopwords(wlist):
	newlist = []
	for w in wlist:
		if w not in STOPWORDS:
			newlist.append(w)
	return newlist

def get_maxitem(d):
	"""
	Give a dictionary, return the key whose value is the maximun.
	"""
	d_items = d.items()
	d_items.sort(key = itemgetter(1), reverse=True)
	return d_items[0]
				
def get_labels(data_dir):
	"""
	Return all labels (subdirectory names) for the given directory
	All subdirectories under the give directory are assumed labels
	So data_dir is supposed to have only label directories
	"""
	labels = []
	for label in os.listdir(data_dir):
		label_path = os.path.join(data_dir,label)
		if os.path.isdir(label_path):
			labels.append(label)
	return labels 

def get_labeledfiles(base_dir,labeledtopics):
	"""
	Returns the list of all files with label attached tuple (filename with path, label)
	
	base_dir is assumed to have topic directories
	labeledtopics is a mapping from a topic to a label
	"""
	labeledfiles = []
	for topic, label in labeledtopics:
		if topic in os.listdir(base_dir):
			topic_path = os.path.join(base_dir,topic)
			if os.path.isdir(topic_path):
				for filename in os.listdir(topic_path):
					labeledfiles.append((os.path.join(topic_path,filename),label))
		else:
			print "Warning: topic \'%s\' is not in the folder \'%s\'\n" % (topic, base_dir)
	return labeledfiles

class FeatureExtractor():
	"""
	A class related to features of word lists
	"""
	def __init__(self):
		pass
	
	def create_featureset(self, labeledfiles, feature_size, train_maxsize, rand=True):
		"""
		create a feature set with given list of files and options	
		labeledfiles is a list of tuples (file, label)
		eg) [('./data/train/earn\\10000.txt', 'cat1'), ('./data/train/earn\\10002.txt', 'cat1') ...]
		"""
		# process at most maxnum
		# shuffle the list to balance inputs
		if len(labeledfiles) > train_maxsize:
			if rand:
				random.shuffle(labeledfiles)
			labeledfiles = labeledfiles[:train_maxsize]
		
		# determine featureset
		# currently very poor in that 
		# 1. features (frequent words) come from one file
		# 2. NOT removing stop words
		# --> there is a lot of change for improvement
		filename = labeledfiles[0][0]	# filename with path
		wlist = load(filename)	 
		freq_words, freq_words_dic = get_frequent_words(wlist,feature_size)
		
		# create features with a list of words
		# attach feature type string 'EXIST_' at the beginning of each word.
		# The existence of a particular word becomes a feature.
		self.featureset = self.create_bag_of_word_feature('EXIST_',freq_words)
		#self.featureset = self.create_bag_of_word_feature("COUNT,%s_" % '1.5' ,freq_words)


	def create_bag_of_word_feature(self, ftype_str, wlist):
		return set( [ftype_str + w for w in wlist] )
	
	def extract_features(self,wlist,label):
		"""
		Extract features of the given word list with its feature set
		return a tuple of (features, label)
		eg) ({'EXIST_its': False, 'EXIST_of': True, 'EXIST_to': False}, 'cat1')
		"""
		features = {}
		# For now, the features we use need only frequent words information
		freq_words, freq_words_dic  =  get_frequent_words(wlist,-1)	# in fact, all words 

		for fname in self.featureset:
			# every feature name is <feature type string>_<word string>
			ftype_str, w = fname.split('_',1)
			if ftype_str == 'EXIST':
				features[fname] = w in freq_words_dic
			elif ftype_str.startswith('COUNT'):
				features[fname] = freq_words_dic.get(w,0)
		return (features,label)

	def build_examples(self,labeledfiles,maxnum,rand=True):
		"""
		Return a list of examples from the list of files
		A single example is build with a single labeled file (filename with path, label)
		"""	
		# process at most maxnum
		# shuffle the list to balance inputs
		if len(labeledfiles) > maxnum:
			if rand:
				random.shuffle(labeledfiles)
			labeledfiles = labeledfiles[:maxnum]
		
		examples = []
		for filename, label in labeledfiles:
			wlist = load(filename)
			examples.append(self.extract_features(wlist,label))

		return examples 


class ProbDist():
	"""
	A class for a discrete probability distribution.

	The class can store either the regular probability or the log probability for each value,
	depending on the 'log' flag.
	
	member variables:
	self.log - true if logs are stored rather than regular probability values.
	self.min_prob - a constant for the minimum probability stored in the table
	self.data - a dictionary representing the probability distribution. 
	"""
	
	def __init__(self, log=True, bin_boundaries=None):
		"""
		when bin_boundaries==None, we will have a probability for each value.
		when bin_boundaries have boundary values, 
			we will have probabilities over the range of values separated by the boundaries
		"""
		if log:
			self.min_prob = -100
		else:
			self.min_prob = math.exp(-100)

		self.log = log
		self.bin_boundaries = bin_boundaries
		# if bin_boundaries is list, sort it
		if isinstance(bin_boundaries,list):
			self.bin_boundaries.sort()
                self.data = dict()

        def maximumLikelihood(self,vlist):
                """
                Performs maximum likelihood on vlist to compute the parameters
                of the probabilty distribution.
                """
		# compute probabilities
		cnts = {}	# dictionary
		for i in [self.val2binidx(v) for v in vlist]:
			cnts[i] = cnts.get(i, 0) + 1
		if self.log == True:
			self.data = dict([(i, math.log(float(cnts[i])/len(vlist))) for i in cnts.keys()])
		else:
			self.data = dict([(i, float(cnts[i])/len(vlist)) for i in cnts.keys()])

        def maximumAPosteriori(self,vlist,hyperparameters):
                # May want to fill this out
                pass
		
	def get(self, val):
                """Returns the stored probability value (or its log, if self.log is true)
                for the input point val"""
		# return min_prob for unseen values
		if self.val2binidx(val) not in self.data:
			return self.min_prob
		# return corresponding probability
		return self.data[self.val2binidx(val)]

        def getP(self, val):
                """Returns the probability value for the input point val"""
                if self.log: return math.exp(self.get(val))
                else: return self.get(val)

	def getLogP(self, val):
                """Returns the log-probability value for the input point val"""
                if self.log: return self.get(val)
                else: return math.log(self.get(val))
		
	def val2binidx(self, val):
		if self.bin_boundaries == None or len(self.bin_boundaries) <= 0:
			return val
		if val < self.bin_boundaries[0]:
			return 0
		for idx, bb in enumerate(self.bin_boundaries):
			if val >= bb:
				return idx+1
				
			
