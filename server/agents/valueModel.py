import torch
from torch import nn
from game.game import GameState
import random
from torch.optim.lr_scheduler import LambdaLR
from copy import deepcopy

class ValueNN(nn.Module):
    def __init__(self, gs_shape, player_num):
        super(ValueNN, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(1, 4, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Linear(4 * (gs_shape[0] // 4) * (gs_shape[1] // 4), 64),
            nn.GELU(),
        )
        self.linear = nn.Sequential(
            nn.Flatten(),
            nn.Linear(gs_shape[0]*gs_shape[1], 256),
            nn.LeakyReLU(),
            nn.Linear(256, 64),
            nn.LeakyReLU(),
        )
        self.reg = nn.Linear(128, player_num)

    def forward(self, x):
        cx = self.conv(x.unsqueeze(1))
        lx = self.linear(x)
        x = self.reg(torch.cat((cx, lx), 1))
        return x



class dataCACHE():
    def __init__(self, device, gs_shape):
        self.curgs = torch.empty((0, *gs_shape), device=device, dtype=torch.float32)
        self.nextgs = torch.empty((0, *gs_shape), device=device, dtype=torch.float32)
        self.reward = torch.empty((0, 2), device=device, dtype=torch.float32)
        # self.reward = torch.empty((0, 1), device=device, dtype=torch.float32)
        # self.PID = torch.empty((0, 1), device=device, dtype=torch.int64)

    def size(self):
        return self.curgs.shape[0]
    
    def empty(self):
        return self.size() == 0
    
    def getBatch(self, batch_size, rep=1, random=False):
        if not random:
            for _ in range(rep):
                curidx = 0
                while curidx < self.size():
                    c_batch_size = min(batch_size, self.size()-curidx)
                    # res = [self.curgs[curidx:curidx+c_batch_size],
                    #     self.nextgs[curidx:curidx+c_batch_size],
                    #     self.reward[curidx:curidx+c_batch_size],
                    #     self.PID[curidx:curidx+c_batch_size]]
                    res = [self.curgs[curidx:curidx+c_batch_size],
                        self.nextgs[curidx:curidx+c_batch_size],
                        self.reward[curidx:curidx+c_batch_size]]
                    yield res
                    curidx += c_batch_size
        else:
            N = self.size()
            while True:
                indices = torch.randint(0, N, (batch_size,))
                yield [
                    self.curgs[indices],
                    self.nextgs[indices],
                    self.reward[indices]
                ]

    def insert(self, curgs, nextgs, reward):
        self.curgs = torch.cat((self.curgs, curgs))
        self.nextgs = torch.cat((self.nextgs, nextgs))
        self.reward = torch.cat((self.reward, reward))

    # def insert(self, curgs, nextgs, reward, PID):
    #     self.curgs = torch.cat((self.curgs, curgs))
    #     self.nextgs = torch.cat((self.nextgs, nextgs))
    #     self.reward = torch.cat((self.reward, reward))
    #     self.PID = torch.cat((self.PID, PID))

class ValueModel():

    def reset_scheduler(self, lr):
        def lr_lambda(epoch):
            start_lr = lr
            end_lr = lr/10
            # print(epoch, start_lr, end_lr, end_lr + (start_lr - end_lr) * (1 - epoch / 10000))
            if epoch < 10000:
                return end_lr + (start_lr - end_lr) * (1 - epoch / 10000)
            else:
                return end_lr
        self.scheduler = LambdaLR(self.optimizer, lr_lambda=lr_lambda)


    def __init__(self, gamma, model, gs_shape, player_num, lr):
        self.gamma = gamma
        self.loss_fn = nn.MSELoss()
        self.model = model
        self.device = next(model.parameters()).device
        self.player_num = player_num
        self.cache = dataCACHE(self.device, gs_shape)
        self.gs_shape = gs_shape
        self.lr = lr
        self.optimizer = torch.optim.RMSprop(self.model.parameters(), lr=lr)
        # self.reset_scheduler(self.lr)

    def getVal(self, gs:GameState):
        self.model.eval()
        x = torch.FloatTensor(gs.board.board).to(device=self.device).reshape(1, *self.gs_shape)
        res = self.model(x).squeeze(0)
        self.model.train()
        return res.detach().cpu().numpy()

    def step(self, batch_size, rep=1):
        all_loss = 0
        # cnt = 0
        rep = 10000000
        pre_loss = float('inf')
        # self.reset_scheduler(self.lr)
        batch_size = self.cache.size()
        # for stepid,(curgs, nextgs, reward) in enumerate(self.cache.getBatch(batch_size, random=True)):
        old_model= deepcopy(self.model)
        for stepid,(curgs, nextgs, reward) in enumerate(self.cache.getBatch(batch_size, rep=rep)):
            curV = self.model(curgs)
            nextV = old_model(nextgs)
            # curV = curV.gather(1, PIDs)
            # nextV = nextV.gather(1, PIDs)
            target = (reward + self.gamma * nextV).detach()
            # target = reward + self.gamma * nextV
            loss = self.loss_fn(curV, target)
            self.optimizer.zero_grad()
            loss.backward()
            if loss <= 1e-4:break
            all_loss += loss.detach().cpu().item()
            # cnt += 1
            self.optimizer.step()
            # self.scheduler.step()
            if stepid % 1000 == 999:
                # print(f'loss={loss} lr={self.scheduler.get_last_lr()[0]}')
                print(f'loss={all_loss/1000} lr={self.optimizer.param_groups[0]["lr"]}')
                if abs(pre_loss - all_loss) <= 5e-5 or all_loss > pre_loss:
                    break
                pre_loss = all_loss
                all_loss = 0
            if stepid > 10000:break

        # print(f'Loss: {all_loss/cnt}')


    def store_sample(self, gs:GameState, next_gs: GameState, r:list):
        curgs = torch.FloatTensor(gs.board.board).to(device=self.device)
        nextgs = torch.FloatTensor(next_gs.board.board).to(device=self.device)
        reward = torch.FloatTensor(r).to(device=self.device)
        self.cache.insert(curgs.reshape(1, *curgs.shape), nextgs.reshape(1, *nextgs.shape),
                           reward.reshape(1, *reward.shape))
        
    # def store_sample(self, gs:GameState, next_gs: GameState, r:float, pid:int):
    #     curgs = torch.FloatTensor(gs.board.board).to(device=self.device)
    #     nextgs = torch.FloatTensor(next_gs.board.board).to(device=self.device)
    #     reward = torch.FloatTensor([r]).to(device=self.device)
    #     PID = torch.IntTensor([pid]).to(device=self.device)
    #     self.cache.insert(curgs.reshape(1, *curgs.shape), nextgs.reshape(1, *nextgs.shape),
    #                        reward.reshape(1, *reward.shape), PID.reshape(1, *PID.shape))