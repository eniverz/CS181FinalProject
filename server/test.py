from game.game import Board, GameState, MIRROR_GT, ADJACENT_GT

gs = GameState(4, 1, MIRROR_GT)
gs.board = gs.board.moveChecker((10,3),(10,4),0)
gs.board = gs.board.moveChecker((11,3),(9,5),0)
print(gs.board.nextSteps((12,2)))
