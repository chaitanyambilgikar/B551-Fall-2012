import math
from astar_fibheap import AStar

def gridcells(w,h,obstacles):
	"""w,h are width, height
	obstacles a list of x,y-coord 2-tuples.
	
	Returns a w-by-h list of lists
	Cells have value True except for x,y in obstacles, which
	are False"""
	cells = [[True]*w for i in xrange(h)]
	for (x,y) in obstacles:
		cells[x][y] = False
	return cells

def valid_cell(gridmap,state):
	"""gridmap is a list-of-lists as from gridcells()
	state a 2-tuple or 2-list
	
	Returns True if state represents a non-obstacle x,y
	coord on the map, False else."""
	if state[0] >= len(gridmap) or state[0] < 0:
		return False
	if state[1] >= len(gridmap[0]) or state[1] < 0:
		return False
	return gridmap[state[0]][state[1]]

def iterate_map_cells(gridmap):
	"""Returns an iterator over the cell coords in a map, x-major
	ordering"""
	for i in xrange(len(gridmap)):
		for j in xrange(len(gridmap[i])):
			if gridmap[i][j]: #BUGFIX?
			#if gridmap[j]:
				yield (i,j)
	return

def enumerate_map_cells(gridmap):
	"""Returns a flat list of cell coords in x-major order
	i.e., with coords ordered [(0,0), (0,1), (0,2), (1,0), ...]"""
	return [cell for cell in iterate_map_cells(gridmap)]

def map_successors_4(gridmap,state):
	"""With state a 2-tuple or 2-list giving x,y in gridmap,
	for successor states that can be moved to from state,
	iterates over valid (successor,cost) pairs (not considering diagonals)"""
	if not gridmap[state[0]][state[1]]:
		raise ValueError("Input state is not valid")
	candidates = [(1,0),(-1,0),(0,1),(0,-1)]
	for dir in candidates:
		if valid_cell(gridmap,(state[0]+dir[0],state[1]+dir[1])):
			yield ((state[0]+dir[0],state[1]+dir[1]),1.0)
	return

def map_successors_8(gridmap,state):
	"""Iterates over valid (successor,cost) pairs, considering diagonals"""
	if not gridmap[state[0]][state[1]]:
		raise ValueError("Input state is not valid")
	candidates = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
	for dir in candidates:
		if valid_cell(gridmap,(state[0]+dir[0],state[1]+dir[1])):
			cost = (1. if dir[0] == 0 or dir[1] == 0 else math.sqrt(2.0))
			yield ((state[0]+dir[0],state[1]+dir[1]),cost)
	return


class MapAStar(AStar):
	"""Implementation of A* for a single agent moving to the goal.

	Can add multiple goals into the goals member (a set).

	If diagonals is true, allows moving along diagonals.
	"""
	def __init__(self,gridmap,start,goal):
		self.map = gridmap
		self.goals = set([goal])
		self.diagonals = True
		AStar.__init__(self,start)

	def is_goal(self, state):
		return state==(-1,-1) or state in self.goals
		
	def successors(self, state):
		actions = []
		costs = []
		succ_fn = (map_successors_8 if self.diagonals else map_sucessors_4)
		for s,c in succ_fn(self.map,state):
			actions.append(s)
			costs.append(c)
		return (actions,costs)

	def clear_visited(self):
		self.visited = [[None]*len(r) for r in self.map]
		
	def visit(self, state, node):
		if state[0] < 0 and state[1] < 0: return
		self.visited[state[0]][state[1]]=node
		
	def visited_state_node(self, state):
		if state[0] < 0 and state[1] < 0: return None
		return self.visited[state[0]][state[1]]

def search_path(map,start,goals):
	"""Returns a path from start the to a goal state.
	Goals is a list of goal coords
	Returns a list of states on optimal path, or none if no path is found"""
	astar = None
	astar = MapAStar(map,start,goals[0])
	if len(goals) > 1:
		astar.goals = set(goals)
	res = astar.search()
	if not res: return None
	return [n.state for n in astar.result_path()]


