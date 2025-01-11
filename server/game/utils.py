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

EMPTY_BOX = -1

DX = [-1, -1, 0, 0, 1, 1]
DY = [0, 1, -1, 1, -1, 0]
DIR = [(DX[i], DY[i]) for i in range(len(DX))]


ADJACENT_GT = 0
MIRROR_GT = 1

