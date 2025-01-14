import torch.nn as nn
import torch


m = nn.Conv2d(3, 32, 7,2,3)

x = torch.zeros((3, 17, 17))
print(m(x).shape)
x = torch.zeros((3, 20, 17))
print(m(x).shape)
x = torch.zeros((3, 18, 18))
print(m(x).shape)