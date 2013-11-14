#Successor function implementation
from collections import deque
import heapq

DICT_FILENAME = '/home/chaitanya/Temp_py/words.txt'
def make_dictionary(size):
	"""Returns a Python set object containing words of the given size, loaded
	from the file whose name is given in the global variable DICT_FILENAME.
	This set object can be used for fast lookups of arbitrary strings to see
	if they're legal words (i.e., by using Python's "if VALUE in SET:"
	syntax)."""
	with open(DICT_FILENAME) as fin:
		words = fin.readlines()
	words = [w.strip().lower() for w in words if len(w.strip()) == size]
	return set(words)    
def get_successor(start):
    all_possible = make_dictionary(len(start))
    correct =[]
    for i in range(len(start)):
        temp = start
        for j in range(97,123):
            s = start[0:i] + chr(j) + start[i+1:len(start)]
            if s in all_possible:
                if s != temp:
                    print s
                    correct = correct + [s]
    print correct
        
""" for the BFS revisited problem:
according to the ppt,it says to keep all the generated states in a list called VISITED
This can be implemented as a hash table (like a dictionary) or as a seperate data structure
I think using it like a dictionary would be better where we could assign a key as a number and the value could be the state (or the word).
So when we expand a node  and generate it's successors
for s in problem.successors(n.state)
        if s.state in visited:
                break
        c=SearchNode(s,n)
        stats.on_generate()
        visited = visited + [s]

For Depth limited DFS:
It tries to search (recursively) until the depth limit is hit. If it is hit at one node, it sets the boolean cutoff to true. It then
retraces back to the parent and visits its other successors. If any one of them is the goal, it returns true. If all such parents
at depth limit-1 have children at depth limit which are not the goal states (which means that the boolean cutoff has been set to
true) it returns the cutoff.
For IDS:
IDS is like Depth limited DFS, but with the variation that if a limit is hit, and all nodes at that depth are not goal nodes, then
instead of returning cutoff as the result, it must set the new limit as limit+1 and call Depth limited DFS again.
"""
def depth_limited_DFS_callback(problem,limit,curnode):
        """A subroutine for depth_limited_DFS.  If the depth limit is hit, then 
        the SearchResult.successful member is set to the string 'cutoff'
        rather than True or False."""
        stats = SearchStats()

        #BONUS POINTS: Implement this so that infeasible queries do not
        #run forever
        
        if problem.is_goal(curnode.state):
                return (stats,SearchResult(True,curnode))

        #test for depth limit
        if curnode.depth == limit:
                return (stats,SearchResult('cutoff'))

        #expand to successors
        stats.on_expand()
        succ = problem.successors(curnode.state)
        cutoff = False
        for s in succ:
                stats.on_generate()
                c = SearchNode(s,curnode)
                (sstats,sres) = depth_limited_DFS_callback(problem,limit,c)
                stats += sstats

                #test for solution
                if sres.successful==True:
                        return (stats,sres)
                #test for cutoff
                if sres.successful=='cutoff':
                        cutoff = True
        
        #this branch failed
        if cutoff:
                return (stats,SearchResult('cutoff'))
        else:
                return (stats,SearchResult(False))

def depth_limited_DFS_forIDS(problem,limit):
        """Performs an iterative-deepening search for the given WordProblem
        'problem'. If the depth limit is hit, then the SearchResult.successful
        member is set to the string 'cutoff' rather than True or False. """

        print "Starting depth-limited(%d) search for IDS..."%(limit,)
        (stats,res) = depth_limited_DFS_callback(problem,limit,SearchNode(problem.start))
        while(res.successful=='cutoff'):
                limit+=1
                (stats,res) = depth_limited_DFS_callback(problem,limit,SearchNode(problem.start))
        #mark the start node
        stats.on_generate()
        return (stats,res)
            
""" For A* search:
The heuristic:
Lets start with the heuristic of Hamming distance. The Hamming distance between two words is defined as the number of substitutions
required to transform one word to the other, where each transformation must lead to a legal word.
Is this admissible?
For a heuristic function h(n) to be admissible, it must never overestimate the cost of reaching to the goal node, and the
h(g) = 0 , where g is the goal state.
Lets see if this holds true for Hamming distance:
Assume the start state as take and the goal state as talk.
So, h(start) = 2. This holds true as 2 is a good lowerbound for the number of transformations needed.

Coding:
Wee need to define additional attributes for every node.
Each node will have h(n), g(n) and f(n)
g(n) can be calculated as no transformations taken from the root. So for root,
root.g = 0
and for every other node,
n.g = self.parent.g + 1

h(n) can be calculated as number of transformations required to get to the goal state
sum = 0
for ch1, ch2 in zip(n.state, goal.state):
       if(ch1 != ch2):
               sum+=1

return sum

algo for A* search
root <-- SearchNode(problem.start)
the g, n and f values are assigned
if problem.is_goal(root.state)
return true
q=[]
visited = []
heapq.heappush(q,[root])
visited = visited + [root]
while len(q)>0:
        n = heapq.heappop(q)
        stats.on_expand()
        for s in problem.successors(n.state):
                if s in visited:
                        stats.on_revisit()
                        break
                        
                c = SearchNode(s,n)
                g,n and f values are assigned here
                if problem.is_goal(s):
                        return (stats,SearchResult(True,c))
                heapq.heappush(q,c)
                visited = visited + [s]
return (stats,SearchResult(False))



"""
