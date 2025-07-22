#! usr/env/bin python3
# nevclient.model.Enums.NISCOPETriggerSlope.py

# extern modules
from enum import Enum

class NISCOPETriggerSlope(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

    def __str__(self) -> str:
        return self.value
    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")