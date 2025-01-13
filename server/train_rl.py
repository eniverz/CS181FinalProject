from agents.RLDLAgent import RLAgent
from agents.valueModel import ValueNN, ValueModel
import torch
import math

board_size = 3
player_num = 2
gs_shape = (board_size*4+1, board_size*4+1)
nn = ValueNN(gs_shape, player_num)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
nn.to(device)
nn.load_state_dict(torch.load('./models/value_model_minmax100.pt'))


value_model = ValueModel(gamma=0.98, model=nn, gs_shape=gs_shape, player_num=player_num, lr=0.0001)
rlagent = RLAgent(board_size, 2, value_model, explore_rate=0.0, minmax_rate=1.0)
rlagent.train(train_steps=5, batch_size=32, rep=10)

torch.save(value_model.model.state_dict(), f'./model_tzh/vm_mnmx.pt')



# for iter in range(30):
#     print(f'Iter {iter} starts')
#     rlagent = RLAgent(board_size, 2, value_model, explore_rate=0.0, minmax_rate=1.0)
#     rlagent.train(train_steps=5, batch_size=32, rep=10)
#     if iter % 10 == 9:
#         torch.save(value_model.model.state_dict(), f'./model2/value_model_minmax_noexplore{iter+1}.pt')

# for iter in range(100):
#     print(f'Iter {iter} starts')
#     rlagent = RLAgent(board_size, 2, value_model, explore_rate=0.4, minmax_rate=0.6)
#     rlagent.train(train_steps=30, batch_size=32, rep=10)
#     if iter % 10 == 9:
#         torch.save(value_model.model.state_dict(), f'./model2/value_model_minmax{iter+1}.pt')

# for iter in range(100):
#     print(f'Iter {iter} starts')
#     rlagent = RLAgent(board_size, 2, value_model, explore_rate=0.0, minmax_rate=1.0*math.cos(iter/100*math.pi/2))
#     rlagent.train(train_steps=30, batch_size=32, rep=10)
#     if iter % 10 == 9:
#         torch.save(value_model.model.state_dict(), f'./model2/value_model_minmax2_noexplore{iter+1}.pt')


# for iter in range(1000):
#     print(f'Iter {iter} starts')
#     rlagent = RLAgent(board_size, 2, value_model, explore_rate=0.1 if iter<800 else 0, minmax_rate=0.5*math.cos(iter/1000*math.pi/2))
#     rlagent.use_minmax = False
#     rlagent.train(train_steps=30, batch_size=32, rep=5)
#     if iter % 100 == 99:
#         torch.save(value_model.model.state_dict(), f'./models2/value_model{iter+1}.pt')
