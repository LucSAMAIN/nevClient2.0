#! usr/env/bin python3
# nevclient.model.config.PSA.SweepConf.py

# utils
from nevclient.utils.Logger import Logger
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# sweep direction
from nevclient.model.Enums.SweepDirection import SweepDirection

class SweepConf():
    """
    The SweepConf class is used to store information about the
    PSA simulation, since it involves a lot of different
    parameters and configuration.
    It allows us to lighten the main class.
    
    Attributes
    ----------
    param    : CSVParameter
        The CSVParameter to which this instance is
        configuring for.
    start    : float
    stop     : float
    steps    : int
    sweepDi  : SweepDirection
        The configuration settings of the sweeper / NISCOPE panel

    """
    def __init__(self, 
                       param    : CSVParameter,
                       start        : float,
                       stop         : float,
                       steps        : int,
                       sweepDi      : SweepDirection):
        self.logger = Logger("SweepConf")

        self.param         = param
        self.start         = start
        self.stop          = stop
        self.steps         = steps
        self.sweepDi       = sweepDi

    



# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetStart(self) -> float:
        return self.start
    def GetStop(self) -> float:
        return self.stop
    def GetSteps(self) -> int:
        return self.steps
    def GetParam(self) -> CSVParameter:
        return self.param
    def GetSweepDi(self) -> SweepDirection:
        return self.sweepDi

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetStart(self, value : float):
        self.start = value
    def SetStop(self, value : float):
        self.stop = value
    def SetSteps(self, value : int):
        self.steps = value
    def SetParam(self, param : CSVParameter):
        self.param = param
    def SetSweepDi(self, value : SweepDirection):
        self.sweepDi = value