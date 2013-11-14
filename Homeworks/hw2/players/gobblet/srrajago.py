import collections
import sys
import math


PLAYERS = ['B', 'O']
SIZES = ['S', 'M', 'L']
THREES = [[(0,0), (1,1), (2,2)], [(2,0), (1,1), (0,2)], [(0,0), (1,0), (2,0)],
			[(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)], [(0,0), (0,1), (0,2)],
			[(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)]]
DIAGONAL_PLACES = THREES[:2]



from game_player import *
from gobblet import *

class GobbletPlayer(GamePlayer):
	def __init__(self, playerID):
		GamePlayer.__init__(self, playerID)
		
	# EXAMPLE: Loads a file from the same directory this module is stored in
	#  and returns its contents.  Pattern any file operations you do in your
	#  player on this model.
	#
	# NB: Make a note of the working directory before you cd to the module
	#  directory, and restore it afterward!  The rest of the program may break
	#  otherwise.
        def load_file(self, fname):
		wd = os.getcwd()
		os.chdir("players/gobblet")
		fin = open(fname)
		contents = fin.read()
		fin.close()
		os.chdir(wd)
		return contents


	
	# gets player given a piece, and returns None if there is no piece
	def get_player(self,game_piece):
                if game_piece != None :
                        return game_piece.player
                return None


        #returns the number of open lines for the opponent
        def open3(self, state, otherPlayer):
		s = 0
		for three in THREES:
                        flag = True
                        for x in three:
                                if (self.get_player(state.board_value(x)) == otherPlayer):
                                        flag  = False
                        if (flag):
                                s += 1
                return s


        #returns a list indicatind the number of piecec on board for a given player. Active pieces are at index 0, pieces are counted at larger depending on the depth in the board stack
        def no_of_pieces_on_board(self, state, player):
                value_stack = [0,0,0]
                for i in range(3):
                        for j in range(3):
                                stack = state.board_stack((i,j))
                                no_of_pieces = len(stack)
                                for k in range(no_of_pieces,0,-1):
                                        if stack[k-1].player == player:
                                                value_stack[no_of_pieces - k] += 1
                
                return value_stack
                                        

        # returns the number which gives two in a line for a player such that the third  in the line can be filled by the player.               
        def two_in_row(self, state, player,other_player):
                s = 0
                for three in THREES:
                        other = []
                        player_pts = 0
                        none_pts = 0
                        for x in three:
                                player_in_x = self.get_player(state.board_value(x))
                                if player_in_x == player:
                                        player_pts += 1
                                elif player_in_x == None:
                                        none_pts +=1
                                else:                                        
                                        other.append(x)
                        if player_pts == 2 and none_pts == 0:                       
                                for i in range(len(other)):
                                        flag = False
                                        size = state.board_value(other[i]).size
                                        for j in range(size+1,3):
                                                if state.pieces_available(other_player,j)>0:
                                                        none_pts +=1
                                        
                        if player_pts == 2 and none_pts >= 1:
                                s+=1
                                
                return s

	
	#returns values to promote the player to put pieces at the center, higher value for the larger piece
	def center_piece(self, state, player):
                c = state.board_value((1,1))
                if c == None:
                        return 0
                elif c.player == player and c.size == 2:
                        return 3
                elif c.player == player and c.size == 1:
                        return 2
                elif c.player == player and c.size == 0:
                        return 1
                return 0
        
        #evaluation function
	def evaluate(self, state, players):
                value_stack_self = self.no_of_pieces_on_board(state, players[0])
		value_stack_opponent = self.no_of_pieces_on_board(state, players[1])
		weights = [.2,1,1,1,0.5,0.2]
                attribute = []
		attribute.append(self.open3(state, players[1]) - self.open3(state, players[0]))
		attribute.append(self.two_in_row(state, players[0],players[1])*20 - self.two_in_row(state, players[1],players[0])*40)
		attribute.append(value_stack_self[0] - value_stack_opponent[0])
		attribute.append(value_stack_self[1] - value_stack_opponent[1])
		attribute.append(value_stack_self[2] - value_stack_opponent[2])
		attribute.append(self.center_piece(state, players[0]) - self.center_piece(state, players[1]))
		
		
		val = 0
		for i in range(len(weights)):
                        val += weights[i]*attribute[i]
		return val
	
        #check if terminal condition. If yes return value associated
	def terminal_checks(self, state, h, players):
		# If current player wins, that's a positive'
		if state.is_win(players[0]):
                        return (sys.maxint, None)
		# If opponent wins, that's a negative
		elif state.is_win(players[1]):
			return (-sys.maxint-1000, None)
		
		# If there are no more expansions allowed, or if
		# we hit the horizon, evaluate
		if state.expansions_count() <= 0 or h <= 0:
        		return (self.evaluate(state, players), None)
		
		# if no termination, return None
		return None

	#recursive method which is called during minimax search. players tells who current player
	def minimax_search(self, state, h,players):
		# Get player IDs
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		
		# Get successor states
		# We should check to see if this is None, but since we just
		#  checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		
		if len(successors) == 0:
			return (0, None)
		
		# Recur on each of the successor states (note we take the state out
		# of the successor tuple with x[1] and decrease the horizon)
		values = [self.minimax_search(s.state, h-1,players) for s in successors]
		# We're not interested in the moves made, just the minimax values
		values = [x[0] for x in values]
		# Look for the best among the returned values
		# Max if we're current player
		# Min if we're opponent
		if state.get_next_player() == players[0]:
                        #print 'h max' + str(h)
			max_idx = max(enumerate(values), key=lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key=lambda x: x[1])[0]
			
		# Return the minimax value and corresponding move
		return (values[max_idx], successors[max_idx].move)

        #method to be invoked for mini max algorithm
	def minimax_move(self, state, visited):
		# Adjust our play horizon to the expansion count,
		# based on a maximum branching factor of 8.
		# NB: This may not be the right formula!
		exp = state.expansions_count()

		#b is the branching factor; taken as 27
		b = 27

		#Horizon is calculated.
		h = int(math.floor(math.log((exp*(b-1)+1),10)/math.log(b,10)))
                print "Player",state.get_next_player(),"search depth",h
                #if current players such that the current player gets 0 and opponent gets 1
		players = [0,1]
		current_player = state.get_next_player()
		if current_player == 1:
                        players = [1,0]
		c =  self.minimax_search(state,h,players)
                print "evaluation value ", c[0]
		return c[1]
	
	# Get a move for the indicated state, using an alpha-beta search.
	def alpha_beta_move(self, state, visited):
		#average branching factor, b = 27.
		exp = state.expansions_count()
		b = 27
                #horizon for alpha beta
                h = int(math.floor(1.33 * math.log(exp,10)/math.log(b,10)))+1
                players = [0,1]
		current_player = state.get_next_player()
		if current_player == 1:
                        players = [1,0]
		exp = state.expansions_count()
		print "Player",state.get_next_player(),"search depth",h
		c = self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint, players)
		print "evaluation value ", c[0]
		return c[1]

	#returns alpha-beta move	
	def tournament_move(self, state, visited):
		return self.alpha_beta_move(state, visited)

	#recursive method called during alpha-beta search
	def alpha_beta_search(self, state, h, a, b, players):
		# Get player IDs
		player = state.get_next_player()
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		
		# Get successor states
		# We should check to see if this is None, but since we just
		#  checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)
		
		# We start out with a low best-value and no move
		v = -sys.maxint-1 if player == players[0] else sys.maxint
		m = None
		for s in successors:
			# Recur on the successor state
			s_val = self.alpha_beta_search(s.state, h-1, a, b, players)
			# If our new value is better than our best value, update the best
			#  value and the best move
			if (player == players[0] and s_val[0] > v) \
					or (player == players[1] and s_val[0] < v):
				v = s_val[0]
				m = s.move
			# If we're maxing and exceeding the min above, just return
			# Likewise if we're minning and exceeding the max above
			if (player == players[0] and v >= b) \
					or (player == players[1] and v <= a):
				return (v, m)
			# Update a,b for the next successor
			a = a if player == players[1] else max(a,v)
			b = b if player == players[0] else min(b,v)
		# return the best value, move we found
		return (v,m)
		
	
		
def make_player(playerID):
	return GobbletPlayer(playerID)
