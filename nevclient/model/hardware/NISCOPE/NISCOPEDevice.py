#! usr/env/bin python3
# nevclient.model.hardware.NISCOPE.NISCOPEDevice

# logger
from nevclient.utils.Logger import Logger
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel

class NISCOPEDevice():
    """
    The NISCOPEDevice class is used to store the information about the NISCOPE instruments.

    Attributes
    ----------
    slot : int
        ???
    deviceName : str
        ????
    modelName : str
        ????
    nChannels : int
        The number of channels the device has.
    chassis : int
        ????
    serial : int (unsigned in the backend)
        ????
    
    actualFreq : float
        The actual sample rate of the device.
    actualDlen : int
        The actual data length of the device.
    channels   : list[NISCOPEChannel]
        The list of NISCOPEChannel configuration instances.
    id : int
        The device ID, used to identify the device in the NISCOPE system.
    """

    def __init__(self,
                 id: int,
                 slot: int,
                 deviceName: str,
                 modelName: str,
                 nChannels: int,
                 chassis: int,
                 serial: int,
                 actualFreq: float,
                 actualDlen: int,
                 channels: list[NISCOPEChannel]):
        
        self.logger = Logger(f"NISCOPEDevice id={id}")

        self.id         = id
        self.slot       = slot
        self.deviceName = deviceName
        self.modelName  = modelName
        self.nChannels  = nChannels
        self.chassis    = chassis
        self.serial     = serial
        self.actualFreq = actualFreq
        self.actualDlen = actualDlen
        self.channels   = channels

# ──────────────────────────────────────────────────────────── Methods ──────────────────────────────────────────────────────────

    def __str__(self):
        s = f"NISCOPEDevice(id={self.id}, slot={self.slot}, deviceName='{self.deviceName}', modelName='{self.modelName}', "
        s += f"nChannels={self.nChannels}, chassis={self.chassis}, serial={self.serial}):\n"
        s += f"  actualFreq={self.actualFreq}, actualDlen={self.actualDlen}\n"
        return s

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetId(self, newId: int):
        self.id = newId

    def SetSlot(self, newSlot: int):
        self.slot = newSlot

    def SetDeviceName(self, newDeviceName: str):
        self.deviceName = newDeviceName

    def SetModelName(self, newModelName: str):
        self.modelName = newModelName

    def SetNChannels(self, newNChannels: int):
        self.nChannels = newNChannels

    def SetChassis(self, newChassis: int):
        self.chassis = newChassis

    def SetSerial(self, newSerial: int):
        self.serial = newSerial

    def SetActualFreq(self, newActualFreq: float):
        self.actualFreq = newActualFreq

    def SetActualDlen(self, newActualDlen: int):
        self.actualDlen = newActualDlen

    def SetChannels(self, newChannels: list[NISCOPEChannel]):
        self.channels = newChannels

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetId(self) -> int:
        return self.id

    def GetSlot(self) -> int:
        return self.slot

    def GetDeviceName(self) -> str:
        return self.deviceName

    def GetModelName(self) -> str:
        return self.modelName

    def GetNChannels(self) -> int:
        return self.nChannels

    def GetChassis(self) -> int:
        return self.chassis

    def GetSerial(self) -> int:
        return self.serial

    def GetActualFreq(self) -> float:
        return self.actualFreq

    def GetActualDlen(self) -> int:
        return self.actualDlen

    def GetChannels(self) -> list[NISCOPEChannel]:
        return self.channels
    