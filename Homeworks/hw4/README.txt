FRAMEWORK

**********************************************************************************************
1. Files and Folders

- data: Examples from the widely used Reuters text classification dataset.

        This folder contains two folders, 'train' and 'test'.
        These folders contain topic subfolders, each of which contains a number of
        news articles on those topics.

        Your job is to build a binary topic classifier.  Since there are many topics
        to choose from, you will select a topic to classify with a command-line
        argument (see How to Run).

- classify.py: main program
- classifiers.py: contains 'NaiveBayesianClassifier' and 'DecisionTreeClassifier' at the moment.
                  Implement your third classfier here
- utils.py: contain the 'FeatureExtractor' class and 'ProbDist' class and other small functions.
            Using these may help you save time.
- data_info.xls: information about the data

**********************************************************************************************
2. How to Run

Usage:
    python classify.py [options] cat1 cat2

The arguments cat1 and cat2 indicate the categories used for positive and negative examples.
A category can contain one or more topics.  For multiple topics in a category, seperate
topic names with a comma (and no space).  For example, 

   python classify.py gold coffee,corn

would build a classifier for the 'gold' topic, using the 'coffee' and 'corn' topics as
negative examples.

Options:
  -h, --help            prints a help message and exits
  -c b/d/t              selects between NaiveBayesClassifier, DecisionTreeClassifier, and
                        ThirdClassifier.
  --fsize=FEATURE_SIZE  number of features (words) to use
  --trmax=TRAIN_MAXSIZE maximum number of training examples.
         when the number of files exceeds this, files will be chosen randomly.
  -q                    minimize prints

**********************************************************************************************
3. How to Implement Your Code

In classifiers.py, there are templates for three classifiers: DecisionTreeClassifier,
NaiveBayesClassifier, and ThirdClassifier.  These correspond to where you should
implement your answers for questions I, II, and III, respectively.  
All classifiers have two major methods train() and test_one().

Your job is to implement the followings
1. NaiveBayesClassifier
- train()
- test_one()

2. DecisionTreeClassifier
The train() and test_one() are already given for this classifier.
your job is to implement
- decision_tree_learning()
- choose_feature()

3. ThirdClassifier
* You are free to choose to implement a new technique other than naive bayesian classifier and decision tree.
* For tuning the existing classifiers, one of good things to do is to try new feature sets.  For example, choose words that are frequent in a category of texts but not in the other category of texts.  (Refer to the comments in create_featureset() in 'utils.py'.)
In case of implementing a new technique, your job will be mainly to implement
- train() 
- test_one()
In case of new feature sets, your job will be mainly to change 
- FeatureExtractor() in utils.py

The train(self,examples,featureset) methods have two arguments 'examples' and 'featureset'.

- 'featureset' is a set of feature names, created by fe.create_featureset().  For example,
	set(['EXIST_to', 'EXIST_its', 'EXIST_of'])
  would state that the words 'to', 'its', and 'of' are the features used by the examples.

- 'examples' is a list of examples.  Each example is a tuple (features, label), where features
   is a dictionary mapping feature names to values.  For example
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
   The label of an example is either 'cat1' or 'cat2', which indicate that the example belongs
   to category 1 or 2, respectively.

Please be sure to read the comments in classifier.py.
