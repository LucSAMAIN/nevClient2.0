#! usr/bin/env python3
# nevclient.model.data.PulseConf

# logger
from nevclient.utils.Logger import Logger
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter




    
class PulseConf():
    """
    This class is used to store information
    about a defined pulse.

    Attributes:
    -----------
    id            : int
        The  pulse's id.
    delay         : float
        The delay of the pulse in ms
    width         : float
        The width of the pulse in ms
    amp           : float
        The amplitude of the pulse in mV 
    active        : bool
        Is the checkbox checked or not ?
    param         : CSVParameter
        The CSVParameter instance linked
        to this pulse configuration
    """
    def __init__(self,
                 id       : int,
                 delay    : float,
                 width    : float,
                 amp      : float,
                 active   : bool,
                 param    : CSVParameter):
        self.logger = Logger(f"PulseConfiguration id={id}")
        
        self.id     = id
        self.delay  = delay
        self.width  = width
        self.amp    = amp
        self.active = active
        self.param  = param

# ────────────────────────────────────────────────── SETTERS ─────────────────────────────────────────────────────
    
    def SetDelay(self, delay : float):
        self.delay = delay
    def SetAmp(self, amp : float):
        self.amp = amp
    def SetWidth(self, width : float):
        self.width = width
    def SetActive(self, active : bool):
        self.active = active
    def SetParam(self, param : CSVParameter):
        self.param = param
    def SetId(self, id : int):
        self.id = id

# ────────────────────────────────────────────────── GETTERS ─────────────────────────────────────────────────────

    def GetDelay(self) -> float:
        return self.delay
    def GetAmp(self) -> float:
        return self.amp
    def GetWidth(self) -> float:
        return self.width
    def GetActive(self) -> bool:
        return self.active
    def GetParam(self) -> CSVParameter:
        return self.param
    def GetId(self) -> int:
        return self.id


