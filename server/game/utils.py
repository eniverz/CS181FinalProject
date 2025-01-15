import numpy as np

class Node:
    def __init__(self, value, nxt=None):
        self.value = value
        self.nxt = nxt


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def empty(self):
        return self.front is None

    def push(self, value):
        new_node = Node(value)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.nxt = new_node
            self.rear = new_node
        assert not self.empty()

    def pop(self):
        if self.empty():
            raise IndexError("Pop from empty queue")
        result = self.front.value
        self.front = self.front.nxt
        if self.front is None:
            self.rear = None
        return result

EMPTY_BOX = 0

DX = [-1, -1, 0, 0, 1, 1]
DY = [0, 1, -1, 1, -1, 0]
DIR = [(DX[i], DY[i]) for i in range(len(DX))]


ADJACENT_GT = 0
MIRROR_GT = 1


def MahattanDIS(pos1, pos2):
    if pos1[0] <= pos2[0] and pos1[1] <= pos2[1]:
        return pos2[0] - pos1[0] + pos2[1] - pos1[1]
    if pos1[0] >= pos2[0] and pos1[1] >= pos2[1]:
        return pos1[0] - pos2[0] + pos1[1] - pos2[1]
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

def EuclideanPos(pos):
    return [pos[0]+0.5*pos[1], (3**0.5)/2*pos[1]]

def EuclideanDIS(pos1, pos2):
    epos1 = EuclideanPos(pos1)
    epos2 = EuclideanPos(pos2)
    return ((epos1[0]-epos2[0])**2+(epos1[1]-epos2[1])**2)**0.5

def softmax(input):
    input = np.copy(input).astype('float64')
    input -= np.max(input, axis=-1, keepdims=True)
    exps = np.exp(input)
    return exps / np.sum(exps, axis=-1, keepdims=True)


def stress_message(message, extra_newline=False):
    print('{2}{0}\n{1}\n{0}{2}'.format('='*len(message), message, '\n' if extra_newline else ''))


BOARD_HIST_MOVES = 3
def to_model_input(gs):
    # initialise the model input
    model_input = np.zeros((gs.board.len, gs.board.len, BOARD_HIST_MOVES * 2 + 1)) # may change dtype afterwards
    # get np array board
    new_board = gs.board.board_np
    # get history moves
    hist_moves = gs.board.hist_moves
    # get opponent player
    opPID = 1 - gs.curPID

    # firstly, construct the current state layers
    op_layer = np.copy(new_board[:, :, 0])
    cur_layer = np.copy(new_board[:, :, 0])
    # construct layer for current player
    np.putmask(cur_layer, cur_layer != gs.curPID, 0)
    for checker_id, checker_pos in enumerate(gs.board.getPlayerCheckers(gs.curPID)):
        cur_layer[checker_pos[0], checker_pos[1]] = checker_id + 1
    # construct layer for opponent player
    np.putmask(op_layer, op_layer != opPID, 0)
    for checker_id, checker_pos in enumerate(gs.board.getPlayerCheckers(opPID)):
        op_layer[checker_pos[0], checker_pos[1]] = checker_id + 1

    model_input[:, :, 0] = np.copy(cur_layer)
    model_input[:, :, 1] = np.copy(op_layer)

    # construct the latter layers
    moved_player = opPID
    hist_index = len(hist_moves) - 1
    for channel in range(1, BOARD_HIST_MOVES):
        if not np.any(new_board[:, :, channel]): # timestep < 0
            break
        move = hist_moves[hist_index]
        orig_pos = move[0]
        dest_pos = move[1]

        if moved_player == gs.curPID:
            value = cur_layer[dest_pos]
            cur_layer[dest_pos] = cur_layer[orig_pos]
            cur_layer[orig_pos] = value
        else:
            value = op_layer[dest_pos]
            op_layer[dest_pos] = op_layer[orig_pos]
            op_layer[orig_pos] = value

        hist_index -= 1
        moved_player = 1 - moved_player
        model_input[:, :, channel * 2] = np.copy(cur_layer)
        model_input[:, :, channel * 2 + 1] = np.copy(op_layer)

    if gs.curPID == 1: # player ID=1 to play
        model_input[:, :, BOARD_HIST_MOVES * 2] = np.ones((gs.board.len, gs.board.len))

    return model_input