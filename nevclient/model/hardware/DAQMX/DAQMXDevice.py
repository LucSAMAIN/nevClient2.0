#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.DAQMXDevice

# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.Enums.DAQMXDeviceKind import DAQMXDeviceKind

class DAQMXDevice():
    """
    The DAQMXDevice abstract class is used to store information about the hardware.
    See the above doctstring about the "DAQMXINFO" command.

    Attributes
    ----------
    id : int
        The device id
    deviceName : str
        The device name
    modelName : str
        The model name of the device
    nChannels : int
        The number of channels the device communicate with
    state     : int
        The state of the device (? no much information about this + not much really used)
    channels  : list[DAQMXChannel]
        A list of the runtime instance of DAQMX channels.
    freq   : float
        The sampling frequence of the dynamic device
    dataLength  : int
        The maximum lenght of data to set for every channel.
    """
    def __init__(self,
                    id          : int,        # integer index used in every SET/RUN command
                    deviceName  : str,        # device name
                    modelName   : str,        # the device model name, e.g. PXI-6704
                    nChannels   : int,        # channel count  
                    state       : int,         # status
                    channels    : list[DAQMXChannel],
                    freq        : float,
                    dataLength  : int
                ):
            self.id          = id
            self.deviceName  = deviceName
            self.modelName   = modelName
            self.nChannels   = nChannels
            self.state       = state
            self.channels    = channels
            self.dataLength  = dataLength
            self.freq        = freq

            
    def getDeviceKind(self) -> DAQMXDeviceKind:
        raise NotImplementedError("The getDeviceKind method must be implemented by a child class of DAQMXDevice.")
    
    # ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetId(self, newId: int):
        self.id = newId

    def SetDeviceName(self, newDeviceName: str):
        self.deviceName = newDeviceName

    def SetModelName(self, newModelName: str):
        self.modelName = newModelName

    def SetNChannels(self, newNChannels: int):
        self.nChannels = newNChannels

    def SetState(self, newState: int):
        self.state = newState

    def SetChannels(self, newChannels: list[DAQMXChannel]):
        self.channels = newChannels

    def SetFreq(self, newFreq: float):
        self.freq = newFreq

    def SetDataLength(self, newDataLength: int):
        self.dataLength = newDataLength

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetId(self) -> int:
        return self.id

    def GetDeviceName(self) -> str:
        return self.deviceName

    def GetModelName(self) -> str:
        return self.modelName

    def GetNChannels(self) -> int:
        return self.nChannels

    def GetState(self) -> int:
        return self.state

    def GetChannels(self) -> list[DAQMXChannel]:
        return self.channels

    def GetFreq(self) -> float:
        return self.freq

    def GetDataLength(self) -> int:
        return self.dataLength