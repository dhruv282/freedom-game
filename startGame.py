#!/usr/bin/python3
import sys
from random import randrange
from math import inf
import copy


BLANK = '-'
WHITE_STONE = u'\u25cf'
BLACK_STONE = u'\u25cb'

'''
Cell object for each cell in the board

Attributes:
	- num: cell number
	- val: value in the cell (stone or blank)
	- position: tuple of x,y position of cell on the board
	- adjacent: list of cell numbers of adjacent cells
'''
class cell():
	def __init__(self, num=0, val=BLANK, position=(0,0), adj=[]):
		self.num = num
		self.val = val
		self.position = position
		self.adjacent = adj
		self.counted = False

'''
Board object for game board that contains all cells

Attributes:
	- row: number of rows in board
	- col: number of columns in board
	- moves: list of possible moves based on last cell played
	- cells: list of cell objects
'''
class board():
	def __init__(self, m, n):
		self.row = m
		self.col = n
		self.moves = []
		self.cells = []

		# evaluating adjacent cells for each cell in the board
		num = 0
		for x in range(self.row):
			for y in range(self.col):
				adj = []
				if (num % self.col) != 0:
					# left
					adj.append(num - 1)

					# top left
					if num >= self.col:
						adj.append(num - (self.col+1))

					# bottom left
					if num + (self.col-1) < self.row*self.col:
						adj.append(num + (self.col-1))

				if ((num+1) % self.col) != 0:
					# right
					adj.append(num + 1)

					# top right
					if num >= self.col:
						adj.append(num - (self.col-1))

					# bottom right
					if num + (self.col+1) < self.row*self.col:
						adj.append(num + (self.col+1))

				# top
				if (num - self.col) >= 0:
					adj.append(num-self.col)

				# bottom
				if (num + self.col) < self.row*self.col:
					adj.append(num + self.col)

				self.cells.append(cell(num=num, position=(x,y), adj=adj))
				num += 1

	'''
	Prints game board
	- Index of cell in moves list printed if cell exists in the list
	- Cells in the moves list are blank
	'''
	def print(self):
		print('***********************************************')
		for i in range(len(self.cells)):
			if i in self.moves:
				print(' {:>3} '.format(self.moves.index(i)), end='')
			else:
				print(' {:>3} '.format(self.cells[i].val), end='')
			if (i+1) % self.col == 0:
				print('\n')
		print('***********************************************')

	'''
	Gets moves for the given cell
	- Possible moves are adjacent cells that are still blank
	- If no adjacent cells are blank,
	  then all other blank cells on the board are considered to be possible moves
	- If move is last move, then a skip option is added as a possible move

	Parameters:
		- cellNo: number of cell to get moves for

	Return:
		- returns if last move
	'''
	def getMoves(self, cellNo):
		self.moves = []
		for c in self.cells[cellNo].adjacent:
			if self.cells[c].val == BLANK:
				self.moves.append(c)
		
		if len(self.moves) == 0:
			for c in range(len(self.cells)):
				if self.cells[c].val == BLANK:
					self.moves.append(c)

		if self.checkIfLastMove():
			self.moves.append('s')
			return True
		return False

	'''
	Checks if last move is left on the board
	- This is done by ensuring that exactly 1 blank is on the board
	'''
	def checkIfLastMove(self):
		if len(self.moves) != 1:
			return False
		count = 0
		for c in self.cells:
			if c.val == BLANK:
				count+=1
			if count > 1:
				return False
		return True

'''
Class that contains important game functions such as:
	- game execution
	- score updating
	- move selection for computer 

Attributes:
	- gameBoard: contains a board object initialized with m,n parameters
	- humanScore: records human player score
	- computerScore: records computer score
	- hStone: stone used by human (first player gets white stone)
	- cStone: stone used by computer (first player gets white stone)
'''
class game():
	def __init__(self, m=0, n=0):
		self.gameBoard = board(m,n)
		self.humanScore = 0
		self.computerScore = 0

	'''
	Selects first player and handles gameplay
	- Game keeps running until all cells are filled or last player chooses to skip
	- Scores are updates after a move is made by either players
	- If Computer is the first player, a random cell is played as its first move 
	'''
	def startGame(self):
		# randomly picking first player
		firstPlayer = randrange(50)

		if firstPlayer <= 25:
			curPlayer = 'Computer'
			self.cStone = WHITE_STONE
			self.hStone = BLACK_STONE
		else:
			curPlayer = 'Human'
			self.hStone = WHITE_STONE
			self.cStone = BLACK_STONE

		# initializing last cell and round number
		lastCell = -1
		roundNum = 1

		# loop to carry on game execution
		while not self.goal():
			print('\n\n***********************************************')
			print('ROUND '+str(roundNum))
			print('\nSCORE')
			print('Computer ('+self.cStone+'): '+str(self.computerScore))
			print('Human ('+self.hStone+'): '+str(self.humanScore))
			print('\nCURRENT PLAYER: '+curPlayer)
			
			# getting moves based on value of lastCell
			if lastCell < 0:
				self.gameBoard.moves = [i for i in range(0,len(self.gameBoard.cells))]
				lastMove = False
			else:
				lastMove = self.gameBoard.getMoves(lastCell)
			
			#printing board
			self.gameBoard.print()
			
			# Determine player
			if curPlayer == 'Computer':
				if lastCell < 0:
					# pick first move randomly
					move = randrange(len(self.gameBoard.moves))
				else:
					# use max depth of 8
					depth = min(len(self.gameBoard.moves), 8)

					# evaluate best move
					_, move = self.minimaxWithAlphaBeta(self, depth, 'Computer', -inf, inf)
				print('Computer played move: '+str(self.gameBoard.moves.index(move)))
				
				# accounting for skip option provided for last move
				if move == 's':
					break
			else:
				# checking if last move
				if lastMove:

					# prompting user to make a move
					move = input('Enter move to make (0 or s to skip): ')
					
					# accounting for skip option provided for last move
					if move == 's':
						break
					else:
						move = int(move)
				else:
					# prompting user to make a move
					move = input('Enter move to make (0-'+str(len(self.gameBoard.moves)-1)+'): ')
					move = int(move)

				# validating user input
				while (move < 0 or move >= len(self.gameBoard.moves)):
					print('Invalid move!')
					move = input('Enter move to make (0-'+str(len(self.gameBoard.moves)-1)+'): ')
					move = int(move)
				move = self.gameBoard.moves[move]

			# making move and updating variables
			if curPlayer == 'Computer':
				self.makeMove(move, self.cStone)
				curPlayer = 'Human'
			else:
				self.makeMove(move, self.hStone)
				curPlayer = 'Computer'
			lastCell = move
			self.updateScore()
			roundNum += 1

		# determine winner
		if(self.computerScore > self.humanScore):
			print('\n***Computer Wins!***')
		elif(self.computerScore < self.humanScore):
			print('\n***Human Wins!***')
		else:
			print('\n***Tie***')

	'''
	Checks if all cells are filled
	'''
	def goal(self):
		for c in self.gameBoard.cells:
			if c.val == BLANK:
				return False
		return True

	'''
	Places a stone on the given cell

	Parameters:
		- cellNo: number of cell to place a stone on
		- stone: type of stone to place on cell
	'''
	def makeMove(self, cellNo, stone):
		if cellNo != 's':
			self.gameBoard.cells[cellNo].val = stone

	'''
	Calculates evaluation of a board based on stones placed by each player
	- lines of 3 stones and 2 stones are counted are given weight of
	  10 and 1 respectively to incentivize the computer to make such combinations
	- Difference of the computer and human scores is returned
	'''
	def evaluation(self):
		self.updateScore()
		self.updateScore(3, 1/10, False, False)
		self.updateScore(2, 1/100, False, False)
		return self.computerScore - self.humanScore

	'''
	Recursive minimax algorithm with alpha beta pruning to get ideal move

	Paramters:
		- state: game object showing current state
		- depth: depth of tree to explore
		- maximizingPlayer: current player ('Computer' when function first called)
		- alpha: value of alpha (-infinity when function first called)
		- beta: value of beta (infinity when function first called)
	
	Return:
		- Returns cell number of best move
	'''
	def minimaxWithAlphaBeta(self, state, depth, maximizingPlayer, alpha, beta):
		# checking if depth = 0 or no blanks left
		if depth == 0 or state.goal():
			return state.evaluation(), -1

		if maximizingPlayer == 'Computer':
			maxEval = -inf
			maxMove = -1
			for move in state.gameBoard.moves:
				temp = copy.deepcopy(state)
				temp.makeMove(move, state.cStone)
				if move != 's':
					temp.gameBoard.getMoves(move)
				else:
					temp.gameBoard.moves = []
				evaluation, _ = temp.minimaxWithAlphaBeta(temp, depth-1, 'Human', alpha, beta)
				
				# update maxEval and maxMove since better evaluation found
				if maxEval < evaluation:
					maxMove = move
					maxEval = evaluation
				
				alpha = max(alpha, maxEval)
				if beta <= alpha:
					break
			return maxEval, maxMove
		else:
			minEval = +inf
			minMove = -1
			for move in state.gameBoard.moves:
				temp = copy.deepcopy(state)
				temp.makeMove(move, state.hStone)
				if move != 's':
					temp.gameBoard.getMoves(move)
				else:
					temp.gameBoard.moves = []
				evaluation, _ = temp.minimaxWithAlphaBeta(temp, depth-1, 'Computer', alpha, beta)
				
				# update minEval and minMove since better evaluation found
				if minEval > evaluation:
					minMove = move
					minEval = evaluation
				beta = min(beta, minEval)
				if beta <= alpha:
					break
			return minEval, minMove

	'''
	Gets score for human and computer players

	Parameters:
		- numStones: combination of stones to detect (default: 4)
		- weight: weight carried by given combination (default: 100)
		- initializeScore: set scores to 0 before evaluation (default: True)
		- combCheck: score combinations with a common stone a point less
	'''
	def updateScore(self, numStones=4, weight=1, initializeScore=True, combCheck=True):
		if initializeScore:
			self.humanScore = 0
			self.computerScore = 0

		for x in self.gameBoard.cells:
			x.counted = False

		# horizontal count
		col = 0
		for i in range(self.gameBoard.row):
			hCount = 0
			cCount = 0
			hC = []
			cC = []
			for j in range(col, col+self.gameBoard.col):
				c = self.gameBoard.cells[col]
				col += 1
				hCount, cCount, hC, cC = self.getCounts(c, hCount, cCount, hC, cC, numStones, weight, combCheck)
			
			if hCount == numStones:
				if combCheck:
					self.humanScore += len(hC)
				else:
					self.humanScore += weight
			elif combCheck:
				for x in hC:
					x.counted = False

			if cCount == numStones:
				if combCheck:
					self.computerScore += len(cC)
				else:
					self.computerScore += weight
			elif combCheck:
				for x in cC:
					x.counted = False

		
		# vertical count
		for i in range(self.gameBoard.col):
			stopPoint = (self.gameBoard.col * self.gameBoard.row) - (self.gameBoard.col - i)
			stopPoint += 1
			hCount = 0
			cCount = 0
			hC = []
			cC = []
			for j in range(i, stopPoint, self.gameBoard.col):
				c = self.gameBoard.cells[j]
				hCount, cCount, hC, cC = self.getCounts(c, hCount, cCount, hC, cC, numStones, weight, combCheck)

			if hCount == numStones:
				if combCheck:
					self.humanScore += len(hC)
				else:
					self.humanScore += weight
			elif combCheck:
				for x in hC:
					x.counted = False

			if cCount == numStones:
				if combCheck:
					self.computerScore += len(cC)
				else:
					self.computerScore += weight
			elif combCheck:
				for x in cC:
					x.counted = False
		

		# diagonal to the right
		exploredCells = []
		for i in range(len(self.gameBoard.cells)):
			hCount = 0
			cCount = 0
			hC = []
			cC = []
			n = i
			while (n+1) % self.gameBoard.col != 0:
				n+=1
				if n + self.gameBoard.col >= self.gameBoard.col*self.gameBoard.row:
					n-=1
					break
				n+=self.gameBoard.col
			stopPoint = n
			for j in range(i, stopPoint+1, 1+self.gameBoard.col):
				if j not in exploredCells:
					exploredCells.append(j)
					c = self.gameBoard.cells[j]
					hCount, cCount, hC, cC = self.getCounts(c, hCount, cCount, hC, cC, numStones, weight, combCheck)

			if hCount == numStones:
				if combCheck:
					self.humanScore += len(hC)
				else:
					self.humanScore += weight
			elif combCheck:
				for x in hC:
					x.counted = False

			if cCount == numStones:
				if combCheck:
					self.computerScore += len(cC)
				else:
					self.computerScore += weight
			elif combCheck:
				for x in cC:
					x.counted = False

		# diagonal to the left
		exploredCells = []
		for i in range(len(self.gameBoard.cells)):
			hCount = 0
			cCount = 0
			hC = []
			cC = []
			n = i
			while n % self.gameBoard.col != 0:
				n-=1
				if n + self.gameBoard.col >= self.gameBoard.col*self.gameBoard.row:
					n+=1
					break
				n+=self.gameBoard.col
			stopPoint = n
			for j in range(i, stopPoint+1, self.gameBoard.col-1):
				if j not in exploredCells:
					exploredCells.append(j)
					c = self.gameBoard.cells[j]
					hCount, cCount, hC, cC = self.getCounts(c, hCount, cCount, hC, cC, numStones, weight, combCheck)

			if hCount == numStones:
				if combCheck:
					self.humanScore += len(hC)
				else:
					self.humanScore += weight
			elif combCheck:
				for x in hC:
					x.counted = False

			if cCount == numStones:
				if combCheck:
					self.computerScore += len(cC)
				else:
					self.computerScore += weight
			elif combCheck:
				for x in cC:
					x.counted = False

		for x in self.gameBoard.cells:
			x.counted = False

	'''
	Detect a combination of a certain number in the given sequences of stones

	Parameters:
		- c: value of cell
		- hCount: records number of stones used by human player next to each other
		- cCount: records number of stones used by computer player next to each other
		- numStones: combination of stones to detect
		- weight: weight that the combination of stone carry
	'''
	def getCounts(self, c, hCount, cCount, hC, cC, numStones, weight, combCheck):
		# human
		if c.val == self.hStone:
			hCount += 1
			if combCheck and not c.counted:
				hC.append(c)
				c.counted = True
		elif c.val != self.hStone:
			if hCount == numStones:
				if combCheck:
					self.humanScore += len(hC)
				else:
					self.humanScore += weight
			elif combCheck:
				for x in hC:
					x.counted = False
			hC = []
			hCount = 0

		# computer
		if c.val == self.cStone:
			cCount += 1
			if combCheck and not c.counted:
				cC.append(c)
				c.counted = True
		elif c.val != self.cStone:
			if cCount == numStones:
				if combCheck:
					self.computerScore += len(cC)
				else:
					self.computerScore += weight
			elif combCheck:
				for x in cC:
					x.counted = False
			cC = []
			cCount = 0
		
		return hCount, cCount, hC, cC

def main():
	if len(sys.argv) != 3:
		print('Usage: '+sys.argv[0]+' m n')
		sys.exit()

	# initialize game
	g = game(int(sys.argv[1]), int(sys.argv[2]))

	# begin game
	try:
		g.startGame()
	except KeyboardInterrupt:
		print('\n\n***Game ended by user***')


if __name__ == "__main__":
	main()