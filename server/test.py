# import torch
# from torch import nn
# from agents.valueModel import ValueNN, ValueModel
# from game.game import ADJACENT_GT, MIRROR_GT, Board, GameState
# from agents.RLDLAgent import RLAgent
import numpy as np

x = np.zeros((0,5),dtype=np.float32)
y = np.zeros((0,),dtype=np.float32)
for i in range(3):
    x = np.vstack((x,np.array([i,i,i,i,i],dtype=np.float32)))
    y = np.append(y,i)
print(x)
print(y)
x = x.transpose()

print(x.shape,y.shape)

z = x@y
print(z.shape)
print(x,y,z)
# gs = GameState(2, 2)
# print(gs.board.corners)

# board_size = 3
# player_num = 2
# gs_shape = (board_size*4+1, board_size*4+1)
# nn = ValueNN(gs_shape, player_num)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# nn.to(device)
# nn.load_state_dict(torch.load('./models/value_model_minmax100.pt'))
# nn.load_state_dict(torch.load('./models/value_model100.pt'))
# nn.load_state_dict(torch.load('./model2/value_model_minmax2_noexplore80.pt'))
# nn.load_state_dict(torch.load('./model_tzh/vm_mnmx.pt'))


# value_model = ValueModel(gamma=0.95, model=nn, gs_shape=gs_shape, player_num=player_num, lr=0.001)

# agent = RLAgent(board_size, player_num, value_model, 0, 0)
# step = 0
# while not agent.gs.checkWin():
#     next_gs = agent.get_next_gs()
#     agent.step()
#     step += 1
#     print(f'Step {step} eval={agent.minmaxAgent.evaluate(agent.gs)} PID={agent.get_curPID()} V={agent.value_model.getVal(agent.gs)}')

# agent = RLAgent(board_size, player_num, value_model, 0, 1)
# step = 0
# while not agent.gs.checkWin():
#     next_gs = agent.get_next_gs()
#     agent.step()
#     step += 1
#     print(f'Step {step} eval={agent.minmaxAgent.evaluate(agent.gs)} PID={agent.get_curPID()} V={agent.value_model.getVal(agent.gs)}')

