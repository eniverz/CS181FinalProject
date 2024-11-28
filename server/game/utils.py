class Node:
    def __init__(self, value, nxt):
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

    def pop(self):
        if self.empty():
            raise IndexError("Pop from empty queue")
        result = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return result
