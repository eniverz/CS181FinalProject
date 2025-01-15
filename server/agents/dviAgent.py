from agents.agent import Agent
from game.game import GameState
import random
from game.utils import MahattanDIS,ADJACENT_GT

def get_reward(gs:GameState, next_gs:GameState):
    pid = gs.curPID
    start_pos, end_pos = next_gs.movement

    # r = abs(gs.board.corners[pid][1]-start_pos[1]) - abs(gs.board.corners[pid][1]-end_pos[1])
    r = MahattanDIS(gs.board.corners[pid], start_pos) - MahattanDIS(gs.board.corners[pid], end_pos)
    if r < 0: r *= 0.01
    if next_gs.board.checkWin(pid):
        r += 15
    # print(start_pos, end_pos, r, gs.board.corners[pid])
    return r


class GreedyAgent(Agent):
    def __init__(self, board_size: int, player_num: int, explore_rate: float=0, game_type: int = ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.explore_rate = explore_rate
        # self.minmaxAgent = minmaxAgent(board_size, player_num, max_depth=2, game_type=game_type)
    def get_next_gs(self):
        possibleList = self.gs.nextGameStates()
        if random.random()<self.explore_rate:
            return random.choice(possibleList)
        best_reward = -1e9
        best_next_gs = []
        for next_gs in possibleList:
            reward = get_reward(self.gs, next_gs)
            if reward > best_reward:
                best_next_gs = [next_gs]
                best_reward = reward
            elif reward == best_reward:
                best_next_gs.append(next_gs)
        return random.choice(best_next_gs)

class EmptyModel():
    def __init__(self):
        pass
    def getVal(self, x, y):
        return 0
    def train(self, x, y):
        pass

import torch
from agents.dviModel import gs_to_input

class DVIAgent(Agent):
    def __init__(self, board_size: int, player_num: int, vmodel, gamma: float=0.9, explore_rate: float=0, device="cpu", game_type: int = ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.vmodel = vmodel
        self.explore_rate = explore_rate
        self.gamma = gamma
        self.device = device
        self.record_input = torch.empty([0, 3, 2*board_size+1, 2*board_size+1], dtype=torch.float32).to(device=self.device)
        self.record_V = torch.empty([0, 1], dtype=torch.float32).to(device=self.device)
        self.record_PID = torch.empty([0, 1], dtype=torch.long).to(device=self.device)

    def record(self, gs:GameState, V):
        cur_record_input = gs_to_input(gs, self.board_size).to(device=self.device)
        cur_record_V = torch.tensor([V], dtype=torch.float32).to(device=self.device)
        cur_record_PID = torch.tensor([gs.curPID], dtype=torch.long).to(device=self.device)
        self.record_input = torch.cat((self.record_input, cur_record_input.unsqueeze(0)), dim=0)
        self.record_V = torch.cat((self.record_V, cur_record_V.unsqueeze(0)), dim=0)
        self.record_PID = torch.cat((self.record_PID, cur_record_PID.unsqueeze(0)), dim=0)

    def clear_record(self):
        self.record_input = torch.empty([0, 3, 2*self.board_size+1, 2*self.board_size+1], dtype=torch.float32).to(device=self.device)
        self.record_V = torch.empty([0, 1], dtype=torch.float32).to(device=self.device)
        self.record_PID = torch.empty([0, 1], dtype=torch.long).to(device=self.device)


    def get_next_gs(self):
        possibleList = self.gs.nextGameStates()
        if random.random()<self.explore_rate:
            return random.choice(possibleList)
        best_V = -1e9
        best_next_gs = []
        for next_gs in possibleList:
            reward = get_reward(self.gs, next_gs)
            V = self.vmodel.getVal(next_gs, self.get_curPID()) * self.gamma + reward
            if V > best_V:
                best_next_gs = [next_gs]
                best_V = V
            elif V == best_V:
                best_next_gs.append(next_gs)
        self.record(self.gs, best_V)
        return random.choice(best_next_gs)
    
    def train(self):
        self.vmodel.train(self.record_input, self.record_V, self.record_PID)

def create_dviagent(board_size, device, path=None, agent_type='v1'):
    if agent_type not in ['v1']:
        return None
    if agent_type == 'v1':
        from agents.dviModel import dviValueModel,dviVM_V1
        input_shape = (board_size*2+1,  board_size*2+1)
        vm = dviVM_V1(board_size, input_shape, 2).to(device=device)
        if path is not None:
            vm.load_state_dict(torch.load(path,map_location=device))
        vmodel = dviValueModel(board_size, input_shape, vm)
        agent_dvi = DVIAgent(board_size, 2, vmodel, explore_rate=0, device=device)
        return agent_dvi