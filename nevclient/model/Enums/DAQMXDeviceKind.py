#! usr/env/bin python3
# nevclient.model.Enums.DAQMXDeviceKind.py

# extern modules
from enum import Enum

class DAQMXDeviceKind(Enum):
    SAO = "SAO"       # Static Analogue Output
    DAO = "DAO"       # Dynamic Analogue Output (waveforms)
    SDO = "SDO"       # Static Digital Output
    DDO = "DDO"       # Dynamic Digital Output  (not used in 2017 rack)

    def __str__(self):          # easier to print
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