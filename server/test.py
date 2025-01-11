import torch
from torch import nn
from agents.valueModel import ValueNN

x = torch.randn(1, 17, 17)
t = ValueNN((17, 17), 2)
print(t(x).shape)