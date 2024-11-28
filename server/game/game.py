from copy import deepcopy
from game.utils import Queue

EMPTY_BOX = -1

DX = [-1, -1, 0, 0, 1, 1]
DY = [0, 1, -1, 1, -1, 0]
DIR = [(DX[i], DY[i]) for i in range(len(DX))]

class Board:
    def __init__(self, board_size, player_num):
        assert player_num in [1,2,3,6], "player_num should be 1,2,3 or 6"
        self.len = board_size * 4 + 1
        self.N = board_size
        self.player_num = player_num
        self.board = [[EMPTY_BOX for i in range(self.len)] for j in range(self.len)]
        self.checkerlist = [[] for player in range(player_num)]
        if player_num >= 1:
            player_id = 0
            for i in range(board_size):
                for j in range(i+1):
                    pos = (3*board_size-j, i)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)
        if player_num == 2 or player_num == 6:
            player_id = 1 if player_num == 2 else 3
            for i in range(board_size):
                for j in range(i+1):
                    pos = (board_size+j, 3*board_size+1+i)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)
        if player_num == 3 or player_num == 6:
            player_id = 1 if player_num == 3 else 2
            for i in range(board_size):
                for j in range(i+1):
                    pos = (i, 3*board_size-j)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)
            player_id = 2 if player_num == 3 else 4
            for i in range(board_size):
                for j in range(i+1):
                    pos = (2*board_size+1+i, 3*board_size-j)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)
        
        if player_num == 6:
            player_id = 1
            for i in range(board_size):
                for j in range(i+1):
                    pos = (2*board_size-1-i, board_size+j)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)
            player_id = 5
            for i in range(board_size):
                for j in range(i+1):
                    pos = (4*board_size-i, board_size+j)
                    self.board[pos[0]][pos[1]] = player_id
                    self.checkerlist[player_id].append(pos)

    def posInBoard(self, pos):
        # pos in upside-triangle
        if pos[1] >= self.N and pos[0] >= self.N and pos[0]+pos[1] <= 5*self.N:
            return True
        # pos in downside-triangle
        if pos[1] <= 3*self.N and pos[0] <= 3*self.N and pos[0]+pos[1] >= 3*self.N:
            return True
        return False
    
    def posEmpty(self, pos):
        return self.posInBoard(pos) and self.board[pos[0]][pos[1]] == EMPTY_BOX
    
    def posNotEmpty(self, pos):
        return self.posInBoard(pos) and self.board[pos[0]][pos[1]] != EMPTY_BOX
    

    def getPlayerCheckers(self, player_id):
        return self.checkerlist[player_id]

    def moveChecker(self, start_pos, end_pos, player_id):
        assert self.posInBoard(start_pos), f'Start position {start_pos} not in board'
        assert self.posInBoard(end_pos), f'End position {end_pos} not in board'
        assert self.board[start_pos[0]][start_pos[1]] == player_id, f'Start position does not belong to {player_id}: {start_pos}->{end_pos}'
        assert self.board[end_pos[0]][end_pos[1]] == EMPTY_BOX, f'End position is not empty: {start_pos}->{end_pos}'


        newBoard = deepcopy(self)
        newBoard.board[start_pos[0]][start_pos[1]] = EMPTY_BOX
        newBoard.board[end_pos[0]][end_pos[1]] = player_id
        newBoard.checkerlist[player_id].remove(start_pos)
        newBoard.checkerlist[player_id].append(end_pos)
        return newBoard

    def nextSteps(self, pos):
        possibleList = []

        # check neighbor
        for dx, dy in DIR:
            npos = (pos[0]+dx, pos[1]+dy)
            if self.posEmpty(npos):
                possibleList.append(npos)

        # check jump
        vis = set()
        q = Queue()
        q.push(pos)
        while not q.empty():
            cur = q.pop()
            for dx, dy in DIR:
                midpos = (cur[0]+dx, cur[1]+dy)
                if self.posNotEmpty(midpos):
                    npos = (midpos[0]+dx, midpos[1]+dy)
                    if npos not in vis:
                        if self.posEmpty(npos):
                            possibleList.append(npos)
                            q.push(npos)
                            vis.add(npos)
        print(pos, possibleList)
        return possibleList

    def debugPlayerCheckers(self):
        for player_id in range(self.player_num):
            print(f"player {player_id}:")
            for pos in self.checkerlist[player_id]:
                print(pos)
            print()

class GameState:
    def __init__(self, board_size:int, player_num:int):
        self.board = Board(board_size, player_num)
        self.curPID = 0
    
    def nextGameStates(self):
        b = self.board
        curPID = self.curPID
        nxtPID = (self.curPID + 1) % b.player_num
        newstates = []
        for pos in b.getPlayerCheckers(curPID):
            nxtPosList = b.nextSteps(pos)
            for nxtpos in nxtPosList:
                newGameState = GameState(b.N, b.player_num)
                newGameState.curPID = nxtPID
                newGameState.board = b.moveChecker(pos, nxtpos, curPID)
                newstates.append(newGameState)
        return newstates