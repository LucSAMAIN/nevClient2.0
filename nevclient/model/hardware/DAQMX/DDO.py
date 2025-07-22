#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.DDO

# Logger
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXDynamicDevice import DAQMXDynamicDevice
from nevclient.model.hardware.DAQMX.DAQMXDigitalDevice import DAQMXDigitalDevice
from nevclient.model.Enums.DAQMXDeviceKind import DAQMXDeviceKind

class DDO(DAQMXDynamicDevice, DAQMXDigitalDevice):
    """
    Defines the DDO type of DAQMX devices.
    Dynamic Digital Output.
    
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
    freq           : float
        The sampling frequence of the dynamic device
    dataLength     : int
        The maximum lenght of data to set for every channel.
    """
    def __init__(self,
                    id          : int,        # integer index used in every SET/RUN command
                    deviceName  : str,        # device name
                    modelName   : str,        # the device model name, e.g. PXI-6704
                    nChannels   : int,        # channel count  
                    state       : int,         # status
                    freq        : float, # sampling frequency - only for dynamic devices
                    dataLength  : int, # max lenght data for a channel
                    channels    : list[DAQMXChannel]
                ):
        self.logger = Logger(f"DDO id={id}")
        super().__init__(id=id, 
                         deviceName=deviceName, 
                         modelName=modelName, 
                         nChannels=nChannels, 
                         state=state, 
                         freq=freq, 
                         dataLength=dataLength,
                         channels=channels)


# ──────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────  
    def getDeviceKind(self) -> DAQMXDeviceKind:
        return DAQMXDeviceKind.DDO
    
    def _resetData(self):
        self.data = [[] for _ in range(self.nChannels)]        
    
    def __str__(self):
        return (
            f"DAO Device object: ("
            f"  id={self.id},"
            f"  deviceName={self.deviceName},"
            f"  modelName={self.modelName},"
            f"  nChannels={self.nChannels},"
            f"  lData={self.dataLength},"
            f"  freq={self.freq},"
            f"  state={self.state})"
        )

    def __repr__(self):
        return (
            f"DAO Device: ("
            f"id={self.id}, "
            f"deviceName={self.deviceName})"
        )
