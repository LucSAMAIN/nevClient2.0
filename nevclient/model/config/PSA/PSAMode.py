#! usr/env/bin python3
# nevclient.model.config.PSA.PSAMode

# utils
from nevclient.utils.Logger import Logger
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPEUnion import NISCOPEUnion
# psa
from nevclient.model.config.PSA.ChannelConf import ChannelConf
from nevclient.model.config.PSA.PSASimulation import PSASimulation
from nevclient.model.config.PSA.SweepConf import SweepConf
from nevclient.model.config.PSA.TimingConf import TimingConf
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter

class PSAMode():
    """
    This class stores the main components for 
    running a PSA simulation.

    Attributes
    ----------
    name          : str
        The name of the PSA mode (i.e. 'null cline')
    niscopeUnion  : NISCOPEUnion
        The NISCOPE union's id this override
        configuration mode is working with.
    operation     : callable
        The operation to apply on the PSA
        data before plotting.
        i.e. std mean for nc mode
    psaSimulation : PSASimulation
        The data of the current ongoing simulation
    chnConfList   : list[ChannelConf]
        The list of the channel configuration
        instance.
    timing        : TimingConf
        The current timing configuration.
    operationName : str
        The name of the defined operation
        i.e. 'std-mean' for the NC mode
    curParam      : CSVParameter
        The currently selected parameter.
    sweepMap      : dict[str : SweepConf]
        Mapping parameters'name to their corresponding sweeping configuration.
    tag           : str
        The tag's name, i.e. '#NCMODE'
    """
    def __init__(self,
                 name          : str,
                 niscopeUnion  : NISCOPEUnion,
                 operation     : callable,
                 psaSimulation : PSASimulation,
                 chnConfList   : list[ChannelConf],
                 timing        : TimingConf,
                 operationName : str,
                 curParam      : CSVParameter,
                 sweepMap      : dict[str : SweepConf],
                 tag           : str
                 ):
        self.logger       = Logger("PSAMode")

        self.name          = name
        self.niscopeUni    = niscopeUnion
        self.operation     = operation
        self.psaSimulation = psaSimulation
        self.chnConfList   = chnConfList
        self.sweepMap      = sweepMap
        self.timing        = timing
        self.operationName = operationName
        self.curParam      = curParam
        self.tag           = tag


# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetName(self, name: str):
        self.name = name

    def SetNiscopeUni(self, niscopeUni: NISCOPEUnion):
        self.niscopeUni = niscopeUni

    def SetOperation(self, operation: callable):
        self.operation = operation

    def SetPsaSimulation(self, psaSimulation: PSASimulation):
        self.psaSimulation = psaSimulation

    def SetChnConfList(self, chnConfList: list[ChannelConf]):
        self.chnConfList = chnConfList

    def SetSweepMap(self, newSweepMap: dict[str, SweepConf]):
        self.sweepMap = newSweepMap

    def SetTiming(self, timing: TimingConf):
        self.timing = timing

    def SetOperationName(self, value : str):
        self.operationName = value
    
    def SetCurParam(self, newCurParam: CSVParameter):
        self.curParam = newCurParam

    def SetTag(self, tag : str):
        self.tag = tag

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────
    
    def GetCurParam(self) -> CSVParameter:
        return self.curParam
    
    def GetName(self) -> str:
        return self.name

    def GetNiscopeUni(self) -> NISCOPEUnion:
        return self.niscopeUni

    def GetOperation(self) -> callable:
        return self.operation

    def GetPsaSimulation(self) -> PSASimulation:
        return self.psaSimulation

    def GetChnConfList(self) -> list[ChannelConf]:
        return self.chnConfList

    def GetSweepMap(self) -> dict[str, SweepConf]:
        return self.sweepMap

    def GetTiming(self) -> TimingConf:
        return self.timing
    
    def GetOperationName(self) -> str:
        return self.operationName
    
    def GetTag(self) -> str:
        return self.tag