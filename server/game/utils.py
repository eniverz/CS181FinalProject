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
