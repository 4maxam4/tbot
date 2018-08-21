import abc
import typing
from tbot import machine
from tbot.machine import channel
from . import board

B = typing.TypeVar("B", bound=board.Board)


class BoardMachine(machine.Machine, typing.Generic[B]):

    @abc.abstractmethod
    def connect(self) -> channel.Channel:
        pass

    def __init__(self, board: B) -> None:
        super().__init__()
        self.board = board

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.board!r})"
