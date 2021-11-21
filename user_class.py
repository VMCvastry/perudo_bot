from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    name: str | None = None

    def get_name(self):
        if not self.name:
            return "Anon"
        return self.name
