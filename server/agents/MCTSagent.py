from agents.agent import Agent
from game.game import ADJACENT_GT, MIRROR_GT, Board, GameState
import random
import math
from game.utils import *
from agents.MCTSmodel import *

class Node:
        def __init__(self, gs):
            self.edges = []
            self.gs = gs
            self.pi = np.zeros(gs.board.len * gs.board.len * gs.board.len, dtype='float64')
        
        def isLeaf(self):
            return len(self.edges) == 0
        
class Edge:
    def __init__(self, prior, gs, fromNode, toNode):
        self.fromPos = gs.movement[0]
        self.toPos = gs.movement[1]
        self.fromNode = fromNode
        self.toNode = toNode
        
        self.state = {
            'N': 0,
            'W': 0,
            'Q': 0,
            'P': prior
        }

class MCTS:
    def __init__(self, root, model, Cpuct=3.5):
        self.root = root
        self.Cpuct = Cpuct
        self.model = model
        
    def Selection(self):
        curNode = self.root
        theWay = []
        while not curNode.isLeaf():
            maxUCB = float('-inf')
            chosen_edges = []
            N_sum = sum([edge.state['N'] for edge in curNode.edges])
            for edge in curNode.edges:
                UCB = edge.state['Q'] + self.Cpuct * math.sqrt(N_sum) * edge.state['P'] / (1 + edge.state['N'])
                if UCB > maxUCB:
                    maxUCB = UCB
                    chosen_edges = [edge]
                elif math.fabs(UCB - maxUCB) < 1e-5:
                    chosen_edges.append(edge)
            
            anEdge = random.choice(chosen_edges)
            theWay.append(anEdge)
            curNode = anEdge.toNode
        return curNode, theWay
    
    def Expand_w_Backup(self, leafNode, theWay):
        isWin = leafNode.gs.checkWin()
        if isWin:
            for edge in theWay:
                direction = -1 if edge.fromNode.gs.curPID == leafNode.gs.curPID else 1
                edge.state['N'] += 1
                edge.state['W'] += direction
                edge.state['Q'] = edge.state['W'] / float(edge.state['N'])
            return
        
        # pEval, vEval = self.model.predict(to_model_input(leafNode.gs))
        
        baseR = float('-inf')
        for nextGS in leafNode.gs.nextGameStates():
            fromPos = nextGS.movement[0]
            toPos = nextGS.movement[1]
            nxtPID = nextGS.curPID
            # checkerID = -1
            # for id, pos in enumerate(nextGS.board.getPlayerCheckers(leafNode.gs.curPID)):
            #     if pos == fromPos:
            #         checkerID = id
            #         break
            # priorIndex = checkerID * nextGS.board.len * nextGS.board.len + fromPos[0] * nextGS.board.len + fromPos[1]
            pid = leafNode.gs.curPID
            r = MahattanDIS(leafNode.gs.board.corners[pid], fromPos) - MahattanDIS(leafNode.gs.board.corners[pid], toPos)
            if (r < 0):
                r *= 0.01
            if nextGS.checkWin():
                r += 15
            if r > baseR:
                baseR = r
                newNode = Node(nextGS)
                newEdge = Edge(1, nextGS, leafNode, newNode)
                leafNode.edges.append(newEdge)
            # if(r > 0) :
            #     newNode = Node(nextGS)
            #     newEdge = Edge(1, nextGS, leafNode, newNode)
            #     leafNode.edges.append(newEdge)
            # else:
            #     if(random.random() < 0.2):
            #         newNode = Node(nextGS)
            #         newEdge = Edge(1, nextGS, leafNode, newNode)
            #         leafNode.edges.append(newEdge)
            # newNode = Node(nextGS)
            # newEdge = Edge(pEval[priorIndex], nextGS, leafNode, newNode)
            # leafNode.edges.append(newEdge)
            
        for edge in theWay:
            direction = 1 if edge.fromNode.gs.curPID == leafNode.gs.curPID else -1
            edge.state['N'] += 1
            edge.state['W'] += direction #* vEval
            edge.state['Q'] = edge.state['W'] / float(edge.state['N'])
            
        
    def search(self):
        for _ in range(175):
            leaf, way = self.Selection()
            self.Expand_w_Backup(leaf, way)
            
        maxN = float('-inf')   
        chosenEdges = []
        
        for edge in self.root.edges:
            prob = edge.state['N']
            checkerID = -1
            for id, pos in enumerate(self.root.gs.board.getPlayerCheckers(self.root.gs.curPID)):
                if pos == edge.fromPos:
                    checkerID = id
                    break
            netIndex = checkerID * self.root.gs.board.len * self.root.gs.board.len + edge.toPos[0] * self.root.gs.board.len + edge.toPos[1]
            self.root.pi[netIndex] = prob
        
        self.root.pi /=np.sum(self.root.pi)
        
        sampleIndex = np.random.choice(np.arange(len(self.root.pi)), p=self.root.pi)
        for edge in self.root.edges:
            checkerID = -1
            for id, pos in enumerate(self.root.gs.board.getPlayerCheckers(self.root.gs.curPID)):
                if pos == edge.fromPos:
                    checkerID = id
                    break
            netIndex = checkerID * self.root.gs.board.len * self.root.gs.board.len + edge.toPos[0] * self.root.gs.board.len + edge.toPos[1]
            if netIndex == sampleIndex:
                return self.root.pi, edge
        
        
        
    

class MCTSagent_twoplayer(Agent):
    def __init__(self, board_size: int, player_num: int, max_depth: int, game_type: int = ADJACENT_GT):
        super().__init__(board_size, player_num, game_type)
        self.max_depth = max_depth
    
    def get_next_gs(self):
        node = Node(self.get_GameState())
        model = ResidualCNN(self.get_GameState())
        tree = MCTS(node, model)
        pi, edge = tree.search()
        # print(edge.toNode.gs.movement)
        return edge.toNode.gs
    

def MCTSagent(board_size: int, player_num: int, max_depth: int, game_type: int = ADJACENT_GT):
    if player_num == 2:
        return MCTSagent_twoplayer(board_size, player_num, max_depth, game_type)
    return None