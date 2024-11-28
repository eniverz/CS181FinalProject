from game.game import Board, GameState

gs = GameState(2, 6)
gs.board = gs.board.moveChecker((5,1),(5,2),0)
# gs.board.debugPlayerCheckers()
for ns in gs.nextGameStates():
    pass
    # ns.board.debugPlayerCheckers()