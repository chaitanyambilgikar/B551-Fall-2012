import math
import sys

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

        
	def check_board_stack(self, state, otherPlayer, locations, s):
                val1, val2, val3 = locations
                t11, t12 = val1
                t21, t22 = val2
                t31, t32 = val3
                if (state.board_value (val1) != None and state.board_value (val1).player == otherPlayer) and \
                   (state.board_value (val2) is None or state.board_value (val1).player != state.board_value (val2).player) and \
                   (state.board_value (val3) is None or state.board_value (val1).player != state.board_value (val3).player):
                        if state.board_value (val1).size < 2:
                                s = s+1
                if (state.board_value (val2) != None and state.board_value (val2).player == otherPlayer) and \
                   (state.board_value (val1) is None or state.board_value (val2).player != state.board_value (val1).player) and \
                   (state.board_value (val3) is None or state.board_value (val2).player != state.board_value (val3).player):
                         if state.board_value (val2).size < 2:
                                s = s+1
                if (state.board_value (val3) != None and state.board_value (val3).player == otherPlayer) and \
                   (state.board_value (val1) is None or state.board_value (val3).player != state.board_value (val1).player) and \
                   (state.board_value (val2) is None or state.board_value (val3).player != state.board_value (val2).player):
                         if state.board_value (val3).size < 2:
                                s = s+1
                if (state.board_value (val1) != None and state.board_value (val1).player == otherPlayer) and \
                   (state.board_value (val2) is None) and \
                   (state.board_value (val3) and state.board_value (val3).player == otherPlayer):
                        s = s-1
                if (state.board_value (val3) != None and state.board_value (val3).player == otherPlayer) and \
                   (state.board_value (val1) is None) and \
                   (state.board_value (val2) and state.board_value (val2).player == otherPlayer):
                        s-=1
                if (state.board_value (val2) != None and state.board_value (val2).player == otherPlayer) and \
                   (state.board_value (val3) is None) and \
                   (state.board_value (val1) and state.board_value (val1).player == otherPlayer):
                        s-=1
                return s
                        
                

	def open3(self, state, otherPlayer):
		s=0
		
		if (state.board_value ((0,0)) is None or state.board_value ((0,0)).player != otherPlayer ) and \
                   (state.board_value ((1,1)) is None or state.board_value ((1,1)).player != otherPlayer) and \
                   (state.board_value ((2,2)) is None or state.board_value ((2,2)).player != otherPlayer):
                        s+=1
                elif (state.board_value ((0,0)) and state.board_value ((0,0)).player == otherPlayer) or (state.board_value ((1,1)) and state.board_value ((1,1)).player == otherPlayer) or (state.board_value ((2,2)) and state.board_value ((2,2)).player == otherPlayer):
                        s= self.check_board_stack(state, otherPlayer, ((0,0),(1,1),(2,2)), s)
                if (state.board_value ((0,2)) is None or state.board_value ((0,2)).player != otherPlayer) and \
                   (state.board_value ((1,1)) is None or state.board_value ((1,1)).player != otherPlayer) and \
                   (state.board_value ((2,0)) is None or state.board_value ((2,0)).player != otherPlayer):
                        s+=1
                elif (state.board_value ((0,2)) and state.board_value ((0,2)).player == otherPlayer) or (state.board_value ((1,1)) and state.board_value ((1,1)).player == otherPlayer) or (state.board_value ((2,0)) and state.board_value ((2,0)).player == otherPlayer):
                        s= self.check_board_stack(state, otherPlayer, ((0,2),(1,1),(2,0)),s)
                for i in range(3):
			if (state.board_value((i,0)) is None or state.board_value((i,0)).player != otherPlayer) and \
                           (state.board_value((i,1)) is None or state.board_value((i,1)).player != otherPlayer) and \
                           (state.board_value((i,2)) is None or state.board_value((i,2)).player != otherPlayer):
				s += 1
			elif (state.board_value((i,0)) and state.board_value ((i,0)).player == otherPlayer) or (state.board_value ((i,1)) and state.board_value ((i,1)).player == otherPlayer) or (state.board_value ((i,2)) and state.board_value ((i,2)).player == otherPlayer):
                                s= self.check_board_stack(state, otherPlayer, ((i,0),(i,1),(i,2)),s)
			if (state.board_value((0,i)) is None or state.board_value((0,i)).player != otherPlayer) and \
			   (state.board_value((1,i)) is None or	state.board_value((1,i)).player != otherPlayer) and \
			   (state.board_value((2,i)) is None or	state.board_value((2,i)).player != otherPlayer):
				s += 1
			elif (state.board_value ((0,i)) and state.board_value ((0,i)).player == otherPlayer) or \
                             (state.board_value ((1,i)) and state.board_value ((1,i)).player == otherPlayer) or \
                             (state.board_value ((2,i)) and state.board_value ((2,i)).player == otherPlayer):
                                s= self.check_board_stack(state, otherPlayer, ((0,i),(1,i),(2,i)),s)
		
		return s
	
	# A simple evaluation function for tic-tac-toe
	#
	# Returns the number of 3-in-a-rows available to player X, minus the
	# number of 3-in-a-rows available to player O.
	#
	# "state" is a TicTacToeState object
	def evaluate(self, state):
		players = state.get_players()
		f = self.open3(state, players[1]) - self.open3(state, players[0])
		return f
	
	def terminal_checks(self, state, h, players):
		if state.is_win(players[0]):
			return (sys.maxint, None)
		elif state.is_win(players[1]):
			return (-sys.maxint-1, None)

		if state.expansions_count() <= 0 or h <= 0:
			return (self.evaluate(state), None)
		
		return None
		
	def minimax_search(self, state, h):
                ##Borrowed from tictactoe 
		# Get player IDs
		players = state.get_players()
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)
		i=0

		values = [self.minimax_search(s.state, h-1) for s in successors]

		values = [x[0] for x in values]
		if state.get_next_player() == players[0]:
			max_idx = max(enumerate(values), key=lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key=lambda x: x[1])[0]

		return (values[max_idx], successors[max_idx].move)
	
	
	# A helper function for alpha_beta_move().  See minimax_search().
	#
	# a,b are alpha, beta values.
	def alpha_beta_search(self, state, h, a, b):
		players = state.get_players()
		player = state.get_next_player()
		
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term

		successors = state.successors()
		if len(successors) == 0:
			return (0, None)
		
		if player == players[0]:
                        v = -sys.maxint-1 
		else:
                        v = sys.maxint
		m = None
		for s in successors:
                        values = self.alpha_beta_search(s.state, h-1, a, b) 
                        if (player == players[0] and values[0] > v) or (player == players[1] and values[0] < v):
                                v = values[0]
                                m = s.move
                        if v>=b and player == players[0]:
                                return (v,m)
                        if player == players[0]:
                                a = max(a,v)
                        if v<=a and player == players[1]:
                                return (v,m)
                        if player == players[1]:
                                b = min(b,v)
		return (v,m)
		
	
	# Get a move for the indicated state, using a minimax search.
	#
	# "state" is still a TicTacToeState object
	def minimax_move(self, state, visited):
		exp = state.expansions_count()
		h = int(math.floor(((float(exp)*2.0) % 2)+5))
		print "Player",state.get_next_player(),"search depth",h
		return self.minimax_search(state,h)[1]
	
	# Get a move for the indicated state, using an alpha-beta search.
	#
	# state is a TicTacToeState
	def alpha_beta_move(self, state, visited):
		exp = state.expansions_count()
		h = int(math.floor(((float(exp)*2.0) % 2)+3))
		print "Player",state.get_next_player(),"search depth",h
		return self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint)[1]
		
	def tournament_move(self, state, visited):
                return self.alpha_beta_move(state, visited)
		
		
def make_player(playerID):
	return GobbletPlayer(playerID)
