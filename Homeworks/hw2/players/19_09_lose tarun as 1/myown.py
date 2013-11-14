import collections
import time
import sys
import math
from game_player import *
from gobblet import *
""" You now have to change the values for when there are three pieces in a row. remember that state.get_next_player() return 'you' always"""
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
		 #first find out how many pieces of each size of each player are on the board and on the stack
	  #print "It is ",state.get_next_player()," 's turn"
	  player_list = state.get_players()
	  mine = state.get_next_player()
	  mine = (mine+1)%2
	  
	  total_avail = [[0 for i in range(3)]for i in range(len(player_list))]
	  on_board = [[0 for i in range(3)]for i in range(len(player_list))]
	  for i in range(3):
	    for j in range(3):
	      if state.board[i][j]:
		temp_player = state.board_value((i,j))
		on_board[temp_player.player][temp_player.size] +=1
		total_avail[temp_player.player][temp_player.size]+=1
		#print temp_player.player, temp_player.size
	  #print "Pieces on the board are: ",on_board
	  on_stack =  [[0 for i in range(3)]for i in range(len(player_list))]
	  for i in range(len(player_list)):
	    for j in range(3):
	      on_stack[i][j] = state.pieces_available(i,j)
	      total_avail[i][j] = total_avail[i][j] + on_stack[i][j]
	  #print "Pieces on the stack (unused) are: ",on_stack
	  
	  #print "Total number of pieces are: ",total_avail
	
	  #Now the fun starts!!..Checking every entry in THREES according to the rules we defined! Enjoy (sarcastic!)
	  value = [8,8]
	  for three in THREES:
		  
		  a,b = three[0]
		  c,d = three[1]
		  e,f = three[2]
		  flag1=flag2=flag3=0
		  if state.board[a][b]:
		
			  piece_one = state.board_value((a,b))
			  flag1=1
		  if state.board[c][d]:
			  piece_two = state.board_value((c,d))
			  flag2=1
		  if state.board[e][f]:
			  piece_three = state.board_value((e,f))
			  flag3=1
		  #if the board is completely empty
		  if flag1==flag2==flag3==0:
			  #print "Yeazza!! for ", three
			  continue
		  #if the board has only piece
		  if flag1+flag2+flag3==1:
			  #checking if i am first player:
			  if mine==0:
				  if flag1==1:
					  #check if its my piece
					  if piece_one.player==mine:
						  #check if its a large piece
						  if piece_one.size==2:
							  value[mine]-=1
							  continue
						  #check if its a medium piece
						  elif piece_one.size==1:
							  value[mine]+=1
							  continue
						  #its a small piece
						  else:
							  value[mine]+=3
							  continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_one.size==2:
							  if len(state.board[a][b])>1:
								  concealed_piece = state.board[a][b][-2]
								  if concealed_piece.player==mine:
									  value[mine]-=2
							  value[mine]-=3
							  continue
						  #check if its a medium piece
						  elif piece_one.size==1:
							  value[mine]-=2
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
				  elif flag2==1:
					  #check if its my piece
					  if piece_two.player == mine:
						  #check if its a large piece
						  if piece_two.size==2:
							  value[mine]-=1
							  continue
						  #check if its a medium piece
						  elif piece_two.size==1:
							  value[mine]+=1
							  continue
						  else:
							  value[mine]+=3
							  continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_two.size==2:
							  if len(state.board[a][b])>1:
								  concealed_piece = state.board[c][d][-2]
								  if concealed_piece.player==mine:
									  value[mine]-=2
							  value[mine]-=3
							  continue
						  #check if its a medium piece
						  elif piece_two.size==1:
							  value[mine]-=2
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
				  elif flag3==1:
					  #check if its my piece
					  if piece_three.player==mine:
						 #check if its a large piece
						 if piece_three.size==2:
							 value[mine]-=1
							 continue
						 #check if its a medium piece
						 elif piece_three.size==1:
							 value[mine]+=1
							 continue
						 #its a small piece
						 else:
							 value[mine]+=3
							 continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_three.size==2:
							  if len(state.board[a][b])>1:
								  concealed_piece = state.board[e][f][-2]
								  if concealed_piece.player==mine:
									  value[mine]-=2
							  value[mine]-=3
							  continue
						  #check if its a medium piece
						  if piece_three.size==1:
							  value[mine]-=2
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
			  #check if i am second player
			  if mine==1:
				  if flag1==1:
					  #check if its my piece
					  if piece_one.player ==  mine:
						  #check if its a large piece
						  if piece_one.size==2:
							  value[mine]+=3
							  continue
						  #check if its a medium piece
						  elif piece_one.size==1:
							  value[mine]+=1
							  continue
						  #its a small piece
						  else:
							  value[mine]+=1
							  continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_one.size==2:
							  value[mine]-=2
							  continue
						  #check if its a medium piece
						  elif piece_one.size==1:
							  value[mine]-=1
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
				  elif flag2==1:
					  #check if its my piece
					  if piece_two.player==mine:
						  #check if its a large piece
						  if piece_two.size==2:
							  value[mine]+=3
							  continue
						  #check if its a medium piece
						  elif piece_two.size==1:
							  value[mine]+=1
							  continue
						  #its a small piece
						  else:
							  value[mine]+=1
							  continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_two.size==2:
							  value[mine]-=2
							  continue
						  #check if its a medium piece
						  if piece_two.size==2:
							  value[mine]-=1
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
				  elif flag3==1:
					  #check if its my piece
					  if piece_three.player ==  mine:
						  #check if its a large piece
						  if piece_three.size == 2:
							  value[mine]+=3
							  continue
						  #check if its a medium piece
						  elif piece_three.size == 1:
							  value[mine]+=1
							  continue
						  #its a small piece
						  else:
							  value[mine]+=1
							  continue
					  #not my piece
					  else:
						  #check if its a large piece
						  if piece_three.size==2:
							  value[mine]-=2
							  continue
						  #check if its a medium piece
						  elif piece_three.size==1:
							  value[mine]-=1
							  continue
						  #its a small piece
						  else:
							  value[mine]-=1
							  continue
						  
						  
		  #if the board has 2 pieces
		  #if two consecutive pieces of the same player are found, some penalty must be given to the 
		  if flag1+flag2+flag3==2:
			  if flag1==1 and flag2==1:
				  if piece_one.player==piece_two.player and mine==piece_one.player:
					  if piece_one.size==2:
						  if len(state.board[a][b])<=1:
							  value[mine]-=2
					  if piece_two.size==2:
						  if len(state.board[c][d])<=1:
							  value[mine]-=2
					  t = (piece_one.player + 1)%2
					  value[t]-=2
					  #print " Very favorable state for player ",piece_one.player
					  value[piece_one.player]+=3
					  continue
				  elif piece_one.player==piece_two.player and mine!=piece_one.player:
					  value[mine]-=5
					  continue
				  else:
					  if piece_one.size==2 and piece_two.size==2:
						  if mine==piece_one.player:
							  if len(state.board[a][b])>2:
								  value[piece_one.player]+=3
							  value[piece_one.player]+=1
							  value[piece_two.player]-=1
							  continue
						  else:
							  if len(state.board[c][d])>2:
								  value[piece_two.player]+=3
							  value[piece_two.player]+=1
							  value[piece_one.player]-=1
						  	  continue
					  if (piece_one.size==2 and piece_two.size!=2) or (piece_one.size!=2 and piece_two.size==2):
						  if piece_one.size==2 and mine==piece_one.player:
							  value[piece_one.player]+=2
							  value[piece_two.player]-=1
							  continue
						  if piece_one.size==2 and mine!=piece_one.player:
							  value[piece_one.player]-=2
							  value[piece_two.player]+=1
							  continue
						  if piece_two.size==2 and mine==piece_two.player:
							  value[piece_two.player]+=2
							  value[piece_one.player]-=1
							  continue
						  if piece_two.size==2 and mine!=piece_two.player:
							  value[piece_two.player]-=2
							  value[piece_one.player]+=1
							  continue
						  
							  
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_one.size==1 and piece_two.size==1:
						  #check if player one has any large pieces left
						  if piece_one.player==mine:
							  value[piece_one.player]-=2
							  value[piece_two.player]+=1
							  continue
						  if piece_two.player==mine:
							  value[piece_two.player]-=2
							  value[piece_one.player]+=1
							  continue
					  #check if both pieces are S
					  if piece_one.size==0 and piece_two.size==0:
						  if total_avail[(piece_one.player+1)%2][1]==0 and total_avail[(piece_one.player+1)%2][2]==0:
							  t = (piece_one.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_two.player+1)%2][1]==0 and total_avail[(piece_two.player+1)%2][2]==0:
							  k = (piece_two.player + 1)%2
							  value[k]-=1
						  continue
					  # one piece is S and the other is M
					  continue
			  if flag2==1 and flag3==1:
				  if piece_two.player==piece_three.player and piece_two.player==mine:
					  if piece_two.size==2:
						  if len(state.board[c][d])<=1:
							  value[mine]-=2
					  if piece_three.size==2:
						  if len(state.board[e][f])<=1:
							  value[mine]-=2
					  t = (piece_two.player + 1)%2
					  value[t]-=2
					  #print "State very favorable for player ",piece_two.player
					  value[piece_two.player]+=3
					  continue
				  elif piece_two.player==piece_three.player and piece_two.player!=mine:
					  value[mine]-=5
					  continue
				  else:
					  if piece_two.size==2 and piece_three.size==2:
						  if mine==piece_two.player:
							  if len(state.board[c][d])>2:
								  value[piece_two.player]+=3
							  value[piece_two.player]+=1
							  value[piece_three.player]-=1
							  continue
						  else:
							  if len(state.board[e][f])>2:
								  value[piece_three.player]+=3
							  value[piece_three.player]+=1
							  value[piece_two.player]-=1
							  continue
					  if (piece_two.size==2 and piece_three.size!=2) or (piece_two.size!=2 and piece_three.size==2):
						  if piece_two.size==2 and piece_two.player==mine:
							 value[piece_two.player]+=2
							 value[piece_three.player]-=1
							 continue
						  if piece_two.size==2 and piece_two.player!=mine:
							 value[piece_two.player]-=2
							 value[piece_three.player]+=1
							 continue
						  if piece_three.size==2 and piece_three.player == mine:
							 value[piece_three.player]+=2
							 value[piece_two.player]-=1
							 continue
						  if piece_three.size==2 and piece_three.player != mine:
							 value[piece_three.player]-=2
							 value[piece_two.player]+=1
							 continue
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_two.size==1 and piece_three.size==1:
						  #check if player one has any large pieces left
						  if piece_two.player==mine:
							  value[piece_two.player]-=2
							  value[piece_three.player]+=1
							  continue
						  if piece_three.player ==  mine:
							  value[piece_three.player]-=2
							  value[piece_two.player]+=1
							  continue
						  #check if both pieces are S
					  if piece_two.size==0 and piece_three.size==0:
						  if total_avail[(piece_two.player+1)%2][1]==0 and total_avail[(piece_two.player+1)%2][2]==0:
							  t = (piece_two.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_three.player+1)%2][1]==0 and total_avail[(piece_three.player+1)%2][2]==0:
							  k = (piece_three.player + 1)%2
							  value[k]-=1
						  continue
					  # one piece is S and the other is M
					  continue
			  if flag1==1 and flag3==1:
				  if piece_one.player==piece_three.player and piece_one.player==mine:
					  if piece_one.size==2:
						  if len(state.board[a][b])<=1:
							  value[mine]-=2
					  if piece_three.size==2:
						  if len(state.board[e][f])<=1:
							  value[mine]-=2
					  t  = (piece_one.player + 1)%2
					  value[t]-=2
					  #print "State very favorable for player ",piece_one.player
					  value[piece_one.player]+=3
					  continue
				  elif piece_one.player==piece_three.player and piece_one.player!=mine:
					  value[mine]-=5
					  continue
				  else:
					  if piece_one.size==2 and piece_three.size==2:
						  if mine==piece_one.player:
							  if len(state.board[a][b])>2:
								  value[piece_one.player]+=3
							  value[piece_one.player]+=1
							  value[piece_three.player]-=1
							  continue
						  else:
							  if len(state.board[e][f])>2:
								  value[piece_three.player]+=3
							  value[piece_three.player]+=1
							  value[piece_one.player]-=1
							  continue
					  if (piece_one.size==2 and piece_three.size!=2) or (piece_one.size!=2 and piece_three.size==2):
						  if piece_one.size==2 and piece_one.player == mine:
							  value[piece_one.player]+=2
							  value[piece_three.player]-=1
							  continue
						  if piece_one.size==2 and piece_one.player != mine:
							 value[piece_one.player]-=2
							 value[piece_three.player]+=1
							 continue
						  if piece_three.size==2 and piece_three.player == mine:
							 value[piece_three.player]+=2
							 value[piece_one.player]-=1
							 continue
						  if piece_three.size==2 and piece_three.player != mine:
							 value[piece_three.player]-=2
							 value[piece_one.player]+=1
							 continue
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_one.size==1 and piece_three.size==1:
						  #check if player one has any large pieces left
						  if piece_one.player == mine:
							  value[piece_one.player]-=2
							  value[piece_three.player]+=1
							  continue
						  if piece_three.player == mine:
							  value[piece_three.player]-=2
							  value[piece_one.player]+=1
							  continue
					  #check if both pieces are S
					  if piece_one.size==0 and piece_three.size==0:
						  if total_avail[(piece_one.player+1)%2][1]==0 and total_avail[(piece_one.player+1)%2][2]==0:
							  t = (piece_one.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_three.player+1)%2][1]==0 and total_avail[(piece_three.player+1)%2][2]==0:
							  k = (piece_three.player + 1)%2
							  value[k]-=1
						  continue
					  # one piece is S and the other is M
					  continue
		  #three pieces in a row.
		  if flag1 + flag2 + flag3 ==3:
			  #if all three are mine
			  if piece_one.player==piece_two.player==piece_three.player==mine:
				  value[mine]+=10
				  continue
			  #check if all are his
			  if piece_one.player!=mine and piece_two.player!=mine and piece_three.player!=mine:
				  value[mine]-=10
				  value[piece_one.player]+=10
				  continue
			  #2 are yours 1 is his..or the other way round
			  elif piece_one.player!=mine and piece_two.player!=mine and piece_three.player==mine:
				  if piece_three.size==2:
					  value[mine]+=10
					  value[piece_one.player]-=1
					  continue
				  elif piece_three.size==1:
					  if piece_one.size==2 and piece_two.size==2:
						  value[mine]+=12
					  else:
						  value[mine]+=3
					  value[piece_one.player]-=1
					  continue
				  else:
					  value[mine]+=1
					  value[piece_one.player]-=1
					  continue
			  elif piece_one.player!=mine and piece_two.player==mine and piece_three.player!=mine:
				  if piece_two.size==2:
					  value[mine]+=10
					  value[piece_one.player]-=1
					  continue
				  elif piece_two.size==1:
					  if piece_one.size==2 and piece_three.size==2:
						  value[mine]+=12
					  else:
						  value[mine]+=3
					  value[piece_one.player]-=1
					  continue
				  else:
					  value[mine]+=1
					  value[piece_one.player]-=1
					  continue
			  elif piece_one.player==mine and piece_two.player!=mine and piece_three.player!=mine:
				  if piece_one.size==2:
					  value[mine]+=10
					  value[piece_two.player]-=1
					  continue
				  elif piece_one.size==1:
					  if piece_two.size==2 and piece_three.size==2:
						  value[mine]+=12
					  else:
						  value[mine]+=3
					  value[piece_two.player]-=1
					  continue
				  else:
					  value[mine]+=1
					  value[piece_two.player]-=1
					  continue
				  
	  
	  return value[0]-value[1]
	  
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
			#print " Evaluate for player: ",state.get_next_player()
			return (self.evaluate(state), None)
		
		# if no termination, return None
		return None
			
	def minimax_search(self, state, h):
	# Get player IDs
		players = state.get_players()
		
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
		values = [self.minimax_search(s.state, h-1) for s in successors]
		# We're not interested in the moves made, just the minimax values
		values = [x[0] for x in values]
		# Look for the best among the returned values
		# Max if we're player 1
		# Min if we're player 2
		if state.get_next_player() == players[0]:
			max_idx = max(enumerate(values), key=lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key=lambda x: x[1])[0]
		# Return the minimax value and corresponding move
		return (values[max_idx], successors[max_idx].move)
	
	
	# A helper function for alpha_beta_move().  See minimax_search().
	#
	# a,b are alpha, beta values.	
	def minimax_move(self, state, visited):
		# Adjust our ply horizon to the expansion count,
		# based on a maximum branching factor of 8.
		# NB: This may not be the right formula!
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (2.0 / 8.0)))
		
		print "Player",state.get_next_player(),"search depth",h, exp," This is my player!!!!"
		time.sleep(2)
		return self.minimax_search(state,h)[1]
	def alpha_beta_search(self, state, h, a, b):
		# Get player IDs
		players = state.get_players()
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
			s_val = self.alpha_beta_search(s.state, h-1, a, b)
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
			
	def alpha_beta_move(self, state, visited):
		# Adjust our ply horizon to the expansion count,
		# based on an average branching factor of 4.
		# NB: This may not be the right formula!
		exp = state.expansions_count()
		h = int(math.floor(float(exp) ** (1.0 / 4.0)))
		print "Player",state.get_next_player(),"search depth",h
		return self.alpha_beta_search(state, h, -sys.maxint-1, sys.maxint)[1]
		
	def tournament_move(self, state, visited):
		pass
		
		
def make_player(playerID):
	return GobbletPlayer(playerID)
