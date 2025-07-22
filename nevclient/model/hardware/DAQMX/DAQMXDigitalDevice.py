#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.DAQMXDigitalDevice

# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel

class DAQMXDigitalDevice(DAQMXDevice):
    """
    The DAQMXDigitalDevice abstract class is used to defined the format of Digital DAQMX devices
    """
    def __init__(self,
                    id          : int,        # integer index used in every SET/RUN command
                    deviceName  : str,        # device name
                    modelName   : str,        # the device model name, e.g. PXI-6704
                    nChannels   : int,        # channel count  
                    state       : int,
                    channels    : list[DAQMXChannel],
                    freq        : float,
                    dataLength  : int
                ):
        super().__init__(id=id, 
                         deviceName=deviceName, 
                         modelName=modelName, 
                         nChannels=nChannels, 
                         state=state, 
                         channels=channels,
                         freq=freq,
                         dataLength=dataLength)

# ──────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────
  
    def isDigital(self) -> bool:
        return True
    def isAnalog(self) -> bool:
        return False