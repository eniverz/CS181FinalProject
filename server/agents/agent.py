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
        # for pid in range(self.player_num):
        #     for pos in gameState.board.winstate_pos[pid]:
        #         mid[pid] 
        targetLine = [[0, 1, -13],[1, 0, -13],[1, -1, -5],[0, 1, -3], [1, 0, -3], [1, -1, 5]]
        allCheckerValue = []
        for pid in range(self.player_num):
            PlayerCheckers = gameState.board.getPlayerCheckers(pid)
            for checker in PlayerCheckers:
                checker_x = checker[0]
                checker_y = checker[1]
                a = targetLine[pid][0]
                b = targetLine[pid][1]
                c = targetLine[pid][2]
                dist = abs(checker_x * a + checker_y * b + c) / (a ** 2 + b ** 2 + c ** 2) ** 0.5
                if pid == 2 or pid == 5:
                    dist /= 2 ** 0.5 / 2
                allCheckerValue.append(dist)
                
        return allCheckerValue
    
    def step(self):
        self.gs = self.get_next_gs()

