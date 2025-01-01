from enum import Enum, unique
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from typing_extensions import Tuple


@unique
class HttpStatus(Enum):
    HTTP_200_OK = (200, "success")
    HTTP_400_BAD_REQUEST = (400, "Bad Request!")
    HTTP_401_UNAUTHORIZED = (401, "You have no authentication to access!")
    HTTP_403_FORBIDDEN = (403, "Your authentication is not allowed to access!")
    HTTP_404_NOTFOUND = (404, "Resource Not Found!")
    HTTP_500_INTERNAL_SERVER_ERROR = (500, "the server has some error!")
    HTTP_409_CONFLICT = (409, "Data Conflict!")
    HTTP_422_UNPROCESSABLE_ENTITY = (422, "Unprocessable Entity!")
    _value_: int
    _data_: Tuple[int, str]

    def __new__(cls, *args):
        enum_member = object.__new__(cls)
        enum_member._value_ = args[0]  # Set the enum value
        enum_member._data_ = args  # Store the entire tuple as custom data
        return enum_member

    def __getitem__(self, key):
        return self._data_[key]


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T]

    @staticmethod
    def ok(*, data: Optional[T] = None, code=HttpStatus.HTTP_200_OK[0], msg=HttpStatus.HTTP_200_OK[1]):
        return Result[T](code=code, data=data, msg=msg).to_dict()

    @staticmethod
    def error(*, data: Optional[T] = None, code: int, msg: str, status: HttpStatus):
        result = Result(data=data)
        if status is not None:
            result.code = status[0]
            result.msg = status[1]
        if code is not None:
            result.code = code
        if msg is not None:
            result.msg = msg
        return result.to_dict()

    def to_dict(self):
        return {"code": self.code, "msg": self.msg, "data": self.data}

@unique
class GameType(int, Enum):
    PLAYER_VS_PLAYER = 1
    PLAYER_VS_AI = 2
    AI_VS_AI = 3
