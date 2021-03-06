#####################################
#									#
#		Author : Tarun Gulati		#
#		ID : tgulati@indiana.edu	#
#		Assignment # : 2			#
#		Date : 20th Sept 2012		#
#		Course : B551/Fall 2012		#
#									#
#									#
#####################################


from game_player import *
from gobblet import *
import collections
import sys
import math

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
	
	def evaluate(self, state):
		sum = 0
		totalS = [8, 8]
		boardList = [[0 for j in range(3)] for i in range(2)]
		available = [[0 for j in range(3)] for i in range(2)]
		total = [[0 for j in range(3)] for i in range(2)]
		copyBoard = [[j for j in range(3)]for i in range(8)]
		for i in range(3):
			for j in range(3):
				if state.board[i][j]:
					temp =  state.board_value((i,j))
					if temp.player == 0:
						boardList[0][temp.size] += 1
					elif temp.player == 1:
						boardList[1][temp.size] += 1
		for k in range(3):
			available[0][k] = state.pieces_available(0, k)
			available[1][k] = state.pieces_available(1, k)
			total[0][k] = available[0][k] + boardList[0][k]
			total[1][k] = available[1][k] + boardList[1][k]
		for three in THREES:
			blueValue = 0
			orangeValue = 0
			flag1 = 0
			flag2 = 0
			flag3 = 0
			c1, c2 = three[0]
			c3, c4 = three[1]
			c5, c6 = three[2]
			if state.board[c1][c2]:
				temp1 = state.board_value((c1, c2))
				flag1 += 1
			if state.board[c3][c4]:
				temp2 = state.board_value((c3, c4))
				flag2 += 1
			if state.board[c5][c6]:
				temp3 = state.board_value((c5, c6))
				flag3 += 1
			#checking for an empty row/column/diagonal
			if (flag1 + flag2 + flag3) == 0:
				continue
			# checking for only one piece in a row/column/diagonal
			if (flag1 + flag2 + flag3) == 1:
				#print 'one piece exists!!'
				if flag1 == 1:
					#print 'flag1  ' , temp1.size
					if temp1.size == 2:
						other_player = (temp1.player + 1) % 2
						totalS[other_player] -= 1
						#continue
					if temp1.size == 1:
						if total[(temp1.player + 1) % 2][2] == 0:
							other_player = (temp1.player + 1) % 2
							totalS[other_player] -= 1
							#continue
					if temp1.size == 0:
						if total[(temp1.player + 1) % 2][1] == 0 and total[(temp1.player + 1) % 2][2] == 0:
							other_player = (temp1.player + 1) % 2
							totalS[other_player] -= 1
					continue
				if flag2 == 1:
					#print 'flag1  ' , temp1.size
					if temp2.size == 2:
						other_player = (temp2.player + 1) % 2
						totalS[other_player] -= 1
						#continue
					if temp2.size == 1:
						if total[(temp2.player + 1) % 2][2] == 0:
							other_player = (temp2.player + 1) % 2
							totalS[other_player] -= 1
							#continue
					if temp2.size == 0:
						if total[(temp2.player + 1) % 2][1] == 0 and total[(temp2.player + 1) % 2][2] == 0:
							other_player = (temp2.player + 1) % 2
							totalS[other_player] -= 1
					continue
				if flag3 == 1:
					if temp3.size == 2:
						other_player = (temp3.player + 1) % 2
						totalS[other_player] -= 1
						#continue
					if temp3.size == 1:
						if total[(temp3.player + 1) % 2][2] == 0:
							other_player = (temp3.player + 1) % 2
							totalS[other_player] -= 1
							#continue
					if temp3.size == 0:
						if total[(temp3.player + 1) % 2][1] == 0 and total[(temp3.player + 1) % 2][2] == 0:
							other_player = (temp3.player + 1) % 2
							totalS[other_player] -= 1
					continue
			#checking for 2 pieces in a row/column/diagonal
			if (flag1 + flag2 + flag3) == 2:
				if flag1 == 1 and flag2 == 1:
				#checking if both the pieces belong to the same player
					if temp1.player == temp2.player:
						if temp1.player == state.get_next_player():
							totalS[state.get_next_player()] += 1
							continue
					#checking if both the pieces belong to different players
					if temp1.player != temp2.player:
						#piece 1 and 2 are both LARGE
						if temp1.size == 2 and temp2.size == 2:
							continue
						#one piece is LARGE and the other is a MEDIUM
						if (temp1.size == 2 and temp2.size == 1) or (temp1.size == 1 and temp2.size == 2):
							if temp1.size == 2:
								other_player = (temp1.player + 1) % 2
								totalS[other_player] -= 1
								continue
							else:
								totalS[temp1.player] -= 1
								continue
						#piece 1 and 2 are both MEDIUM
						if temp2.size == 1 and temp1.size == 1:
							if total[temp2.player][2] == 0 and total[temp1.player][2] == 0:
								continue
							elif total[temp2.player][2] == 0:
								totalS[temp2.player] -= 1
								continue
							elif total[temp1.player][2] == 0:
								totalS[temp1.player] -= 1
								continue
						#piece 1 and 2 are both SMALL
						if temp2.size == 0 and temp1.size == 0:
							if (total[(temp2.player + 1) % 2][1] == 0 and total[(temp2.player + 1) % 2][2] == 0) and (total[(temp1.player + 1) % 2][1] == 0 and total[(temp1.player + 1) % 2][2] == 0):
								continue
							elif total[(temp2.player + 1) % 2][1] == 0 and total[(temp2.player + 1) % 2][2] == 0:
								totalS[temp2.player] -= 1
								continue
							elif total[(temp1.player + 1) % 2][1] == 0 and total[(temp1.player + 1) % 2][2] == 0:
								totalS[temp1.player] -= 1
								continue
						#one is SMALL and one is MEDIUM
						if (temp2.size == 1 and temp1.size == 0) or (temp2.size == 0 and temp1.size == 1):
							if temp2.size == 1 and temp1.size == 0:
								if total[temp1.player][2] == 0 and total[temp2.player][2] == 0 and total[temp2.player][1] == 0:
									continue
								elif total[temp1.player][2] == 0:
									totalS[temp1.player] -= 1
									continue
								elif total[temp2.player][1] == 0 and total[temp2.player][2] == 0:
									totalS[temp2.player] -= 1
									continue
							elif temp1.size == 1 and temp2.size == 0:
								if total[temp2.player][2] == 0 and total[temp1.player][2] == 0 and total[temp1.player][1] == 0:
									continue
								elif total[temp2.player][2] == 0:
									totalS[temp2.player] -= 1
									continue
								elif total[temp1.player][1] == 0 and total[temp1.player][2] == 0:
									totalS[temp1.player] -= 1
									continue
						#one is SMALL and one is LARGE
						if (temp2.size == 2 and temp1.size == 0) or (temp2.size == 0 and temp1.size == 2):
							if temp2.size == 2:
								totalS[temp1.player] -= 1
								continue
							elif temp1.size == 2:
								totalS[temp2.player] -= 1
								continue
				if flag2 == 1 and flag3 == 1:
				#checking if both the pieces belong to the same player
					if temp2.player == temp3.player:
						if temp2.player == state.get_next_player():
							totalS[state.get_next_player()] += 1
							continue
					#checking if both the pieces belong to different players
					if temp2.player != temp3.player:
						#piece2 and 3 are both LARGE
						if temp2.size == 2 and temp3.size == 2:
							continue
						#one is LARGE and one is MEDIUM
						if (temp2.size == 2 and temp3.size == 1) or (temp2.size == 1 and temp3.size == 2):
							if temp2.size == 2:
								other_player = (temp2.player + 1) % 2
								totalS[other_player] -= 1
								continue
							else:
								totalS[temp2.player] -= 1
								continue
						#piece 2 and 3 are both MEDIUM
						if temp2.size == 1 and temp3.size == 1:
							if total[temp2.player][2] == 0 and total[temp3.player][2] == 0:
								continue
							elif total[temp2.player][2] == 0:
								totalS[temp2.player] -= 1
								continue
							elif total[temp3.player][2] == 0:
								totalS[temp3.player] -= 1
								continue
						#piece 2 and 3 are both SMALL
						if temp3.size == 0 and temp2.size == 0:
							if (total[(temp2.player + 1) % 2][1] == 0 and total[(temp2.player + 1) % 2][2] == 0) and (total[(temp3.player + 1) % 2][1] == 0 and total[(temp3.player + 1) % 2][2] == 0):
								continue
							elif total[(temp2.player + 1) % 2][1] == 0 and total[(temp2.player + 1) % 2][2] == 0:
								other_player = (temp2.player + 1) % 2
								totalS[other_player] -= 1
								continue
							elif total[(temp3.player + 1) % 2][1] == 0 and total[(temp3.player + 1) % 2][2] == 0:
								other_player = (temp3.player + 1) % 2
								totalS[other_player] -= 1
								continue
						#one is SMALL and one is MEDIUM
						if (temp3.size == 1 and temp2.size == 0) or (temp3.size == 0 and temp2.size == 1):
							if temp2.size == 1 and temp3.size == 0:
								if total[temp3.player][2] == 0 and total[temp2.player][2] == 0 and total[temp2.player][1] == 0:
									continue
								elif total[temp3.player][2] == 0:
									totalS[temp3.player] -= 1
									continue
								elif total[temp2.player][1] == 0 and total[temp2.player][2] == 0:
									totalS[temp2.player] -= 1
									continue
							elif temp3.size == 1 and temp2.size == 0:
								if total[temp2.player][2] == 0 and total[temp3.player][2] == 0 and total[temp3.player][1] == 0:
									continue
								elif total[temp2.player][2] == 0:
									totalS[temp2.player] -= 1
									continue
								elif total[temp3.player][1] == 0 and total[temp3.player][2] == 0:
									totalS[temp3.player] -= 1
									continue
						#one is SMALL and one is LARGE
						if (temp3.size == 2 and temp2.size == 0) or (temp3.size == 0 and temp2.size == 2):
							if temp3.size == 2:
								totalS[temp2.player] -= 1
								continue
							elif temp2.size == 2:
								totalS[temp3.player] -= 1
								continue
				if flag3 == 1 and flag1 == 1:
				#checking if both the pieces belong to the same player
					if temp3.player == temp1.player:
						if temp3.player == state.get_next_player():
							totalS[state.get_next_player()] += 1
							continue
					#checking if both the pieces belong to different players
					if temp3.player != temp1.player:
						#piece 1 and 3 are both LARGE
						if temp3.size == 2 and temp1.size == 2:
							continue
						#one is MEDIUM and one is LARGE
						if (temp3.size == 2 and temp1.size == 1) or (temp3.size == 1 and temp1.size == 2):
							if temp3.size == 2:
								totalS[temp1.player] -= 1
								continue
							else:
								totalS[temp3.player] -= 1
								continue
						#piece 1 and 3 are both MEDIUM
						if temp3.size == 1 and temp1.size == 1:
							if total[temp3.player][2] == 0 and total[temp1.player][2] == 0:
								continue
							elif total[temp3.player][2] == 0:
								totalS[temp3.player] -= 1
								continue
							elif total[temp1.player][2] == 0:
								totalS[temp1.player] -= 1
								continue
						#piece 1 and 3 are both SMALL
						if temp3.size == 0 and temp1.size == 0:
							if (total[(temp3.player + 1) % 2][1] == 0 and total[(temp3.player + 1) % 2][2] == 0) and (total[(temp1.player + 1) % 2][1] == 0 and total[(temp1.player + 1) % 2][2] == 0):
								continue
							elif total[(temp3.player + 1) % 2][1] == 0 and total[(temp3.player + 1) % 2][2] == 0:
								totalS[temp3.player] -= 1
								continue
							elif total[(temp1.player + 1) % 2][1] == 0 and total[(temp1.player + 1) % 2][2] == 0:
								totalS[temp1.player] -= 1
								continue
						#one is SMALL and one is MEDIUM
						if (temp3.size == 1 and temp1.size == 0) or (temp3.size == 0 and temp1.size == 1):
							if temp3.size == 1 and temp1.size == 0:
								if total[temp1.player][2] == 0 and total[temp3.player][2] == 0 and total[temp3.player][1] == 0:
									continue
								elif total[temp1.player][2] == 0:
									totalS[temp1.player] -= 1
									continue
								elif total[temp3.player][1] == 0 and total[temp3.player][2] == 0:
									totalS[temp3.player] -= 1
									continue
							elif temp1.size == 1 and temp3.size == 0:
								if total[temp3.player][2] == 0 and total[temp1.player][2] == 0 and total[temp1.player][1] == 0:
									continue
								elif total[temp3.player][2] == 0:
									totalS[temp3.player] -= 1
									continue
								elif total[temp1.player][1] == 0 and total[temp1.player][2] == 0:
									totalS[temp1.player] -= 1
									continue
						#one is SMALL and one is LARGE
						if (temp3.size == 2 and temp1.size == 0) or (temp3.size == 0 and temp1.size == 2):
							if temp3.size == 2:
								totalS[temp1.player] -= 1
								continue
							elif temp1.size == 2:
								totalS[temp3.player] -= 1
								continue
			#when three exist in a row
			if (flag1 + flag2 + flag3) == 3:
				#all three belong to the same player
				if (temp1.player == temp2.player == temp3.player):
					totalS[temp1.player] += 2
				if (temp1.player != temp3.player and temp2.player != temp3.player) or (temp1.player != temp2.player and temp3.player != temp2.player) or (temp3.player != temp1.player and temp2.player != temp1.player):
					if temp1.player == temp2.player:
						if temp3.size !=2:
							if temp3.size == 0:
								if total[temp1.player][1] != 0 or total[temp1.player][2] != 0:
									totalS[temp1.player] += 1
									continue
							elif temp3.size == 1:
								if total[temp1.player][2] != 0:
									totalS[temp1.player] += 1
									continue
					if temp2.player == temp3.player:
						if temp1.size !=2:
							if temp1.size == 0:
								if total[temp2.player][1] != 0 or total[temp2.player][2] != 0:
									totalS[temp2.player] += 1
									continue
							elif temp1.size == 1:
								if total[temp2.player][2] != 0:
									totalS[temp2.player] += 1
									continue
					if temp1.player == temp3.player:
						if temp2.size !=2:
							if temp2.size == 0:
								if total[temp1.player][1] != 0 or total[temp1.player][2] != 0:
									totalS[temp1.player] += 1
									continue
							elif temp2.size == 1:
								if total[temp1.player][2] != 0:
									totalS[temp1.player] += 1
									continue
		sum = totalS[0] - totalS[1]
		return sum
	
	def terminal_checks(self, state, h, players):
		# If first player wins, that's a positive
		if state.is_win(players[0]):
			return (sys.maxint, None)
		# If second player wins, that's a negative
		elif state.is_win(players[1]):
			return (-sys.maxint-1, None)
		
		# If there are no more expansions allowed, or if
		# we hit the horizon, evaluate
		if state.expansions_count() <= 0 or h <= 0:
			#print state.expansions_count() , h
			return (self.evaluate(state), None)
		
		# if no termination, return None
		return None
	
	def minimax_search(self, state, h):
		players = state.get_players()
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		successors = state.successors()
		if len(successors) == 0:
			return (0, None)
		values = [self.minimax_search(s.state, h-1) for s in successors]
		values = [x[0] for x in values]
		if state.get_next_player() == players[0]:
			max_idx = max(enumerate(values), key=lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key=lambda x: x[1])[0]
		# Return the minimax value and corresponding move
		return (values[max_idx], successors[max_idx].move)
	
	def minimax_move(self, state, visited):
		exp = state.expansions_count()
		print 'expansion count : ' , exp
		h = int(math.floor(float(exp) ** (12.0 / 26.0)))
		print "nightfury : ",state.get_next_player()," search depth",h
		return self.minimax_search(state,h)[1]
	
	
	def alpha_beta_search(self, state, h, a, b):
		# Get player IDs
		players = state.get_players()
		player = state.get_next_player()
		
		# Do most of our terminal checks
		term = self.terminal_checks(state, h, players)
		if term != None:
			return term
		successors = state.successors()
		if len(successors) == 0:
			return (0, None)
		
		# We start out with a low best-value and no move
		v = -sys.maxint-1 if player == players[0] else sys.maxint
		m = None
		for s in successors:
			s_val = self.alpha_beta_search(s.state, h-1, a, b)
			if (player == players[0] and s_val[0] > v) \
					or (player == players[1] and s_val[0] < v):
				v = s_val[0]
				m = s.move
			if (player == players[0] and v >= b) \
					or (player == players[1] and v <= a):
				return (v, m)
			a = a if player == players[1] else max(a,v)
			b = b if player == players[0] else min(b,v)
		# return the best value, move we found
		return (v,m)
	
	def alpha_beta_move(self, state, visited):
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (10.0 / 26.0)))
		print "Player",state.get_next_player(),"search depth",h
		return self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint)[1]
		
	def tournament_move(self, state, visited):
		return self.alpha_beta_move(state, visited)
		
		
def make_player(playerID):
	return GobbletPlayer(playerID)
