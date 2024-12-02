from game.game import Board, GameState, MIRROR_GT, ADJACENT_GT
import numpy as np
from copy import deepcopy

gs = GameState(4, 1, MIRROR_GT)
gs.board.debugPlayerCheckers()
gs.board = gs.board.moveChecker((9,3),(8,6),0)
gs.board.debugPlayerCheckers()
print(gs.board.nextSteps((10,2)))
print(gs.board.nextSteps((11,2)))
# print(gs.checkWin())
# x = deepcopy(gs.board.checkerlist[1])
# gs.board.checkerlist[1] = deepcopy(gs.board.checkerlist[0])
# gs.board.checkerlist[0] = x
# print(gs.checkWin())
# pos = [[i, j] for i in range(17) for j in range(17) if gs.board.posInBoard((i, j))]
# position = [[True if gs.board.posInBoard((i,j)) else False for j in range(17)] for i in range(17)]
# np.set_printoptions(linewidth=200)
# print(pos)
# print(np.array(position))
# print([8,8] in pos)
# gs = GameState(2, 6)
# gs.board = gs.board.moveChecker((5,1),(5,2),0)
# # gs.board.debugPlayerCheckers()
# for ns in gs.nextGameStates():
#     pass
#     # ns.board.debugPlayerCheckers()
