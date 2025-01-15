import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from game.game import ADJACENT_GT, MIRROR_GT, Board, GameState

from game.utils import *
BOARD_HIST_MOVES = 3

class Model(nn.Module):
    def __init__(self, input_dim, filters, gs, version=0):
        super(Model, self).__init__()
        self.input_dim = input_dim
        self.filters = filters
        self.version = version
        self.gs = gs

    def predict(self, input_board):
        self.eval()
        with torch.no_grad():
            input_board = torch.tensor(input_board, dtype=torch.float32).unsqueeze(0)
            logits, v = self.forward(input_board)
            p = softmax(logits.numpy())
            return p.squeeze(), v.squeeze()

    def save(self, save_dir, model_prefix, version):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.version = version
        torch.save(self.state_dict(), '{}/{}{:0>4}.pth'.format(save_dir, model_prefix, version))
        print('\nSaved model "{}{:0>4}.pth" to "{}"\n'.format(model_prefix, version, save_dir))

    def save_weights(self, save_dir, prefix, version):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        torch.save(self.state_dict(), '{}/{}{:0>4}-weights.pth'.format(save_dir, prefix, version))
        stress_message('Saved model weights "{}{:0>4}-weights" to "{}"'.format(prefix, version, save_dir), True)

    def load(self, filepath):
        self.load_state_dict(torch.load(filepath))
        return self

    def load_weights(self, filepath):
        self.load_state_dict(torch.load(filepath))
        return self

class ResidualCNN(Model):
    def __init__(self, gs, filters=64):
        input_dim = (gs.board.len, gs.board.len, BOARD_HIST_MOVES * 2 + 1)
        Model.__init__(self, input_dim, filters, gs)
        self.model = self.build_model(gs)

    def build_model(self, gs):
        layers = []
        layers.append(nn.Conv2d(self.input_dim[0], 64, kernel_size=3, padding=1))
        layers.append(nn.BatchNorm2d(64))
        layers.append(nn.ReLU(inplace=True))

        for _ in range(9):
            layers.append(self.residual_block(64, [32, 32, 64], kernel_size=3))

        self.policy_head = self.build_policy_head(64, gs.board.len, gs.player_num)
        self.value_head = self.build_value_head(64, gs.board.len)

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.model(x)
        policy = self.policy_head(x)
        value = self.value_head(x)
        return policy, value

    def build_policy_head(self, in_channels, len, player_num):
        layers = []
        layers.append(nn.Conv2d(in_channels, 16, kernel_size=1))
        layers.append(nn.BatchNorm2d(16))
        layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Flatten())
        layers.append(nn.Linear(16 * len * len, player_num * len * len))
        return nn.Sequential(*layers)

    def build_value_head(self, in_channels, len):
        layers = []
        layers.append(nn.Conv2d(in_channels, 1, kernel_size=1))
        layers.append(nn.BatchNorm2d(1))
        layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Flatten())
        layers.append(nn.Linear(len * len, 32))
        layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Linear(32, 1))
        layers.append(nn.Tanh())
        return nn.Sequential(*layers)

    def residual_block(self, in_channels, filters, kernel_size):
        layers = []
        layers.append(nn.Conv2d(in_channels, filters[0], kernel_size=1))
        layers.append(nn.BatchNorm2d(filters[0]))
        layers.append(nn.ReLU(inplace=True))

        layers.append(nn.Conv2d(filters[0], filters[1], kernel_size=kernel_size, padding=1))
        layers.append(nn.BatchNorm2d(filters[1]))
        layers.append(nn.ReLU(inplace=True))

        layers.append(nn.Conv2d(filters[1], filters[2], kernel_size=1))
        layers.append(nn.BatchNorm2d(filters[2]))

        return nn.Sequential(*layers)

if __name__ == '__main__':
    model = ResidualCNN()
    print(model)