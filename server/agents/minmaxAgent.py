from game.game import Board, GameState, ADJACENT_GT, MIRROR_GT
from agents.agent import Agent

class minmaxAgent_multiplayer(Agent):
    def __init__(self, board_size:int, player_num:int, max_depth:int, game_type:int=ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.max_depth = max_depth

    def minLayer_Multiplayer(self, gs:GameState, depth):
        '''
        Return result:list[float], best_next_gameState:gamestate
        '''
        if depth == self.max_depth or gs.checkWin():
            return self.evaluate(gs), None
        best_next_gs = None
        best_value = None
        mn = float('inf')
        curPID = self.get_curPID()
        for next_gs in gs.nextGameStates():
            res, _ = self.minLayer_Multiplayer(next_gs, depth+1)
            if res[curPID] < mn:
                mn = res[curPID]
                best_next_gs = next_gs
                best_value = res
        return best_value, best_next_gs

    def get_next_gs(self):
        return self.minLayer_Multiplayer(self.get_GameState(), 0)[1]


class minmaxAgent_twoplayer(Agent):
    def __init__(self, board_size:int, player_num:int, max_depth:int, game_type:int=ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.max_depth = max_depth

    def evaluate_twoplayer_minmax(self, gs:GameState, curPID):
        '''
        return a single float
        the smaller, the better
        '''
        res = self.evaluate(gs)
        oppPID = 1 - curPID
        return res[curPID] - res[oppPID]

    def maxLayer_TwoPlayer(self, gs:GameState, alpha, beta, depth, curPID):
        if depth == self.max_depth or gs.checkWin():
            return self.evaluate_twoplayer_minmax(gs, curPID), None
            
        best_next_gs = None
        mx = float('-inf')
        for next_gs in gs.nextGameStates():
            res, _ = self.minLayer_TwoPlayer(next_gs, alpha, beta, depth+1, curPID)
            if res > mx:
                mx = res
                best_next_gs = next_gs
                alpha = max(alpha, res)
                if res >= beta:break
        return mx, best_next_gs
        
    def minLayer_TwoPlayer(self, gs:GameState, alpha, beta, depth, curPID):
        if depth == self.max_depth or gs.checkWin():
            return self.evaluate_twoplayer_minmax(gs, curPID), None
            
        best_next_gs = None
        mn = float('inf')
        for next_gs in gs.nextGameStates():
            res, _ = self.maxLayer_TwoPlayer(next_gs, alpha, beta, depth+1, curPID)
            if res < mn:
                mn = res
                best_next_gs = next_gs
                beta = min(beta, res)
                if res <= alpha:break
        return mn, best_next_gs
        
    def get_next_gs(self):
        return self.minLayer_TwoPlayer(
            gs=self.get_GameState(),
            alpha=-float('inf'),
            beta=float('inf'),
            depth=0,
            curPID=self.get_curPID()
        )