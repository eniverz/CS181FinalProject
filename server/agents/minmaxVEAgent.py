from agents.agent import Agent
from game.game import ADJACENT_GT, MIRROR_GT, Board, GameState
from game.utils import MahattanDIS, EuclideanDIS
import numpy as np

FEATURE_CNT = 3

def calculateF(gs:GameState, pid):
    Flist = []
    N = gs.board.N
    f = 0
    for checker in gs.board.getPlayerCheckers(pid):
        f += EuclideanDIS(checker, gs.board.corners[pid])**2
    Flist.append(f)

    f = 0
    for checker in gs.board.getPlayerCheckers(pid):
        tx = -0.5*checker[1] + 3*N
        f += abs(checker[0]-tx)**2
    Flist.append(f)

    # f = 0
    # for checker in gs.board.getPlayerCheckers(pid):
    #     f += MahattanDIS(checker, gs.board.corners[pid])**2
    # Flist.append(f)
    f = 0
    for checker in gs.board.getPlayerCheckers(pid):
        f += MahattanDIS(checker, gs.board.corners[pid])
    Flist.append(f)

    # f = 0
    # for checker in gs.board.getPlayerCheckers(pid):
    #     f += abs(checker[1]-gs.board.corners[pid][1])
    # Flist.append(f)


    # f = 0
    # for checker in gs.board.getPlayerCheckers(pid):
    #     f += abs(checker[1]-gs.board.corners[pid][1])**2
    # Flist.append(f)

    return np.array(Flist)

class minmaxAgent_twoplayer_FA(Agent):
    def __init__(self, board_size: int, max_depth: int, w: np.ndarray, game_type: int = ADJACENT_GT):
        super().__init__(board_size, 2, game_type)
        self.max_depth = max_depth
        self.w = w

    def evaluateF(self, gs: GameState):
        return calculateF(gs, 0) - calculateF(gs, 1)
    def evaluate(self, gs: GameState):
        """
        return a single float
        the smaller, the better
        """
        return np.dot(self.evaluateF(gs), self.w)
        # return res[curPID]

    def maxLayer_TwoPlayer(self, gs: GameState, alpha, beta, depth, curPID):
        if depth == self.max_depth or gs.checkWin():
            return self.evaluate(gs), None

        best_next_gs = None
        mx = float("-inf")
        for next_gs in gs.nextGameStates():
            res, _ = self.minLayer_TwoPlayer(next_gs, alpha, beta, depth + 1, curPID)
            if res > mx:
                mx = res
                best_next_gs = next_gs
                alpha = max(alpha, res)
                if res >= beta:
                    break
        return mx, best_next_gs

    def minLayer_TwoPlayer(self, gs: GameState, alpha, beta, depth, curPID):
        if depth == self.max_depth or gs.checkWin():
            return self.evaluate(gs), None

        best_next_gs = None
        mn = float("inf")
        for next_gs in gs.nextGameStates():
            res, _ = self.maxLayer_TwoPlayer(next_gs, alpha, beta, depth + 1, curPID)
            if res < mn:
                mn = res
                best_next_gs = next_gs
                beta = min(beta, res)
                if res <= alpha:
                    break
        return mn, best_next_gs

    def record_next_gs_and_V(self):
        curPID = self.get_curPID()
        return self.minLayer_TwoPlayer(gs=self.get_GameState(), alpha=-float("inf"), beta=float("inf"), depth=0, curPID=curPID) if curPID == 0 \
            else self.maxLayer_TwoPlayer(gs=self.get_GameState(), alpha=-float("inf"), beta=float("inf"), depth=0, curPID=curPID)

    def get_next_gs(self):
        curPID = self.get_curPID()
        return self.minLayer_TwoPlayer(gs=self.get_GameState(), alpha=-float("inf"), beta=float("inf"), depth=0, curPID=curPID)[1] if curPID == 0 \
            else self.maxLayer_TwoPlayer(gs=self.get_GameState(), alpha=-float("inf"), beta=float("inf"), depth=0, curPID=curPID)[1]

def train_minmaxFA_one_game(board_size: int, max_depth: int, w: np.ndarray, game_type: int = ADJACENT_GT):
    agent = minmaxAgent_twoplayer_FA(board_size, max_depth, w, game_type)
    ftargets = np.zeros((0,FEATURE_CNT),dtype=np.float32)
    Vtargets = np.zeros((0,),dtype=np.float32)
    steps = 0
    while not agent.get_GameState().board.checkWin(0) and not agent.get_GameState().board.checkWin(1):
        V, next_gs = agent.record_next_gs_and_V()
        ftargets = np.vstack((ftargets, agent.evaluateF(agent.get_GameState())))
        Vtargets = np.append(Vtargets, V)
        agent.set_GameState(next_gs)
        steps += 1
    # print(ftargets, Vtargets)
    # print(steps)
    w_new, residuals, rank, s = np.linalg.lstsq(ftargets, Vtargets)
    return w_new

def train_minmaxFA(board_size: int, max_depth: int, w: np.ndarray, game_type: int = ADJACENT_GT):
    lr = 0.1
    decay = 0.95
    mnlr = 0.01
    # first_epoch = True
    first_epoch = False
    while True:
        w_new = train_minmaxFA_one_game(board_size, max_depth, w, game_type)
        print(w_new-w, np.linalg.norm(w_new-w), lr)
        if np.linalg.norm(w_new-w) < 1e-2:
            break
        if first_epoch:
            w = (w+w_new) / 2
        else:
            w = w + lr*(w_new-w)
            lr *= decay
            if lr < mnlr:
                lr = mnlr
        print(w)
    return minmaxAgent_twoplayer_FA(board_size, max_depth, w, game_type), w
