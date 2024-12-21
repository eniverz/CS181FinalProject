from game.game import Board, GameState, ADJACENT_GT, MIRROR_GT
from agent import Agent

class minmaxAgent(Agent):
    def __init__(self, board_size:int, player_num:int, max_depth:int, game_type:int=ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.max_depth = max_depth

    def 