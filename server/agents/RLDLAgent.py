from agents.agent import Agent
from game.game import ADJACENT_GT, MIRROR_GT, Board, GameState
import torch
import random
from agents.minmaxAgent import minmaxAgent
from agents.valueModel import ValueModel
# V(value)
# pi(next action)
# R(reward)


class RLAgent_DLvalue(Agent):
    def __init__(self, board_size: int, player_num: int, value_model: ValueModel, explore_rate: float, minmax_rate: float, game_type: int = ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.value_model = value_model
        self.explore_rate = explore_rate
        self.minmax_rate = minmax_rate
        self.minmaxAgent = minmaxAgent(board_size, player_num, max_depth=2, game_type=game_type)
        self.store = []

    def get_next_gs(self) -> GameState:
        possibleList = self.gs.nextGameStates()
        rs = random.random()
        if rs < self.explore_rate:
            return random.choice(possibleList)
        elif rs < self.explore_rate + self.minmax_rate:
                self.minmaxAgent.set_GameState(self.gs)
                return self.minmaxAgent.get_next_gs()
        else:
            max_val = -float("inf")
            best_next_gs = []
            for next_gs in possibleList:
                value = self.value_model.getVal(next_gs)
                value = value[self.get_curPID()] - value[1-self.get_curPID()]
                if value > max_val:
                    best_next_gs = [next_gs]
                    max_val = value
                elif value == max_val:
                    best_next_gs.append(next_gs)
            return random.choice(best_next_gs)

    def train(self, train_steps, batch_size, rep=1):
        step = 0
        while not self.gs.board.checkWin(0) and not self.gs.board.checkWin(1):
            # print(f'Step {step} starts')
            next_gs = self.get_next_gs()
            # reward = [next_gs.board.checkWin(pid)*2-1 for pid in range(self.player_num)]
            reward = [int(next_gs.board.checkWin(pid)) for pid in range(self.player_num)]
            self.value_model.store_sample(self.gs, next_gs, reward)
            self.gs = next_gs
            step += 1
            print(f'Step {step} finishes with reward={reward} eval={self.minmaxAgent.evaluate(self.gs)}')
            # if step % train_steps == 0:
            #     self.value_model.step(batch_size, rep)
        # return
        self.value_model.step(batch_size, rep)
        print(f'Finish training with {step} steps')


