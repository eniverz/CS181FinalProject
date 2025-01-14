import numpy as np
from agents.minmaxVEAgent import minmaxAgent_twoplayer_FA
from agents.minmaxAgent import minmaxAgent_twoplayer
import torch
from game.game import GameState
from agents.dviAgent import GreedyAgent, EmptyModel, DVIAgent
from agents.dviModel import dviValueModel, dviVM_V1

# w = np.array([1.06,0.47,-1.24]) # 63/70  -> FA first,FA wins 63steps/mm first,FA wins 70steps
# w_ori = np.array([1,0.3,0.3]) # 69/66
# BATTLE : 63/-69


# w = np.array([0.41,0.20,-0.15]) # 73/66 hard:-54/58
# w_ori = np.array([0.5,0.2,0]) # 73/66 hard: -54/
# BATTLE : 69/-65 -> trained frist,trained win 69steps/ori first,ori win 65steps

# w = np.array([0.97, 0.39, -1.11]) # 63/70
# w_ori = np.array([0.9,0.2,0.4]) # 69/66
# BATTLE 63/-69

# w = np.array([0.51, 0.36, -0.27]) # 63/64
# w_ori = np.array([0.5,0.5,0.5]) # 73/66
# BATTLE -58/-65

# w = np.array([0.35, 0.72, -0.41]) # 57/68
# w_ori = np.array([0.3,1.0,0.3]) # 57/68
# BATTLE 67/68

# w = np.array([0.3, 0.24, 0.57]) # 60/66
# w_ori = np.array([0.3,0.3,1]) # 63/66
# BATTLE 69/-69

# w = np.array([0.40, 0.59, -0.27]) # 63/64
# w_ori = np.array([0.3,0.7,0.7]) # 65/60
# BATTLE -64/62

# w = np.array([0.75, 0.61, -0.12]) # 63/64
# w_ori = np.array([0.7,0.7,0.3]) # 73/74
# BATTLE 71/-69

# w = np.array([0.73, 0.37, -0.3]) # 63/64
# w_ori = np.array([0.7,0.3,0.7]) # 67/66
# BATTLE 61/-65

# w = np.array([0.44, 0.42, 0.1]) # 73/74
# w_ori = np.array([0.4,0.5,0.6]) # 73/66
# BATTLE 71/70


# ------------THE FOLLOWING ARE BAD ATTEMPTS(NOT CONVERGE)-----------------
# w = np.array([0.95, 0.65, -0.6]) # 63/64
# w_ori = np.array([1.0,1.0,1.0]) # 73/66
# BATTLE -70/-65


w = np.array([0.25,0.35,0.06]) # 69/74
w_ori = np.array([0.2,0.5,0.8]) # 67/70
# BATTLE -66/74


board_size = 3
max_depth = 2
input_shape = (board_size*2+1,  board_size*2+1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


agent_FA = minmaxAgent_twoplayer_FA(board_size, max_depth, w)
agent_FA_ori = minmaxAgent_twoplayer_FA(board_size, max_depth, w_ori)
agent_mm = minmaxAgent_twoplayer(board_size, 2, max_depth)
agent_mm4 = minmaxAgent_twoplayer(board_size, 2, max_depth=4)
agent_greedy = GreedyAgent(board_size, 2)
agent_empty_dvi = DVIAgent(board_size, 2, EmptyModel(), device=device)


vm = dviVM_V1(board_size, input_shape, 2).to(device=device)
vm.load_state_dict(torch.load('models/dvi/v1_69.pt'))
vmodel = dviValueModel(board_size, input_shape, vm)
agent_dvi = DVIAgent(board_size, 2, vmodel, explore_rate=0, device=device)

# from agents.valueModel import ValueNN, ValueModel
# from agents.RLDLAgent import RLAgent_DLvalue
# import torch
# gs_shape = (board_size*4+1, board_size*4+1)
# nn = ValueNN(gs_shape, 2)
# nn.to(device)
# # nn.load_state_dict(torch.load('./models/value_model_minmax100.pt'))
# # nn.load_state_dict(torch.load('./models/value_model100.pt'))
# # nn.load_state_dict(torch.load('./model2/value_model_minmax2_noexplore80.pt'))
# nn.load_state_dict(torch.load('./models/scratch30.pt'))


# value_model = ValueModel(gamma=0.95, model=nn, gs_shape=gs_shape, player_num=2, lr=0.001)

# rlagent = RLAgent_DLvalue(board_size, 2, value_model, 0, 0)

def battle(board_size, agent1, name1, agent2, name2, battle_name):
    print(battle_name)
    gs = GameState(board_size, 2)
    step = 0
    draw = False
    while not gs.checkEnd():
        if gs.curPID == 0:
            agent1.set_GameState(gs)
            gs = agent1.get_next_gs()
        else:
            agent2.set_GameState(gs)
            gs = agent2.get_next_gs()
        step += 1
        if step > 200:
            draw = True
            break
    if not draw:
        print(f'{name1} play first. {name1 if gs.getwinner()==0 else name2} wins after {step}steps.')
    else:print(f'{name2} play first. Draw.')
    gs = GameState(board_size, 2)
    step = 0
    draw = False
    while not gs.checkEnd():
        if gs.curPID == 0:
            agent2.set_GameState(gs)
            gs = agent2.get_next_gs()
        else:
            agent1.set_GameState(gs)
            gs = agent1.get_next_gs()
        # print(agent2.evaluate(gs))
        step += 1
        if step > 200:
            draw = True
            break
        # print(step)    

    # print(agent2.record_input)
    # print(agent2.record_V)
    if not draw:
        print(f'{name2} play first. {name2 if gs.getwinner()==0 else name1} wins after {step}steps.')
    else:print(f'{name2} play first. Draw.')


# battle(board_size, agent_FA, "trainedFA", agent_mm4, "base-hard", "TRAINED vs base-hard")
# battle(board_size, agent_FA, "oriFA", agent_mm4, "base-hard", "ORI vs base-hard")
# battle(board_size, agent_FA, "trainedFA", agent_mm, "base", "TRAINED vs base")
# battle(board_size, agent_FA_ori, "oriFA", agent_mm, "base", "ORI vs base")
# battle(board_size, agent_FA, "trained", agent_FA_ori, "ori", "TRAINED vs ORI")
# battle(board_size, rlagent, "rl agent", agent_mm, "ori", "rl vs ori")
# battle(board_size, agent_greedy, "greedy", agent_mm, "base", "greedy vs base")
while True:
    battle(board_size, agent_greedy, "greedy", agent_dvi, "dvi", "greedy vs dvi")