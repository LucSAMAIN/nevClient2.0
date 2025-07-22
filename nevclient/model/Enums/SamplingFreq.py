#! usr/env/bin python3
# nevclient.model.Enums.SamplingFreq.py

# extern modules
from enum import Enum

class SamplingFreq(Enum):
    """
    The SamplingFreq enum is used to define the different sampling
    frequencies available to the user.
    All the possibilities are stored in the "sampling (Hz)" combobox
    inside the sweeperPanel. 
    """
    K50 = 5e4
    K100 = 1e5
    K150 = 1.5e5

    def __str__(self):
        return f"{self.name[1:]}K (Hz)"

    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
    @classmethod
    def get_all_members(cls):
        return [member for member in cls]

    @classmethod
    def from_string(cls, s: str):
        """
        Converts a string representation (e.g., "50K (Hz)") back to a SamplingFreq member.
        """
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")