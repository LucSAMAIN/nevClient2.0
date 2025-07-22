#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.SDO

# Logger
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXStaticDevice import DAQMXStaticDevice
from nevclient.model.hardware.DAQMX.DAQMXDigitalDevice import DAQMXDigitalDevice
from nevclient.model.Enums.DAQMXDeviceKind import DAQMXDeviceKind

class SDO(DAQMXStaticDevice, DAQMXDigitalDevice):
    """
    Defines the SDO type of DAQMX devices.
    Static Digital Output.
    
    Attributes
    ----------
    id             : int
        The device id
    deviceName     : str
        The device name
    modelName      : str
        The model name of the device
    nChannels      : int
        The number of channels the device communicate with
    state          : int
        The state of the device (? no much information about this + not much really used)
    channels       : list[DAQMXChannel]
        A list of the runtime instance of DAQMX channels.
    freq  = 0.0    : float
        The sampling frequence of the dynamic device
    dataLength = 1 : int
        The maximum lenght of data to set for every channel.
    """
    def __init__(self,
                    id          : int,        # integer index used in every SET/RUN command
                    deviceName  : str,        # device name
                    modelName   : str,        # the device model name, e.g. PXI-6704
                    nChannels   : int,        # channel count  
                    state       : int,        # status
                    channels    : list[DAQMXChannel],
                    freq        : float = 0.0,
                    dataLength  : int = 1
                ):
        self.logger = Logger(f"SDO id={id}")
        super().__init__(id=id, deviceName=deviceName, 
                         modelName=modelName, 
                         nChannels=nChannels, 
                         state=state, 
                         channels=channels,
                         freq=freq,
                         dataLength=dataLength)

# ──────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────  

    def getDeviceKind(self) -> DAQMXDeviceKind:
        return DAQMXDeviceKind.SDO

    def __str__(self):
        return (
            f"SDO Device object: ("
            f"  id={self.id},"
            f"  deviceName={self.deviceName},"
            f"  modelName={self.modelName},"
            f"  nChannels={self.nChannels},"
            f"  state={self.state})"
        )

    def __repr__(self):
        return (
            f"SDO Device: ("
            f"id={self.id}, "
            f"deviceName={self.deviceName})"
        )