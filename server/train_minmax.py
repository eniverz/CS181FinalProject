from agents.minmaxVEAgent import train_minmaxFA, FEATURE_CNT
import numpy as np

board_size = 3
max_depth = 2
# w = np.array([0.45,0.25,0.0],dtype=np.float32) -> [0.41,0.20,-0.15]
# w = np.array([1,0.3,0.3],dtype=np.float32)  -> [1.06,0.47, -1.25]
# w = np.array([0.5,0.5,0.5],dtype=np.float32)
w = np.array([0.9,0.2,0.4],dtype=np.float32)
assert w.shape[0] == FEATURE_CNT
agent, w = train_minmaxFA(board_size, max_depth, w)
print(w)
