#! usr/env/bin python3
# nevclient.model.Enums.SweepDirection.py

# extern modules
from enum import Enum

class SweepDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"

    def __str__(self):
        if self.value == "UP":
            return "↑"
        else:
            return "↓"
    
    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
    @classmethod
    def get_all_members(cls):
        return [member for member in cls]

    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")