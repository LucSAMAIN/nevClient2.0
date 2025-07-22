#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.DAQMXStaticDevice

# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice

class DAQMXStaticDevice(DAQMXDevice):
    """
    The DAQMXStaticDevice is a chid class of the DAQMXDevice.
    It defines the format of dynamic DAQMX devices (DAO and DDO for now). 
    
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
                    state       : int,        # status
                    channels    : list[DAQMXChannel],
                    dataLength  : int = 1 ,
                    freq        : float = 0.0
                ):
        if dataLength != 1:
            raise Exception(f"Tried to create an instance of a DAQMX Static device with a data length that is not 1: {dataLength}")
        if freq != 0.0:
            raise Exception(f"Tried to create an instance of a DAQMX Static device with a freq that is not 0.0: {freq}")
            
        super().__init__(id=id, 
                         deviceName=deviceName, 
                         modelName=modelName, 
                         nChannels=nChannels, 
                         state=state, 
                         channels=channels,
                         freq=freq,
                         dataLength=dataLength)
    


# ──────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────

    def isDynamic(self) -> bool:
        return False
    def isStatic(self) -> bool:
        return True

