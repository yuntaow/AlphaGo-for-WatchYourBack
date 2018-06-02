import sys
sys.path.append('..')
from Game import Game
from watch.WatchGameLogic import Board
import numpy as np
from pprint import pprint
from collections  import deque

"""
Game class for the game WatchYourBack.

Author: yuntao wang

"""

symbol_to_num = {"X":2, "O":1,"@":-1,"-":0}
num_to_symbol = {2:"X", 1:"O", -1:"@", 0:"-"}

player1marker = "O"  #1
player2marker = "@"	 #-1

class WatchGame():

    player1 = 1
    player2 = -1

    def __init__(self, n = 8, maxi = 12):
        self.n = n
        self.turn = 0
        self.maxi_phase1_round = maxi
        self.two_history = deque()
        self.test_turn = 0

    def modified_history(self, move, side):
        if len(self.two_history) >= 2:
            self.two_history.popleft()
            self.two_history.append(move)
        else:
            self.two_history.append(move)

    def increase_turn(self):
        self.turn +=1
        self.test_turn = self.turn

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return np.array(Board(self.n).pieces)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.n,self.n)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        self.test_turn +=1
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        self.modified_history(action, player)

        return (b.pieces, -player)
    

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)

        for x, y in legalMoves:
                if (x*self.n + y) not in self.two_history:
                    valids[self.n*x+y]=1

        return np.array(valids)
        
    def get_sum(self, board):
        c = 0
        for a in board:
            for b in a:
                c += abs(b)
        return c

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        if self.turn >= self.maxi_phase1_round or self.get_sum(board)>=(self.maxi_phase1_round):
            # print(self.turn)
            # print(self.get_sum(board))
            b = Board(self.n)
            b.pieces = np.copy(board)
            result = b.is_win(player)
            if result == 1:
                return 1
            if result == -1:
                return -1
            if result == 0:
                return 1e-4
        else:
            return 0

        

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        new = player*board
        for i in range(self.n):
        	for j in range(self.n):
        		if new[i][j] == -2:
        			new[i][j] = 2
        return new
        

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.

        """
        s=""
        for i in board:
            for ii in i:
                s +=str(ii)
        return s

    def getScore(self, board, side):
    	b = Board(self.n)
    	b.pieces = np.copy(board)
    	return b.countDiff(side)


def display(board):
	n = board.shape[0]
	bo = Board(n)
	bo.read_board(board)

	print("------- Watch Your Back -------")
	p1 = bo.piece[bo.player1]
	p2 = bo.piece[bo.player2]
	print(player1marker, ": ", str(p1), end="   ")
	print(player2marker, ": ", str(p2))
	for i in range(n):
		for j in range(n):
			# print(int(board[i][j]), " " ,end="")
			print(num_to_symbol[int(board[i][j])], " " ,end="")
		print()


if __name__ == '__main__':
    game = WatchGame()

    b = game.getInitBoard()

    # test_board = [['X', '@', '-', '-', '-', '-', '-', 'X'],
    # ['@', '-', '@', 'X', 'O', '-', '-', '-'],
    # ['-', '@', '-', 'O', '-', '-', '-', '-'],
    # ['-', '@', '-', '@', '-', '-', '-', '-'],
    # ['-', 'O', '-', '-', 'O', '-', '-', '-'],
    # ['-', '-', '-', '-', '-', '-', '-', '-'],
    # ['-', '-', '-', 'O', '-', '-', '-', '-'],
    # ['X', '-', '-', '-', '-', '-', '-', 'X']
    # ]

    # board.read_board(test_board, {"X":2, "O":1,"@":-1,"-":0})
    n_b, p = game.getNextState(b, 1, 40)
    pprint(n_b)
    print(p)
	# print(game.stringRepresentation(b))

	# print(game.getBoardSize())

	# print(game.getActionSize())

	# print(game.getNextState(b,1,30))

	# b = game.getNextState(b,1, 40)[0]

	# print(game.stringRepresentation(b))

    # print(game.getValidMoves(b,1))

	# print(game.getGameEnded(b,1))

	# print(game.getCanonicalForm(b,-1))

	# display(b)


