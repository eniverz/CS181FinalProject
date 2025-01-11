from game.game import Board, GameState, MIRROR_GT, ADJACENT_GT
from agents.minmaxAgent import minmaxAgent_multiplayer, minmaxAgent_twoplayer


board_size = 4
player_num = 1
game_type = MIRROR_GT
max_depth = 3

# gs = GameState(board_size, player_num, game_type)
# agent = minmaxAgent_multiplayer(board_size, player_num, max_depth, game_type)
agent = minmaxAgent_twoplayer(board_size, player_num, max_depth, game_type)
print(agent.gs)
agent.gs.board.debugPlayerCheckers()
print(agent.gs.board.winstate_pos)

st = 0
while not agent.get_GameState().checkWin():
    agent.step()
    st += 1
    agent.get_GameState().board.debugPlayerCheckers()    
    print(agent.gs.board.winstate_pos)
    print(agent.evaluate(agent.get_GameState()))
print(st)

