#! usr/env/bin python3
# nevclient.model.hardware.DAMQX.DAQMXAnalogDevice

# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel


class DAQMXAnalogDevice(DAQMXDevice):
    """
    The DAQMXAnalogDevice abstract class is used to defined the format of analogic DAQMX devices
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

    def isAnalog(self) -> bool:
        return True
    def isDigital(self) -> bool:
        return False