from game.game import ADJACENT_GT, MIRROR_GT, GameState


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

    def get_GameState(self):
        return self.gs

    def get_next_gs(self) -> GameState:
        raise NotImplementedError("Error: Don't use abstract method. Please implement first")

    def evaluate(self, gameState):
        targetLine = [
            [0, 1, -(3 * self.board_size + 1)],
            [1, 0, -(3 * self.board_size + 1)],
            [1, -1, -(self.board_size + 1)],
            [0, -1, self.board_size - 1],
            [-1, 0, self.board_size - 1],
            [-1, 1, -(self.board_size + 1)],
        ]
        if self.player_num == 1:
            playerIDs = [0]
        elif self.player_num == 2:
            playerIDs = [0, 3]
        elif self.player_num == 3:
            playerIDs = [0, 2, 4]
        elif self.player_num == 6:
            playerIDs = [0, 1, 2, 3, 4, 5]
        else:
            raise ValueError("Invalid player_num")
        allCheckerValue = []
        for idx, pid in enumerate(playerIDs):
            playerCheckers = gameState.board.getPlayerCheckers(idx)
            dist = 0
            for checker in playerCheckers:
                checker_x = checker[0]
                checker_y = checker[1]
                a = targetLine[pid][0]
                b = targetLine[pid][1]
                c = targetLine[pid][2]
                judge = checker_x * a + checker_y * b + c
                if judge < 0:
                    dist += -judge / (a**2 + b**2) ** 0.5
            if pid == 2 or pid == 5:
                dist /= 2**0.5 / 2
            allCheckerValue.append(dist)

        return allCheckerValue

    def step(self):
        self.gs = self.get_next_gs()
