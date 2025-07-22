#! usr/env/bin python3
# nevclient.model.hardware.NISCOPE.NISCOPEUnion

# Logger
from nevclient.utils.Logger import Logger
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice
from nevclient.model.Enums.NISCOPETriggerCoupling import NISCOPETriggerCoupling
from nevclient.model.Enums.NISCOPETriggerSlope import NISCOPETriggerSlope
from nevclient.model.Enums.NISCOPETriggerType import NISCOPETriggerType

class NISCOPEUnion():
    """
    The NISCOPEUnion class is used to store information about NISCOPE devices unions.

    Attributes
    ----------
    id : int
        The union id number used to identify the union in the NISCOPE system.
    dlen : int
        The data length for the union. 
        This is the "minRecordLength" in the NISCOPE server terminology.
    freq : float
        The minimum sample rate for the union. 
        This is the "minSampleRate" in the NISCOPE server terminology.
   
    refPosition : float
        ???
    triggerType : TriggerType
        ???
    triggerSource : str
        ???
    triggerDevice : int
        ???
    triggerLevel : float
        ???
    triggerSlope : TriggerSlope
        ???
    triggerCoupling : TriggerCoupling
        ???
    triggerHoldoff : float
        ???
    triggerDelay : float
        ???
    nChannels : int
        The number of channels (?)
    devicesMap : dict[int, NISCOPEDevice]
        A map of device ID to NISCOPEDevice object for quick access.
    """
    #  devActualDlen : list[int]
    #     A list of the actual data length for each device in the union.
    #     The length of this list is equal to the number of devices in the union.
    #     The first value is for device 0, the second value is for device 1,
    # devActualFreq : list[float]
    #     A list of the actual sample rates for each device in the union.
    #     The length of this list is equal to the number of devices in the union.
    #     The first value is for device 0, the second value is for device 1, etc.

    # channelVerticalRange : list[int]
    #     Since device's id are range from 0 to nDevices-1, this list defined the channel vertical range for each device in the union.
    #     So the first value in this list is the channel vertical range for device 0, the second value is still for device 0 until we reach
    #     index nChannels-1 of the first device, then the next value is for device 1, etc.
    # channelVerticalCoupling : list[VerticalCoupling]
    #     Since device's id are range from 0 to nDevices-1, this list defined the channel vertical coupling for each device in the union.
    #     So the first value in this list is the channel vertical coupling for device 0, the second value is still for device 0 until we reach
    #     index nChannels-1 of the first device, then the next value is for device 1, etc.

    def __init__(self,
                 id: int,
                 dlen: int,
                 freq: float,
                 refPosition: float,
                 triggerType: NISCOPETriggerType,
                 triggerSource: str,
                 triggerDevice: int,
                 triggerLevel: float,
                 triggerSlope: NISCOPETriggerSlope,
                 triggerCoupling: NISCOPETriggerCoupling,
                 triggerHoldoff: float,
                 triggerDelay: float,
                 nChannels: int,
                 devicesMap: dict[int, NISCOPEDevice]):
        
        self.logger = Logger(f"NISCOPEUnion id={id}")

        self.id              = id
        self.dlen            = dlen
        self.freq            = freq
        self.refPosition     = refPosition
        self.triggerType     = triggerType
        self.triggerSource   = triggerSource
        self.triggerDevice   = triggerDevice
        self.triggerLevel    = triggerLevel
        self.triggerSlope    = triggerSlope
        self.triggerCoupling = triggerCoupling
        self.triggerHoldoff  = triggerHoldoff
        self.triggerDelay    = triggerDelay
        self.nChannels       = nChannels
        self.devicesMap      = devicesMap

# ──────────────────────────────────────────────────────────── Methods ──────────────────────────────────────────────────────────

    def __str__(self):
        s = f"NISCOPEUnion(id={self.id}, dlen={self.dlen}, freq={self.freq}, nChannels={self.nChannels}, nDevices={len(self.devicesMap)})\n"
        return s

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetId(self, newId: int):
        self.id = newId

    def SetDlen(self, newDlen: int):
        self.dlen = newDlen

    def SetFreq(self, newFreq: float):
        self.freq = newFreq

    def SetRefPosition(self, newRefPosition: float):
        self.refPosition = newRefPosition

    def SetTriggerType(self, newTriggerType: NISCOPETriggerType):
        self.triggerType = newTriggerType

    def SetTriggerSource(self, newTriggerSource: str):
        self.triggerSource = newTriggerSource

    def SetTriggerDevice(self, newTriggerDevice: int):
        self.triggerDevice = newTriggerDevice

    def SetTriggerLevel(self, newTriggerLevel: float):
        self.triggerLevel = newTriggerLevel

    def SetTriggerSlope(self, newTriggerSlope: NISCOPETriggerSlope):
        self.triggerSlope = newTriggerSlope

    def SetTriggerCoupling(self, newTriggerCoupling: NISCOPETriggerCoupling):
        self.triggerCoupling = newTriggerCoupling

    def SetTriggerHoldoff(self, newTriggerHoldoff: float):
        self.triggerHoldoff = newTriggerHoldoff

    def SetTriggerDelay(self, newTriggerDelay: float):
        self.triggerDelay = newTriggerDelay

    def SetNChannels(self, newNChannels: int):
        self.nChannels = newNChannels

    def SetDevicesMap(self, newDevicesMap: dict[int, NISCOPEDevice]):
        self.devicesMap = newDevicesMap

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetId(self) -> int:
        return self.id

    def GetDlen(self) -> int:
        return self.dlen

    def GetFreq(self) -> float:
        return self.freq

    def GetRefPosition(self) -> float:
        return self.refPosition

    def GetTriggerType(self) -> NISCOPETriggerType:
        return self.triggerType

    def GetTriggerSource(self) -> str:
        return self.triggerSource

    def GetTriggerDevice(self) -> int:
        return self.triggerDevice

    def GetTriggerLevel(self) -> float:
        return self.triggerLevel

    def GetTriggerSlope(self) -> NISCOPETriggerSlope:
        return self.triggerSlope

    def GetTriggerCoupling(self) -> NISCOPETriggerCoupling:
        return self.triggerCoupling

    def GetTriggerHoldoff(self) -> float:
        return self.triggerHoldoff

    def GetTriggerDelay(self) -> float:
        return self.triggerDelay

    def GetNChannels(self) -> int:
        return self.nChannels

    def GetDevicesMap(self) -> dict[int, NISCOPEDevice]:
        return self.devicesMap

   