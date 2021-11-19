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

    def get_win_ratio(self):
        return round(self.victory / (self.victory + self.defeat), 2)

    def __str__(self):
        return f"{self.name} by {self.user_id}: {self.get_win_ratio() * 100}% victories "
