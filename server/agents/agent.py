from game.game import ADJACENT_GT, MIRROR_GT, GameState
from math import sqrt

def MahattanDIS(pos1, pos2):
    if pos1[0] <= pos2[0] and pos1[1] <= pos2[1]:
        return pos2[0] - pos1[0] + pos2[1] - pos1[1]
    if pos1[0] >= pos2[0] and pos1[1] >= pos2[1]:
        return pos1[0] - pos2[0] + pos1[1] - pos2[1]
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

class Agent:
    def __init__(self, board_size: int, player_num: int, game_type: int = ADJACENT_GT):
        self.gs = GameState(board_size, player_num, game_type)
        self.board_size = board_size
        self.player_num = player_num
        self.game_type = game_type

    def get_curPID(self):
        return self.gs.curPID

    def set_GameState(self, gs):
        self.gs = gs

    def get_GameState(self) -> GameState:
        return self.gs

    def get_next_gs(self) -> GameState:
        raise NotImplementedError("Error: Don't use abstract method. Please implement first")

    def evaluate(self, gameState:GameState):
        val = [0] * gameState.player_num
        for pid in range(self.gs.player_num):
            for checker in gameState.board.getPlayerCheckers(pid):
                val[pid] += MahattanDIS(checker, gameState.board.corners[pid])
        return val

    def step(self):
        self.gs = self.get_next_gs()
