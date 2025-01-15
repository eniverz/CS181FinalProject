import matplotlib.pyplot as plt
from copy import deepcopy
from typing import Optional, Tuple

# Set up the grid size and style
fig, ax = plt.subplots(figsize=(10, 10))

# Create the grid
ax.set_xticks(range(0, 13, 1))
ax.set_yticks(range(0, 13, 1))
ax.set_xlim(-1, 13)
ax.set_ylim(-1, 13)
ax.grid(which='both', color='lightblue', linestyle='-', linewidth=0.5)

class Board:
    def __init__(self, board_size, player_num, game_type):
        self.len = board_size * 4 + 1
        self.board = [[0 for i in range(self.len)] for j in range(self.len)]
        self.checkerlist = [[] for player in range(player_num)]
        self.winstate_pos = [set() for player in range(player_num)]
        triangle_pos_list = [[] for triagle_id in range(6)]  # the positions of the six triangles
        corners = [(3*board_size, 0), (board_size, board_size), (0, 3*board_size), (board_size, 4*board_size), (3*board_size, 3*board_size), (4*board_size, board_size)]
        self.corners = [0,0,0,0,0,0]
        triangle_id = 0
        for i in range(board_size):
            for j in range(i + 1):
                pos = (2 * board_size + 1 + i, board_size - 1 - j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 1
        for i in range(board_size):
            for j in range(i + 1):
                pos = (2 * board_size - 1 - i, board_size + j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 2
        for i in range(board_size):
            for j in range(i + 1):
                pos = (i, 3 * board_size - j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 3
        for i in range(board_size):
            for j in range(i + 1):
                pos = (2 * board_size - 1 - i, 3 * board_size + 1 + j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 4
        for i in range(board_size):
            for j in range(i + 1):
                pos = (2 * board_size + 1 + i, 3 * board_size - j)
                triangle_pos_list[triangle_id].append(pos)

        triangle_id = 5
        for i in range(board_size):
            for j in range(i + 1):
                pos = (4 * board_size - i, board_size + j)
                triangle_pos_list[triangle_id].append(pos)


        if player_num == 1:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.corners[0] = corners[3]

        elif player_num == 2:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.checkerlist[1] = deepcopy(triangle_pos_list[3])
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[0])
            self.corners[0] = corners[3]
            self.corners[1] = corners[0]

        elif player_num == 3:
            self.checkerlist[0] = deepcopy(triangle_pos_list[0])
            self.checkerlist[1] = deepcopy(triangle_pos_list[2])
            self.checkerlist[2] = deepcopy(triangle_pos_list[4])
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[5])
            self.winstate_pos[2] = set(triangle_pos_list[1])
            self.corners[0] = corners[3]
            self.corners[1] = corners[5]
            self.corners[2] = corners[1]

        elif player_num == 6:
            self.checkerlist = deepcopy(triangle_pos_list)
            self.winstate_pos[0] = set(triangle_pos_list[3])
            self.winstate_pos[1] = set(triangle_pos_list[4])
            self.winstate_pos[2] = set(triangle_pos_list[5])
            self.winstate_pos[3] = set(triangle_pos_list[0])
            self.winstate_pos[4] = set(triangle_pos_list[1])
            self.winstate_pos[5] = set(triangle_pos_list[2])
            self.corners[0] = corners[3]
            self.corners[1] = corners[4]
            self.corners[2] = corners[5]
            self.corners[3] = corners[0]
            self.corners[4] = corners[1]
            self.corners[5] = corners[2]

        for player_id in range(player_num):
            for x, y in self.checkerlist[player_id]:
                self.board[x][y] = player_id+1
        self.triangle_pos_list = triangle_pos_list

t = Board(3, 6, None)
# Draw custom annotations and points
points = {}

for player_id, checkerlist in enumerate(t.checkerlist):
    for checker in checkerlist:
        x, y = checker
        points[(x, y)] = player_id + 1

# Plot the points for each cluster and label them
for (x_vals, y_vals), label in points.items():
    ax.scatter(x_vals, y_vals, color='white', edgecolor='black', s=100, zorder=5)
    ax.text(x_vals, y_vals, str(label), color='red', fontsize=12, zorder=10)

# Customize axes
ax.set_xlabel("X-axis", fontsize=12)
ax.set_ylabel("Y-axis", fontsize=12)
ax.set_title("Standardized Grid Diagram", fontsize=16)
ax.set_aspect('equal')

# Show the plot
plt.savefig("./standardized_grid_diagram.png")
plt.show()
