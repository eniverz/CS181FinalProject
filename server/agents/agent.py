from game.game import GameState, ADJACENT_GT, MIRROR_GT

class Agent:
    def __init__(self, board_size:int, player_num:int, game_type:int=ADJACENT_GT):
        self.gs = GameState(board_size, player_num, game_type)
        self.board_size = board_size
        self.player_num = player_num
        self.game_type = game_type
    
    def get_curPID(self):
        return self.gs.curPID

    def get_GameState(self):
        return self.gs

    def get_next_gs(self):
        pass

    def evaluate(self, gameState):
        pass
