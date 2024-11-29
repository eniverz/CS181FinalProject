from copy import deepcopy
from game.utils import Queue

EMPTY_BOX = -1

DX = [-1, -1, 0, 0, 1, 1]
DY = [0, 1, -1, 1, -1, 0]
DIR = [(DX[i], DY[i]) for i in range(len(DX))]

class Board:
    def __init__(self, board_size, player_num):
        '''
        each player has 1+2+...+board_size checkers
        the board is made up of one upward triangle and one downward triangle
        '''
        assert player_num in [1,2,3,6], "player_num should be 1,2,3 or 6"
        self.len = board_size * 4 + 1
        self.N = board_size
        self.player_num = player_num
        self.board = [[EMPTY_BOX for i in range(self.len)] for j in range(self.len)]
        self.checkerlist = [[] for player in range(player_num)]
        self.winstate_pos = [set() for player in range(player_num)]
        triangle_pos_list = [[] for triagle_id in range(6)] # the positions of the six triangles

        triangle_id = 0
        for i in range(board_size):
            for j in range(i+1):
                pos = (2*board_size+1+i, board_size-1-j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 1
        for i in range(board_size):
            for j in range(i+1):
                pos = (2*board_size-1-i, board_size+j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 2
        for i in range(board_size):
            for j in range(i+1):
                pos = (i, 3*board_size-j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 3
        for i in range(board_size):
            for j in range(i+1):
                pos = (board_size+j, 3*board_size+1+i)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 4
        for i in range(board_size):
            for j in range(i+1):
                pos = (2*board_size+1+i, 3*board_size-j)
                triangle_pos_list[triangle_id].append(pos)
        
        triangle_id = 5
        for i in range(board_size):
            for j in range(i+1):
                pos = (4*board_size-i, board_size+j)
                triangle_pos_list[triangle_id].append(pos)

        if player_num == 1:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.winstate_pos[0] = set(triangle_pos_list[3])

        elif player_num == 2:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.checkerlist[1] = deepcopy(triangle_pos_list[3])
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[0])

        elif player_num == 3:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.checkerlist[1] = deepcopy(triangle_pos_list[2])
            self.checkerlist[2] = deepcopy(triangle_pos_list[4])
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[5])
            self.winstate_pos[2] = set(triangle_pos_list[1])

        elif player_num == 6:
            self.checkerlist = deepcopy(triangle_pos_list)
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[4])
            self.winstate_pos[2] = set(triangle_pos_list[5])
            self.winstate_pos[3] = set(triangle_pos_list[0])
            self.winstate_pos[4] = set(triangle_pos_list[1])
            self.winstate_pos[5] = set(triangle_pos_list[2])

        for player_id in range(player_num):
            for x,y in self.checkerlist[player_id]:
                self.board[x][y] = player_id

    def posInBoard(self, pos):
        '''
        check if pos is in the board
        '''
        # pos in upside-triangle
        if pos[1] >= self.N and pos[0] >= self.N and pos[0]+pos[1] <= 5*self.N:
            return True
        # pos in downside-triangle
        if pos[1] <= 3*self.N and pos[0] <= 3*self.N and pos[0]+pos[1] >= 3*self.N:
            return True
        return False
    
    def posEmpty(self, pos):
        '''
        check if pos is in the board and empty
        '''
        return self.posInBoard(pos) and self.board[pos[0]][pos[1]] == EMPTY_BOX
    
    def posNotEmpty(self, pos):
        '''
        check if pos is in the board and not empty
        '''
        return self.posInBoard(pos) and self.board[pos[0]][pos[1]] != EMPTY_BOX
    
    def getPlayerCheckers(self, player_id):
        return self.checkerlist[player_id]

    def moveChecker(self, start_pos, end_pos, player_id):
        '''
        move the checker that belongs to player_id from start to end
        return the new board after the movement
        '''
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
        '''
        get the next steps of certain position
        return the list of new positions
        '''
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
        # print(pos, possibleList)
        return possibleList

    def checkWin(self, player_id):
        '''
        check whether player_id has won
        '''
        return len(set(self.checkerlist[player_id]) & self.winstate_pos[player_id]) == len(self.winstate_pos[player_id])

    def checkLose(self, player_id):
        '''
        check whether player_id loses by having no available move
        '''
        assert True, 'This function should not be called, since checking len(nextGameStates)==0 \
                      when calling nextGameState should be a better approach.'
        for pos in self.checkerlist[player_id]:
            if len(self.nextSteps(pos)) > 0:
                return True
        return False


    def debugPlayerCheckers(self):
        for player_id in range(self.player_num):
            print(f"player {player_id}:")
            for pos in self.checkerlist[player_id]:
                print(pos)
            print()

class GameState:
    def __init__(self, board_size:int, player_num:int):
        '''
        gamestate is made up of a board and the currnet player id
        '''
        self.board = Board(board_size, player_num)
        self.curPID = 0
    
    def nextGameStates(self):
        '''
        get the list of possible next game states
        '''
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

    def checkWin(self):
        return self.board.checkWin(self.curPID)