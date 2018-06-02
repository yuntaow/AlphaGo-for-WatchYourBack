from pprint import pprint
"""
Board class for the game WatchYourBack.

Author: yuntao wang 
Date: 15, 5, 2018.
"""

class Board():
	RIGHT = [0,1]
	LEFT = [0,-1]
	TOP = [-1,0]
	DOWN = [1,0]
	DOWNLEFT = [1,-1]
	DOWNRIGHT = [1,1]
	TOPRIGHT = [-1,1]
	TOPLEFT = [-1,-1]

	player1 = 1
	player2 = -1
	WALL = 2
	in_WALL = -2
	SPACE = 0

	def __init__(self, size = 8):
		self.size = size
		self.pieces = [[self.SPACE]*self.size for i in range(self.size)]
		# initial corners are "X"
		self.pieces[0][0] = self.WALL
		self.pieces[-1][-1] = self.WALL
		self.pieces[-1][0] = self.WALL
		self.pieces[0][-1] = self.WALL
		self.init()

	def init(self):
		self.piece = {self.player1 : len(self.get_player_position(self.player1)),
		self.player2 : len(self.get_player_position(self.player2))
		}


	def __str__(self):
		return str(self.pieces)
	def __getitem__(self, index):
		return self.pieces[index]
	# available moves for phase 1
	def get_legal_moves(self, side):
		return [[i,j] for i in range(self.size) for j in range(self.size) if self.pieces[i][j] == self.SPACE] 

	def get_player_position(self, side):
		return [[a,b] for a in range(self.size) for b in range(self.size) if self[a][b] == side]

	# creates for consistebce
	def has_legal_moves(self, side):
		return True

	def addition_listwise(self, l1, l2):
		return [sum(x) for x in zip(l1, l2)]

    # makes change to the board
	def execute_move(self, move, side):
		if (not self[move[0]][move[1]] == self.SPACE):
			# print("error")
			# pprint(self.pieces)
			# pprint(move)
			exit()
		self[move[0]][move[1]] = side
		self.refresh_board(side)
		self.refresh_board(self.get_other_side(side))

	def _within_board(self, x, y):
		for coord in [y, x]:
			if coord < 0 or coord >= self.size:
				return False
		return True

	def refresh_board(self, side):
		side_pieces = self.get_player_position(side)
		for piece in side_pieces:
			for direction in [self.RIGHT, self.LEFT, self.TOP, self.DOWN]:
				[row,height] = self.addition_listwise(piece, direction)
				if self._within_board(row, height) and self[row][height] == self.get_other_side(side):	
					[row2,height2] = self.addition_listwise([row, height], direction)
					if self._within_board(row2, height2) and (self[row2][height2] == side or self[row2][height2] == self.WALL or self[row2][height2] == self.in_WALL):
						self[row][height] = self.SPACE


	def get_other_side(self, side):
		return self.player2 if side == self.player1 else self.player1

	def is_win(self, side):
		diff = self.countDiff(side)
		if diff > 0:
			return 1
		elif diff == 0:
			return 0
		else:
			return -1

	def countDiff(self, side):
		me = sum([1 for i in range((self.size)) for j in range(self.size) if self[i][j] == side ])
		oppo = sum([1 for i in range((self.size)) for j in range(self.size)if self[i][j] == self.get_other_side(side)])
		return me-oppo

	def read_board(self, board, piece_representaiton = "NOT PROVIDED"):
		if piece_representaiton == "NOT PROVIDED":
			self.pieces = list(board)
			self.init()
		self.pieces = [[piece_representaiton[j]for j in board[i]] for i in range(self.size)]

# testing
if __name__ == '__main__':
	b = Board(size = 8)

	pprint(b.board)

	test_board = [
	['X', '@', '-', '-', '-', '-', '-', 'X'],
	['@', '-', '@', 'X', 'O', '-', '-', '-'],
	['-', '@', '-', 'O', '-', '-', '-', '-'],
	['-', '@', '-', '@', '-', '-', '-', '-'],
	['-', 'O', '-', '-', 'O', '-', '-', '-'],
	['-', '-', '-', '-', '-', '-', '-', '-'],
	['-', '-', '-', 'O', '-', '-', '-', '-'],
	['X', '-', '-', '-', '-', '-', '-', 'X']
	]

	b.read_board(test_board, {"X":2, "O":1,"@":-1,"-":0})
	print(b.get_player_position(1))
	# print("test_board")

	# pprint(b.board)

	# print("player1 moves: ")
	# print(b.get_legal_moves(b.player1))
	# print("player2 moves: ")
	# print(b.get_legal_moves(b.player2))

	# pprint(b.get_player_position(b.player1))

	# pprint(b.has_legal_moves(b.player1))

	# pprint(b.get_other_side(b.player2))

	# pprint(b.is_win(b.player1))

	# b.execute_move([1,1], b.player1)
	# pprint(b.board)
	# print(b.piece)

