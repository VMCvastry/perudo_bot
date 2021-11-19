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
