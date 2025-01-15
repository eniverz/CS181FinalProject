from typing import Optional

from agents.agent import Agent
from agents.minmaxAgent import minmaxAgent_multiplayer, minmaxAgent_twoplayer
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from game.game import MIRROR_GT, GameState
from service.utils import AgentType, GameType, HttpStatus, Result, get_agent_by_type

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

game = GameState(4, 1, MIRROR_GT)
agent: Optional[Agent] = None
agent2: Optional[Agent] = None


@app.get("/")
def get_root():
    return {"message": "Hello World"}


@app.post("/game/init")
def init_game(
    board_size: int = 4,
    player_num: int = 1,
    game_type: GameType = GameType.PLAYER_VS_PLAYER,
    agent_type: AgentType = AgentType.MINMAX,
    agent2_type: AgentType = AgentType.MINMAX,
):
    global game
    global agent
    game = GameState(board_size, player_num, MIRROR_GT)
    if game_type == GameType.PLAYER_VS_AI:
        agent = minmaxAgent_twoplayer(board_size, player_num, 3)
    elif game_type == GameType.AI_VS_AI:
        agent = get_agent_by_type(agent_type, board_size, player_num, 3)
        agent2 = get_agent_by_type(agent2_type, board_size, player_num, 3)
    pos = []
    for x in range(board_size * 4 + 1):
        for y in range(board_size * 4 + 1):
            if game.board.posInBoard((x, y)):
                pos.append([x, y])
    print(pos)
    return Result.ok(data=pos)


@app.get("/checker/all_position/{player_num}")
def get_all_checker_position(player_num: int):
    global game
    pos = []
    for i in range(player_num):
        pos.extend([[x, y, i] for x, y in game.board.getPlayerCheckers(i)])
    return Result.ok(data=pos)


@app.get("/checker/available_pos")
def get_available_pos(x: int, y: int):
    global game
    if (not game.board.posInBoard((x, y))) or game.board.posEmpty((x, y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({x}, {y}) is not a player checker")
    elif not game.board.board[x][y] == game.curPID + 1:
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({x}, {y}) does not belong to player {game.curPID}")
    return Result.ok(data=game.board.nextSteps((x, y)))


@app.post("/checker/move")
def move_checker(start_x: int, start_y: int, end_x: int, end_y: int):
    global game
    if (not game.board.posInBoard((start_x, start_y))) or (not game.board.posInBoard((end_x, end_y))):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) or ({end_x}, {end_y}) is not in board")
    if game.board.posEmpty((start_x, start_y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) is empty")
    if game.board.posNotEmpty((end_x, end_y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({end_x}, {end_y}) is not empty")
    if game.board.board[start_x][start_y] != game.curPID + 1:
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) does not belong to player {game.curPID}")
    is_win = game.moveChecker((start_x, start_y), (end_x, end_y))
    return Result.ok(data={"playerID": game.curPID, "isWin": is_win})


@app.get("/agent/move")
def move_agent():
    global game
    global agent
    if agent is None:
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail="Agent is not initialized")
    agent.set_GameState(game)
    game = agent.get_next_gs()
    is_win = game.board.checkWin(1)
    return Result.ok(data={"movement": game.movement, "isWin": is_win})

@app.get("/agent2/move")
def move_agent2():
    global game
    global agent2
    if agent2 is None:
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail="Agent is not initialized")
    agent2.set_GameState(game)
    game = agent2.get_next_gs()
    is_win = game.board.checkWin(0)
    return Result.ok(data={"movement": game.movement, "isWin": is_win})
