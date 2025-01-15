from agents.dviAgent import DVIAgent
from agents.dviModel import dviValueModel,dviVM_V1
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
board_size = 3
input_shape = (board_size*2+1, board_size*2+1)
vm = dviVM_V1(board_size, input_shape, 2).to(device=device)
vmodel = dviValueModel(board_size, input_shape, vm)


for iter in range(500):
    # explore_rate = 0 if iter>700 else 0.5*(1-iter/700)
    explore_rate = 0.4
    fail = True
    while fail:
        fail = False
        dviagent = DVIAgent(board_size, 2, vmodel, explore_rate=explore_rate, device=device)
        step = 0
        while not dviagent.gs.checkEnd():
            step += 1
            dviagent.step()
            if step > 200:
                fail = True
                break
        if not fail:
            dviagent.train()
            print(f'Iter {iter} ends after {step} steps.')
            if iter % 10 == 9:
                torch.save(vm.state_dict(), f"models/dvi2/v1_iter{iter+1}.pt")