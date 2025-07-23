#! usr/bin/env python3
# nevclient.model.data.PSASimulation

# utils
from nevclient.utils.Logger import Logger
# model.Enums
from nevclient.model.Enums.PSAStatus import PSAStatus




class PSASimulation():
    """
    The PSAData class is used to store information
    about the PSA ongoing simulation.

    Attributes
    ----------
    XSweeper : list[float]
    Y : dict[(devId, chnId) : list[list[float]]]
        The plotting data.
    XAxisName : str
        The current selected XAxis name.
    status : PSAStatus
        The PSAStatus of returned by the backend
        server.
    stage  : int
        The stage step in the PSA simulation.
        It also corresponds to the number of readable
        points.
    lastSValue : float
        The last Sweeper value sent by the backend server
        after calling with the 'GET PSA STAT'
    start, end : int
        The start and end steps integers recovered from the backend
        for the last 'GET PSA DATA' call
    
    logger : Logger
        A Logger instance to display information during running time.
    """
    def __init__(self, 
                 XSweeper  : list[float],
                 Y         : dict[(int, int) : list[list[float]]],
                 XAxisName : str,
                 status    : PSAStatus,
                 stage     : int,
                 lastSValue : float,
                 start      : int,
                 end        : int):

        self.logger = Logger("PSAData")

        self.XSweeper           = XSweeper
        self.XAxisName          = XAxisName
        self.Y                  = Y
        self.status             = status
        self.stage              = stage
        self.lastSValue         = lastSValue
        self.start              = start
        self.end                = end

        self.logger.deepDebug("Succesfully created an instance.")

    

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetY(self, newY : dict):
        self.Y = newY
    def SetXAxisName(self, newAxisName : str):
        self.XAxisName = newAxisName
    def SetStage(self, newStage : int):
        self.stage = newStage
    def SetStart(self, newStart : int):
        self.start = newStart
    def SetLastSValue(self, newLastSValue : float):
        self.lastSValue = newLastSValue
    def SetStatus(self, newStatus : PSAStatus):
        self.status = newStatus
    def SetXSweeper(self, newXSweeper : list[float]):
        self.XSweeper = newXSweeper
    def SetEnd(self, newEnd : int):
        self.end = newEnd

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetXAxisName(self) -> str:
        return self.XAxisName
    def GetStatus(self) -> PSAStatus:
        return self.status
    def GetStage(self) -> int:
        return self.stage
    def GetLastSValue(self) -> float:
        return self.lastSValue
    def GetXSweeper(self) -> list[float]:
        return self.XSweeper
    def GetY(self) -> dict[(int, int) : list[list[float]]]:
        return self.Y