#! usr/env/bin python3
# nevclient.model.Enums.NISCOPEChannelVerticalRange.py

# extern modules
from enum import Enum

class NISCOPEChannelVerticalRange(Enum):
    """
    The NISCOPEChannelVerticalRange enum represents the different types of vertical range for a NISCOPE device.
    See old client code attribute named "range_options" inside the "niscopeChannelBox" class in the "nevcl_psa.py" file
    """
    ONE = 1.0
    FIVE = 5.0
    
    def __str__(self) -> str:
        if self.value == 1.0:
            return "±1.0 (V)"
        elif self.value == 5.0:
            return "±5.0 (V)"
        
    @classmethod
    def from_string(cls, s: str):
        for member in cls:
            if str(member) == s:
                return member
        raise ValueError(f"'{s}' is not a valid string for {cls.__name__}")
                         
    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
    @classmethod
    def get_all_members(cls):
        return [member for member in cls]