#! usr/env/bin python3
# nevclient.model.Enums.NISCOPEChannelVerticalCoupling.py

# extern modules
from enum import Enum

class NISCOPEChannelVerticalCoupling(Enum):
    """
    The NISCOPEChannelVerticalCoupling enum represents the coupling types for a channel in NISCOPE.
    
    Notes
    -----
    I defined it based on the 'nev_niscope.c' file from the NEV backend server project.
    I especially use it in the `ParseNSUCHAN` method to parse the channel coupling information.
    """
    AC = "AC"
    DC = "DC"
    GND = "GND"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")
    
    @classmethod
    def get_all_members(cls):
        return [member for member in cls]