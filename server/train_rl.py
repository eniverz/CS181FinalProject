from agents.RLAgent import RLAgent
from agents.valueModel import ValueNN, ValueModel
import torch

board_size = 4
player_num = 2
nn = ValueNN((board_size*4, board_size*4), player_num)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
nn.to(device)


value_model = ValueModel(gamma=0.95, model=nn, gs_shape=(board_size*4, board_size*4), player_num=player_num, lr=0.001)

rlagent = RLAgent(board_size, 2, value_model, 0.1)


rlagent.use_minmax = True
for iter in range(100):
    rlagent.train(train_steps=100, batch_size=32, rep=10)

rlagent.use_minmax = False
for iter in range(1000):
    rlagent.train(train_steps=100, batch_size=32, rep=5)

