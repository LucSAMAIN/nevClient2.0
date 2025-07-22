#! usr/env/bin python3
# nevclient.model.Enums.NISCOPETriggerCoupling.py

# extern modules
from enum import Enum

class NISCOPETriggerCoupling(Enum):
    AC = "AC"
    DC = "DC"
    HF_REJECT = "HF_REJECT"
    LF_REJECT = "LF_REJECT"
    AC_PULS_HF_REJECT = "AC_PULS_HF_REJECT"

    def __str__(self) -> str:
        return self.value
    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")