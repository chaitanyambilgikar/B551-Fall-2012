#!/usr/bin/env python
from __future__ import division
from bayesnet import *
from politics import *
import time
import operator

def p1():
        flavor = DiscreteBayesNode("Flavor",[],DiscreteCPT(['Lime','Lemon','Cherry'],[0.3,0.3,0.4]))
        list_of_values= [100,1000,10000]
        # Part A of the 1st problem
        for i in list_of_values:
		no_lime = 0
		no_lemon = 0
		no_cherry = 0
		for j in range(i):
			this_try = flavor.cpt.rand_result(())
			if this_try == 'Lime':
				no_lime += 1
			elif this_try == 'Lemon':
				no_lemon += 1
			elif this_try == 'Cherry':
				no_cherry += 1
		frac_lime = no_lime/i
		frac_lemon = no_lemon/i
		frac_cherry = no_cherry/i
		print "Fraction of times lime was picked: ",frac_lime, " for N = ",i
		print "Fraction of times lemon was picked: ",frac_lemon, " for N = ",i
		print "Fraction of times cherry was picked: ",frac_cherry, " for N = ",i
		
		
		#part b of the question
		
	Lime_n_k = [[0 for i in range(100)]for i in range(3)]
	Lemon_n_k = [[0 for i in range(100)]for i in range(3)]
	Cherry_n_k = [[0 for i in range(100)]for i in range(3)]
	row = 0
	for i in list_of_values:
		for k in range(100):
			no_lime = 0
			no_lemon = 0
			no_cherry = 0
			for j in range(i):
				this_try = flavor.cpt.rand_result(())
				if this_try == 'Lime':
					no_lime += 1
				elif this_try == 'Lemon':
					no_lemon += 1
				elif this_try == 'Cherry':
					no_cherry += 1
			frac_lime = no_lime/i
			frac_lemon = no_lemon/i
			frac_cherry = no_cherry/i
			Lime_n_k[row][k] = frac_lime
			Lemon_n_k[row][k] = frac_lemon
			Cherry_n_k[row][k] = frac_cherry
		row+=1
	
	E_n = [ 0 for i in range(3)]
	for i in range(len(list_of_values)):
		#loop over all k
		for j in range(100):
			#loop over all flavors
			E_n[i] = E_n[i] + (Lime_n_k[i][j] - 0.3)**2 + (Lemon_n_k[i][j] - 0.3)**2 + (Cherry_n_k[i][j] - 0.4)**2
	print "E_n is: ",E_n
def p2():
	# creating the Bayesian network consisting of the two nodes Bin and Candy
	two_node_net = DiscreteBayesNet([DiscreteBayesNode('Bin',[],DiscreteCPT(['b1','b2','b3','b4','b5','b6','b7','b8','b9','b10'] \
	,[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])), DiscreteBayesNode('Flavor',['Bin'],DiscreteCPT(['Lemon','Lime','Cherry'], \
	{('b1',):[0.0, 0.0, 0.1],('b2',):[0.0,1.0,0.0],('b3',):[1.0,0.0,0.0],('b4',):[0.0,0.33,0.67],('b5',):[0.0,0.67,0.33],('b6',):[0.33,0.0,0.67] \
	,('b7',):[0.67,0.0,0.33], ('b8',):[0.33,0.67,0.0],('b9',):[0.67,0.33,0.0],('b10',):[0.3333,0.3333,0.3333] }))])
	
	#to  verify the hand calculated values.
	e = {'Flavor': 'Lime'}
	print two_node_net.enumerate_ask('Bin',e)
	
def p3():
	two_node_net1 = DiscreteBayesNet([DiscreteBayesNode('Bin',[],DiscreteCPT(['b1','b2','b3','b4','b5','b6','b7','b8','b9','b10'] \
	,[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])), DiscreteBayesNode('Flavor',['Bin'],DiscreteCPT(['Lemon','Lime','Cherry'], \
	{('b1',):[0.0, 0.0, 1.0],('b2',):[0.0,1.0,0.0],('b3',):[1.0,0.0,0.0],('b4',):[0.0,0.33,0.67],('b5',):[0.0,0.67,0.33],('b6',):[0.33,0.0,0.67] \
	,('b7',):[0.67,0.0,0.33], ('b8',):[0.33,0.67,0.0],('b9',):[0.67,0.33,0.0],('b10',):[0.33,0.33,0.34] }))])
	e = {'Flavor':'Lime'}
	print "P(Bin|Flavor = 'Lime') for original network:"
	print two_node_net1.enumerate_ask('Bin',e)
	list_of_values = [100,1000,10000]
	for i in list_of_values:
		result = []
		for j in range(i):
			result = result + [ two_node_net1.monte_carlo_sample()]
			#print result
		two_node_net1.train_ml(result)
		print "P(Bin|Flavor = 'Lime') for trained network with ",i," samples:"
		print two_node_net1.enumerate_ask('Bin',e)
def p4():
	
	Naive_net = DiscreteBayesNet([DiscreteBayesNode('Vote',[],DiscreteCPT(['D','R','I'],[0.4,0.4,0.2])),
								DiscreteBayesNode('Gender',['Vote'],DiscreteCPT(['M','F'],{('D',):[0.4,0.6],('R',):[0.6,0.4],('I',):[0.5,0.5]})),
								DiscreteBayesNode(('Race'),['Vote'],DiscreteCPT(['W','B','H','A','O'],{('D',):[0.2,0.2,0.2,0.2,0.2],('R',):[0.4,0.1,0.1,0.2,0.2],('I',):[0.1,0.1,0.1,0.6,0.1]})),
								DiscreteBayesNode(('Age'),['Vote'],DiscreteCPT(['0','1','2','3'],{('D',):[0.3,0.2,0.2,0.3],('R',):[0.2,0.1,0.4,0.3],('I',):[0.2,0.2,0.2,0.4]})),
								DiscreteBayesNode(('Ideology'),['Vote'],DiscreteCPT(['P','M','C'],{('D',):[0.7,0.2,0.1],('R',):[0.1,0.3,0.6],('I',):[0.33,0.33,0.34]})),
								DiscreteBayesNode(('Population'),['Vote'],DiscreteCPT(['LC','SC','SB','ST','RU'],{('D',):[0.4,0.2,0.2,0.1,0.1],('R',):[0.1,0.3,0.1,0.1,0.4],('I',):[0.2,0.2,0.2,0.2,0.2]}))])
	e = {'Gender':'M'}
	list_of_values = [100,1000,10000,100000]
	#for i in list_of_values:
	#	print "Number of repititions   = ",i,"\n"
	#	print Naive_net.monte_carlo_estimate('Vote',e,i)
	train_samples = load_samples_training('poll_train.txt')
	Naive_net.train_ml(train_samples)
	samples = load_samples_testing("poll_train.txt")
	number_of_matches_enu = 0
	number_of_matches_monte = 0
	number_of_matches_likely = 0
	number_of_matches_variable_elim = 0
	number_of_matches_top_down = 0
	for i in range(len(samples)):
	  record = samples[i]
	  #print record[0]
	  #print record[1]
	  this_result_enu = Naive_net.enumerate_ask('Vote',record[0])
	  this_result_monte = Naive_net.monte_carlo_estimate('Vote',record[0],10)
	  this_result_likely = Naive_net.likelihood_weighting_estimate('Vote',record[0],10)
	  order = ['Vote']
	  this_result_variable_elim = Naive_net.variable_elimination_ask('Vote',record[0],order)
	  this_result_top_down = Naive_net.top_down_ask('Vote',record[0],order)
	  #print this_result_monte
	  #print this_result
	  
	  #print maximum_enu
	  if ( max(this_result_enu.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	      number_of_matches_enu += 1
	  if this_result_monte != 'Undefined':
	    if (max(this_result_monte.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	      number_of_matches_monte +=1
	  if (max(this_result_likely.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	    number_of_matches_likely += 1
	  if (max(this_result_variable_elim.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	    number_of_matches_variable_elim += 1
	  if (max(this_result_top_down.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	    number_of_matches_top_down += 1
	print "Number of matches for enumerate_ask was: ",number_of_matches_enu
	print "Accuracy was: ",number_of_matches_enu/len(samples)
	print "Number of matches for monte_carlo was: ",number_of_matches_monte
	print "Accuracy was: ",number_of_matches_monte/len(samples)
	print "Number of matches for weighted likelihood was: ",number_of_matches_likely
	print "Accuracy was: ",number_of_matches_likely/len(samples)
	print "Number of matches for variable elimination was: ",number_of_matches_variable_elim
	print "Accuracy was: ",number_of_matches_variable_elim/len(samples)
	print "Number of matches for top down ask was: ",number_of_matches_top_down
	print "Accuracy was: ",number_of_matches_top_down/len(samples)
	
	MyNet = DiscreteBayesNet([DiscreteBayesNode('Gender',[],DiscreteCPT(['M','F'],[0.5,0.5])),
								DiscreteBayesNode('Age',['Gender'],DiscreteCPT(['0','1','2','3'],{('M',):[0.4,0.2,0.2,0.2],('F',):[0.3,0.4,0.2,0.1]})),
								DiscreteBayesNode(('Race'),[],DiscreteCPT(['W','B','H','A','O'],[0.4,0.2,0.15,0.15,0.1])),
								DiscreteBayesNode(('Population'),[],DiscreteCPT(['LC','SC','SB','ST','RU'],[0.3,0.2,0.3,0.15,0.05])),
								DiscreteBayesNode(('Ideology'),['Race','Population'],DiscreteCPT(['P','M','C'],
								{('W','LC',):[0.6,0.3,0.1],('W','SC',):[0.5,0.3,0.2],('W','SB',):[0.1,0.1,0.8],('W','ST',):[0.2,0.3,0.5],('W','RU',):[0.1,0.3,0.6],
								('B','LC',):[0.7,0.2,0.1],('B','SC',):[0.5,0.3,0.2],('B','SB',):[0.1,0.8,0.1],('B','ST',):[0.2,0.3,0.5],('B','RU',):[0.1,0.2,0.7],
								('H','LC',):[0.8,0.1,0.1],('H','SC',):[0.2,0.2,0.6],('H','SB',):[0.6,0.2,0.2],('H','ST',):[0.2,0.6,0.2],('H','RU',):[0.1,0.1,0.8],
								('A','LC',):[0.5,0.3,0.2],('A','SC',):[0.2,0.3,0.5],('A','SB',):[0.3,0.2,0.5],('A','ST',):[0.8,0.1,0.1],('A','RU',):[0.1,0.1,0.8],
								('O','LC',):[0.4,0.4,0.2],('O','SC',):[0.4,0.2,0.4],('O','SB',):[0.1,0.8,0.1],('O','ST',):[0.4,0.2,0.4],('O','RU',):[0.2,0.4,0.4]})),
								DiscreteBayesNode(('Vote'),['Age','Ideology'],DiscreteCPT(['D','R','I'],
								{('0','P',):[0.7,0.0,0.3],('0','M',):[0.1,0.1,0.8],('0','C',):[0.3,0.5,0.2],
								('1','P',):[0.4,0.4,0.2],('1','M',):[0.1,0.8,0.1],('1','C',):[0.4,0.4,0.2],
								('2','P',):[0.3,0.4,0.3],('2','M',):[0.8,0.1,0.1],('2','C',):[0.4,0.3,0.3],
								('3','P',):[0.5,0.3,0.2],('3','M',):[0.33,0.34,0.33],('3','C',):[0.3,0.0,0.7],}))])
	my_train_samples = load_samples_training('poll_train.txt')
	MyNet.train_ml(my_train_samples)
	my_samples = load_samples_testing("poll_test.txt")
	number_of_matches_enu = 0
	number_of_matches_monte = 0
	number_of_matches_likely = 0
	number_of_matches_variable_elim = 0
	number_of_matches_top_down = 0
	for i in range(len(my_samples)):
	  record = my_samples[i]
	  #print record[0]
	  #print record[1]
	  this_result_enu = MyNet.enumerate_ask('Vote',record[0])
	  this_result_monte = MyNet.monte_carlo_estimate('Vote',record[0],10)
	  this_result_likely = MyNet.likelihood_weighting_estimate('Vote',record[0],10)
	  order = ['Vote']
	  this_result_variable_elim = MyNet.variable_elimination_ask('Vote',record[0],order)
	  #this_result_top_down = MyNet.top_down_ask('Vote',record[0],order)
	  #print this_result_monte
	  #print this_result
	  
	  #print maximum_enu
	  if ( max(this_result_enu.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	      number_of_matches_enu += 1
	  if this_result_monte != 'Undefined':
	    if (max(this_result_monte.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	      number_of_matches_monte +=1
	  if (max(this_result_likely.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	    number_of_matches_likely += 1
	  if (max(this_result_variable_elim.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	    number_of_matches_variable_elim += 1
	  #if (max(this_result_top_down.iteritems(),key = operator.itemgetter(1))[0]  == record[1]):
	   # number_of_matches_top_down += 1
	print "Number of matches for enumerate_ask was: ",number_of_matches_enu
	print "Accuracy was: ",number_of_matches_enu/len(my_samples)
	print "Number of matches for monte_carlo was: ",number_of_matches_monte
	print "Accuracy was: ",number_of_matches_monte/len(my_samples)
	print "Number of matches for weighted likelihood was: ",number_of_matches_likely
	print "Accuracy was: ",number_of_matches_likely/len(my_samples)
	print "Number of matches for variable elimination was: ",number_of_matches_variable_elim
	print "Accuracy was: ",number_of_matches_variable_elim/len(my_samples)
	#print "Number of matches for top down ask was: ",number_of_matches_top_down
	#print "Accuracy was: ",number_of_matches_top_down/len(my_samples)
def main():
	print "######## Problem 1 #########"
	p1()
	print 
	print "######## Problem 2 #########"
	p2()
	print 
	print "######## Problem 3 #########"
	p3()
	print
	print "######## Problem 4 #########"
	p4()
	
	
if __name__ == "__main__":
	main()
