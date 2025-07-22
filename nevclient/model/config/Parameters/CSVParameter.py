#! usr/env/bin python3
#nevclient.model.config.Parameters.CSVParameter

# utils
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel

class CSVParameter():
    """
    The CSVParameter class is used to store information
    about the CSV parameters loaded by the user.
    It is deeply related to the CSVWorker class
    that handle the I/O and parsing method to
    generate CSVParameter instances.

    Parameters
    ----------
    name : str
        The parameter's name
    setupsValues : dict[str : float]
        A dictionnary mapping setup names to
        the actual value of the parameter
        for this setup
    channel : DAQMXChannel
        The channel to which this parameter is binded.
    """
    def __init__(self,
                 name : str,
                 setupsValues : dict[str : float],
                 channel : DAQMXChannel):
        self.logger         = Logger("CSVParameter")

        self.name           = name
        self.setupsValues   = setupsValues
        self.channel        = channel

# ──────────────────────────────────────────────────────────── Methods ──────────────────────────────────────────────────────────

    def __str__(self):
        s = f"{self.name} binded to device {self.device.GetDeviceName()} with channel info {self.channelInfo} device is dynamic : {self.device.isDynamic()}"
        return s
    def __repr__(self):
        return self.__str__()
    
# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetName(self, newName: str):
        self.name = newName

    def SetSetupsValues(self, newSetupsValues: dict[str, float]):
        self.setupsValues = newSetupsValues

    def SetChannel(self, channel : DAQMXChannel):
        self.channel = channel

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetName(self) -> str:
        return self.name

    def GetSetupsValues(self) -> dict[str, float]:
        return self.setupsValues

    def GetChannel(self) -> DAQMXChannel:
        return self.channel