import torch
import torch.nn as nn
from game.game import GameState
import torch.optim as optim
from torch.optim.lr_scheduler import ExponentialLR

class resblock(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(resblock, self).__init__()
        self.cv=nn.Sequential(
            nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(),
            nn.Conv2d(out_channel, out_channel, 3,1,1),
            nn.BatchNorm2d(out_channel),
            nn.ReLU()
        )
        self.cp=nn.Conv2d(in_channel,out_channel, 1)
    def forward(self, x):
        return self.cp(x)+self.cv(x)

class dviVM_V1(nn.Module):
    def __init__(self, board_size, input_shape, output_size):
        super(dviVM_V1, self).__init__()
        self.input_shape = input_shape
        self.output_size = output_size
        self.board_size = board_size
        self.prework = nn.Sequential(
            nn.Conv2d(3, 16, 7,2,3),
            nn.BatchNorm2d(16),
            nn.ReLU()
        )
        self.resblock1 = resblock(16, 32)
        self.resblock2 = resblock(32, 32)
        res_shape = [(input_shape[0]+1)//2,(input_shape[1]+1)//2]
        self.output = nn.Sequential(
            nn.Flatten(),
            nn.Linear(res_shape[0]*res_shape[1]*32, 1024),
            nn.Linear(1024, output_size)
        )
    def forward(self, x):
        x = self.prework(x)
        x = self.resblock1(x)
        x = self.resblock2(x)
        x = self.output(x)
        return x

def gs_to_input(gs, board_size):
    cur_record_input = torch.empty([3, 2*board_size+1, 2*board_size+1], dtype=torch.float32)
    for i in range(board_size*2+1):
        for j in range(board_size*2+1):
            x = i + board_size
            y = j + board_size*3-x
            cur_record_input[0,i,j] = gs.board.board[x][y]
            cur_record_input[1,i,j] = gs.board.board[x][y]==1
            cur_record_input[2,i,j] = gs.board.board[x][y]==2
    return cur_record_input

class dviValueModel():
    def __init__(self, board_size, input_shape, model:nn.Module):
        self.input_shape = input_shape
        self.input_size = input_shape[0] * input_shape[1]
        self.board_size = board_size
        self.model = model
        self.device = next(model.parameters()).device

    def getVal(self, gs, pid):
        input_board = gs_to_input(gs, self.board_size).unsqueeze(0).to(device=self.device)
        res = self.model.forward(input_board).detach().cpu()
        return res[0,pid]
    
    def train(self, record_input, record_V, record_PID, max_epochs=500, start_lr=0.01, end_lr=0.001):
        criterion = nn.HuberLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=start_lr)

        gamma = (end_lr / start_lr) ** (1 / max_epochs)
        scheduler = ExponentialLR(optimizer, gamma=gamma)
        loss_cache_size = 20
        prelosses = [1e2 for _ in range(loss_cache_size)]
        preloss = 1e2
        for epoch in range(max_epochs):
            outputs = self.model(record_input)
            targets = record_V
            outputs = outputs.gather(1, record_PID)
            loss = criterion(outputs, targets)
            if loss < 1e-2:break
            optimizer.zero_grad()
            loss.backward()
            preloss = preloss - prelosses[0]/loss_cache_size + loss.detach()/loss_cache_size
            prelosses = prelosses[1:] + [loss.detach()]
            print(loss, preloss)
            # if loss > preloss:
            #     break
            optimizer.step()
            scheduler.step()