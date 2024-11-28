from game.game import Board, GameState
import numpy as np

gs = GameState(4, 2)
pos = [[i, j] for i in range(17) for j in range(17) if gs.board.posInBoard((i, j))]
position = [[True if gs.board.posInBoard((i,j)) else False for j in range(17)] for i in range(17)]
np.set_printoptions(linewidth=200)
print(pos)
print(np.array(position))
print([8,8] in pos)
# gs = GameState(2, 6)
# gs.board = gs.board.moveChecker((5,1),(5,2),0)
# # gs.board.debugPlayerCheckers()
# for ns in gs.nextGameStates():
#     pass
#     # ns.board.debugPlayerCheckers()
