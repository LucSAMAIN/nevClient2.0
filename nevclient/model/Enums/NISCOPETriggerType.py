#! usr/env/bin python3
# nevclient.model.Enums.NISCOPETriggerType.py

# extern modules
from enum import Enum


class NISCOPETriggerType(Enum):
    IMMEDIATE = "IMMEDIATE"
    EDGE = "EDGE"

    def __str__(self) -> str:  # noqa: D401 – single‑line docstring is fine
        return self.value
    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")
