from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.middleware.cors import CORSMiddleware

from game.game import GameState
from service.utils import Result

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

game = GameState(4, 2)

@app.get("/")
def get_root():
    return {"message": "Hello World"}

@app.get("/board/all_position")
def get_all_board_position():
    position = [[i, j] for i in range(17) for j in range(17) if game.board.posInBoard((i, j))]
    return Result.ok(data=position)
