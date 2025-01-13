from agents.minmaxVEAgent import train_minmaxFA, FEATURE_CNT
import numpy as np

board_size = 3
max_depth = 2
# w = np.array([0.45,0.25,0.0],dtype=np.float32) -> [0.41,0.20,-0.15]
# w = np.array([1,0.3,0.3],dtype=np.float32)  -> [1.06,0.47, -1.25]
# w = np.array([0.5,0.5,0.5],dtype=np.float32) -> [0.51, 0.36, -0.27]
# w = np.array([0.9,0.2,0.4],dtype=np.float32) -> [0.97, 0.39, -1.11]
# w = np.array([0.3,1.0,0.3],dtype=np.float32) #-> [0.35, 0.72, -0.41]
# w = np.array([0.3,0.3,1.0],dtype=np.float32) #-> [0.30 0.24 0.50]
# w = np.array([0.3,0.7,0.7],dtype=np.float32) #-> [0.40, 0.59, -0.27]
# w = np.array([0.7,0.7,0.3],dtype=np.float32) #-> [0.75, 0.61, -0.12]
# w = np.array([0.7,0.3,0.7],dtype=np.float32) #-> [0.73, 0.37, -0.3]
# w = np.array([1.0,1.0,1.0],dtype=np.float32) #-> []
# w = np.array([0.4,0.5,0.6],dtype=np.float32) #-> []
w = np.array([0.23078917 ,0.41254208 ,0.31288201],dtype=np.float32) #-> []
assert w.shape[0] == FEATURE_CNT
agent, w = train_minmaxFA(board_size, max_depth, w)
print(w)
