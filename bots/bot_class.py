from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Bot:
    bot_id: int | None
    name: str | None
    user_id: int
    code: str
    victory: int = 0
    defeat: int = 0
    username: str | None = None

    def get_win_ratio(self):
        return (
            0
            if not (self.victory + self.defeat)
            else round(self.victory / (self.victory + self.defeat), 2)
        )

    def __str__(self):
        return f"{self.name:<15} |  {self.bot_id:^3d}  | {self.username:<15} | {self.get_win_ratio() * 100:2.2f}%"
