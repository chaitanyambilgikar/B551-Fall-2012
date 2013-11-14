from game_player import *
from gobblet import *


# A human-interactive GobbletPlayer agent.
class GobbletPlayer(GamePlayer):

	# Make a note of our player ID
	# see comments on GamePlayer for more details
	def __init__(self, player_id):
		GamePlayer.__init__(self, player_id)
	
	# This agent doesn't evaluate states, so just return 0
	#
	# "state" is a GobbletState object
	def evaluate(self, state):
	  #first find out how many pieces of each size of each player are on the board and on the stack
	  print "It is ",state.get_next_player()," 's turn.'"
	  player_list = state.get_players()
	  total_avail = [[0 for i in range(3)]for i in range(len(player_list))]
	  on_board = [[0 for i in range(3)]for i in range(len(player_list))]
	  for i in range(3):
	    for j in range(3):
	      if state.board[i][j]:
		temp_player = state.board_value((i,j))
		on_board[temp_player.player][temp_player.size] +=1
		total_avail[temp_player.player][temp_player.size]+=1
		#print temp_player.player, temp_player.size
	  print "Pieces on the board are: ",on_board
	  on_stack =  [[0 for i in range(3)]for i in range(len(player_list))]
	  for i in range(len(player_list)):
	    for j in range(3):
	      on_stack[i][j] = state.pieces_available(i,j)
	      total_avail[i][j] = total_avail[i][j] + on_stack[i][j]
	  print "Pieces on the stack (unused) are: ",on_stack
	  
	  print "Total number of pieces are: ",total_avail
	
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
			  if flag1==1:
				  if piece_one.size==2:
					  t = (piece_one.player + 1)%2
					  #print " Did flag==1 for ", t
					  value[t]-=1
					  continue
				  elif piece_one.size==0:
					  if total_avail[(piece_one.player+1)%2][1]==0 and total_avail[(piece_one.player +1)%2][2]==0:
						  t = (piece_one.player + 1)%2
					  	  value[t]-=1
					  	  continue
				  elif piece_one.size==1:
					  if total_avail[(piece_one.player + 1)%2][2]==0:
						  t = (piece_one.player + 1)%2
					  	  value[t]-=1
					  	  continue
						 
				  
			  if flag2==1:
				  if piece_two.size==2:
					  t = (piece_two.player + 1)%2
					  #print " Did flag==1 for ", t
					  value[t]-=1
					  continue
				  elif piece_two.size==0:
					  if total_avail[(piece_two.player+1)%2][1]==0 and total_avail[(piece_two.player +1)%2][2]==0:
						  t = (piece_two.player + 1)%2
					  	  value[t]-=1
					  	  continue
				  elif piece_two.size==1:
					  if total_avail[(piece_two.player + 1)%2][2]==0:
						  t = (piece_two.player + 1)%2
					  	  value[t]-=1
					  	  continue
			  if flag3==1:
				  if piece_three.size==2:
					  t = (piece_three.player + 1)%2
					  #print " Did flag==1 for ", t
					  value[t]-=1
					  continue
				  elif piece_three.size==0:
					  if total_avail[(piece_three.player+1)%2][1]==0 and total_avail[(piece_three.player +1)%2][2]==0:
						  t = (piece_three.player + 1)%2
					  	  value[t]-=1
					  	  continue
				  elif piece_three.size==1:
					  if total_avail[(piece_three.player + 1)%2][2]==0:
						  t = (piece_three.player + 1)%2
					  	  value[t]-=1
					  	  continue
		  #if the board has 2 pieces
		  #if two consecutive pieces of the same player are found, some penalty must be given to the 
		  if flag1+flag2+flag3==2:
			  if flag1==1 and flag2==1:
				  if piece_one.player==piece_two.player:
					  t = (piece_one.player + 1)%2
					  value[t]-=5
					  if piece_one.player==state.get_next_player():
						  print " Very favorable state for player ",piece_one.player
						  value[piece_one.player]+=10
					  continue
				  else:
					  if piece_one.size==2 and piece_two.size==2:
						  t = (piece_one.player + 1)%2
						  k = (piece_two.player + 1)%2
						  value[t]-=1
						  value[k]-=1
						  continue
					  if (piece_one.size==2 and piece_two.size!=2) or (piece_one.size!=2 and piece_two.size==2):
						  if piece_one.size==2:
							  t = (piece_one.player + 1)%2
							  value[t]-=1
							  
						  else:
							  t = (piece_two.player + 1)%2
							  value[t]-=1
						  continue
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_one.size==1 and piece_two.size==1:
						  #check if player one has any large pieces left
						  if total_avail[(piece_one.player+1)%2][2]==0:
							  t=(piece_one.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_two.player + 1)%2][2]==0:
							  k=(piece_two.player + 1)%2
							  value[k]-=1
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
				  if piece_two.player==piece_three.player:
					  t = (piece_two.player + 1)%2
					  value[t]-=2
					  if piece_two.player==state.get_next_player():
						  print "State very favorable for player ",piece_two.player
						  value[piece_two.player]+=10
					  continue
				  else:
					  if piece_two.size==2 and piece_three.size==2:
						  t = (piece_two.player + 1)%2
						  k = (piece_three.player + 1)%2
						  value[t]-=1
						  value[k]-=1
						  continue
					  if (piece_two.size==2 and piece_three.size!=2) or (piece_two.size!=2 and piece_three.size==2):
						  if piece_two.size==2:
							  t = (piece_two.player + 1)%2
							  value[t]-=1
							  
						  else:
							  t = (piece_three.player + 1)%2
							  value[t]-=1
						  continue
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_two.size==1 and piece_three.size==1:
						  #check if player one has any large pieces left
						  if total_avail[(piece_two.player+1)%2][2]==0:
							  t=(piece_two.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_three.player + 1)%2][2]==0:
							  k=(piece_three.player + 1)%2
							  value[k]-=1
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
				  if piece_one.player==piece_three.player:
					  t  = (piece_one.player + 1)%2
					  value[t]-=2
					  if piece_one.player==state.get_next_player():
						  print "State very favorable for player ",piece_one.player
						  value[piece_one.player]+=10
					  continue
				  else:
					  if piece_one.size==2 and piece_three.size==2:
						  t = (piece_one.player + 1)%2
						  k = (piece_three.player + 1)%2
						  value[t]-=1
						  value[k]-=1
						  continue
					  if (piece_one.size==2 and piece_three.size!=2) or (piece_one.size!=2 and piece_three.size==2):
						  if piece_one.size==2:
							  t = (piece_one.player + 1)%2
							  value[t]-=1
							  
						  else:
							  t = (piece_three.player + 1)%2
							  value[t]-=1
						  continue
					  #neither of the pieces is L..so now checks if both are medium
					  if piece_one.size==1 and piece_three.size==1:
						  #check if player one has any large pieces left
						  if total_avail[(piece_one.player+1)%2][2]==0:
							  t=(piece_one.player + 1)%2
							  value[t]-=1
						  if total_avail[(piece_three.player + 1)%2][2]==0:
							  k=(piece_three.player + 1)%2
							  value[k]-=1
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
			#if all three belong to the same player then its a win
			if piece_one.player==piece_two.player==piece_three.player:
				k = player_one.player
				t = (player_one.player + 1)%2
				value[t]=0
				value[k]=8
				continue
			#2 pieces of one player and one of the other
			#here you will have to check if the any player has concealed a piece
			
			if (piece_one.player == piece_two.player) or (piece_one.player == piece_three.player) or (piece_two.player == piece_three.player):
				if piece_one.player == piece_two.player:
					if piece_three.size!=2:
						if piece_three.size==0:
							if total_avail[piece_one.player][1]!=0 or total_avail[piece_one.player][2]!=0:
								print "Found 2 pieces of ",piece_one.player," at ", (a,b), (c,d)
								value[piece_one.player]+=10
								continue
						if piece_three.size==1:
							if total_avail[piece_one.player][2]!=0:
								print "Found 2 pieces of ",piece_one.player," at ", (a,b),(c,d)
								value[piece_one.player]+=10
								continue
					#this row is not favorable to piece one
					print " Row ",three," is not favorable for current player!"
					value[piece_one.player]-=1
					continue
				if piece_two.player == piece_three.player:
					if piece_one.size!=2:
						if piece_one.size==0:
							if total_avail[piece_two.player][1]!=0 or total_avail[piece_two.player][2]!=0:
								print "Found 2 pieces of ",piece_two.player," at ", (c,d), (e,f)
								value[piece_two.player]+=10
								continue
							if piece_one.size==1:
								if total_avail[piece_two.player][2]!=0:
									print "Found 2 pieces of ",piece_two.player," at ", (c,d),(e,f)
									value[piece_two.player]+=10
									continue
								#this row is not favorable to piece one
								print " Row ",three," is not favorable for current player!"
								value[piece_two.player]-=1
								continue
				if piece_one.player == piece_three.player:
					if piece_two.size!=2:
						if piece_two.size==0:
							if total_avail[piece_one.player][1]!=0 or total_avail[piece_one.player][2]!=0:
								print "Found 2 pieces of ",piece_one.player," at ", (a,b), (e,f)
								value[piece_one.player]+=10
								continue
							if piece_two.size==1:
								if total_avail[piece_one.player][2]!=0:
									print "Found 2 pieces of ",piece_one.player," at ", (a,b),(e,f)
									value[piece_one.player]+=10
									continue
								#this row is not favorable to piece one
								print " Row ",three," is not favorable for current player!"
								value[piece_one.player]-=1
								continue
	  print "Value of this state is: ",value[0]-value[1]
	  #print "you are player: ",state.get_next_player()
	  return 0
	def minimax_move(self, state, visited):
		# see what the valid moves are so we can check the human's answer
		successors = state.successor_moves()
		successors = [x.get_move() for x in successors]
		sizeNames = ['S','M','L']
		size = None
		self.evaluate(state)
		# Keep looping until the human gives us valid input
		while True:
                        src = raw_input("What square would you like to move to or pick up from (1-9, q to quit)? ")
                        target = None
			if src == 'q':
				# Quit by forfeiting
				return GobbletMove(None, True)
			try:
				src = int(src)
			except:
				print "Please input an integer 0-9, or q to quit. "
				continue
			
			if src >= 1 and src <= 9:
				src -= 1
				src = (src / 3, src % 3)
			else:
				print "Please input an integer 1-9, or q to quit. "
				continue

                        placingNew = False
			if state.board_value(src) == None or state.board_value(src).player != state.get_next_player():
                                placingNew = True
                        else:
                                #existing piece there, do we want to move it or cover it?
                                if state.board_value(src).size < 2:
                                        cover = raw_input("Do you want to cover/move your old piece? (y/n) ")
                                        if cover == 'y':
                                                placingNew=True
                                        elif cover == 'n':
                                                placingNew=False
                                        else:
                                                print "Please answer y/n"
                                                continue
                        if placingNew:
                                #placing a new piece
                                avail = []
                                if state.board_value(src) == None:
                                        avail = [0,1,2]
                                else:
                                        avail = range(state.board_value(src).size+1,3)
                                avail = [s for s in avail if state.pieces_available(state.get_next_player(), s) > 0]
                                if len(avail) == 0:
                                        print "Unable to place a piece at that location"
                                        continue
                                if len(avail) == 1:
                                        size = avail[0]
                                        print "Using piece of size "+str(size)
                                else:
                                        availSizeNames = [sizeNames[s] for s in avail]
                                        size = raw_input("What size piece would you like to use (%s)? "%(",".join(availSizeNames),))
                                        try:
        					size = avail[availSizeNames.index(size.upper())]
                                        except:
        					print "Please input one of (%s)"%(",".join(availSizeNames),)
                				continue
                        		if size not in avail:
                                                print "Please input one of (%s)"%(",".join(availSizeNames),)
                                                continue
                                target = src
                                src = None                                                     
                        else:
                                size = state.board_value(src).size
                                # Ask
                                target = raw_input("What square would you like to move to (1-9)? ")
			
                                # Human may not have input an integer
                                try:
        				target = int(target)
                                except:
        				print "Please input an integer 1-9. "
                			continue
			
                                if target >= 1 and target <= 9:
                                        target -= 1
                                        target = (target / 3, target % 3)
                                else:
        				print "Please input an integer 1-9. "
                                        continue


                        """
			src = raw_input("What square would you like to pick up from (1-9, q to quit, "\
							"0 to place a new piece)? ")
			if src == 'q':
				# Quit by forfeiting
				return GobbletMove(None, True)
			try:
				src = int(src)
			except:
				print "Please input an integer 0-9, or q to quit. "
				continue
			
			if src >= 0 and src <= 9:
				src -= 1
			else:
				print "Please input an integer 0-9, or q to quit. "
				continue
				
			if src >= 0:
				src = (src / 3, src % 3)
				if state.board_value(src) == None or state.board_value(src).player != state.get_next_player():
					print "You do not have a topmost piece at that location. "
					continue
				size = state.board_value(src).size
				valid = False
				for successor in successors:
					if successor.source == src:
						valid = True
						break
				if not valid:
                                        print "That piece is covering a piece that would cause the opponent to win."
			else:
				src = None
				size = raw_input("What size piece would you like to use (0-2)? ")
				try:
					size = int(size)
				except:
					print "Please input an integer 0-2. "
					continue
				if size < 0 or size > 2:
					print "Please input an integer 0-2. "
					continue
				
				if state.pieces_available(state.get_next_player(), size) <= 0:
					print "You do not have any pieces of that size available. "
					continue
		
			# Ask
			target = raw_input("What square would you like to move to (1-9)? ")
			
			# Human may not have input an integer
			try:
				target = int(target)
			except:
				print "Please input an integer 1-9. "
				continue
			
			if target >= 1 and target <= 9:
				target -= 1
				target = (target / 3, target % 3)
			else:
				print "Please input an integer 1-9. "
				continue
			"""
			move = GobbletMove(GobbletMoveDetail(src, target, 
							     GobbletPiece(state.get_next_player(), size)))
						
			# Human may not have input a valid move
			if not state.is_valid_move(move):
				print "That is not a valid move.  Please choose a target square that "\
					"is occupied only by smaller pieces or no pieces. "
				continue
			
			# Return the valid move
			return move
			
def make_player(playerID):
	return GobbletPlayer(playerID)
