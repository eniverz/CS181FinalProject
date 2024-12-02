from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.middleware.cors import CORSMiddleware

from game.game import GameState
from service.utils import HttpStatus, Result

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

game = GameState(4, 1)


@app.get("/")
def get_root():
    return {"message": "Hello World"}


@app.post("/game/init")
def init_game(board_size: int = 4, player_num: int = 1):
    global game
    game = GameState(board_size, player_num)
    return Result.ok()


@app.get("/checker/all_position/{player_num}")
def get_all_checker_position(player_num: int):
    pos = []
    for i in range(player_num):
        pos.extend([[x, y, i] for x, y in game.board.getPlayerCheckers(i)])
    return Result.ok(data=pos)


@app.get("/checker/available_pos")
def get_available_pos(x: int, y: int):
    if (not game.board.posInBoard((x, y))) or game.board.posEmpty((x, y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({x}, {y}) is not a player checker")
    return Result.ok(data=game.board.nextSteps((x, y)))


@app.post("/checker/move")
def move_checker(start_x: int, start_y: int, end_x: int, end_y: int, player_id: int):
    if (not game.board.posInBoard((start_x, start_y))) or (not game.board.posInBoard((end_x, end_y))):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) or ({end_x}, {end_y}) is not in board")
    if game.board.posEmpty((start_x, start_y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) is empty")
    if game.board.posNotEmpty((end_x, end_y)):
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({end_x}, {end_y}) is not empty")
    if game.board.board[start_x][start_y] != player_id:
        raise HTTPException(status_code=HttpStatus.HTTP_400_BAD_REQUEST[0], detail=f"Position ({start_x}, {start_y}) does not belong to player {player_id}")
    new_game = game.board.moveChecker((start_x, start_y), (end_x, end_y), player_id)
    game.board = new_game
    return Result.ok(data=new_game)
