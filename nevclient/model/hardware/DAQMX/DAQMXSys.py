#! usr/env/bin python3
# nevclient.model.hardware.DAQMX.DAQMXSys.py
from __future__ import annotations # to break circular import

# utils
from nevclient.utils.Logger import Logger

class DAQMXSys():
    """
    The DAQMXSys class is used to store information about tasks in a convinient way (see the attributes).

    Attributes
    ----------
    devicesMap : dict[int : DAQMXDevice]
        A dictionnary mapping the id of every device to its runtime object.
    """
    def __init__(self,
                 devicesMap : dict[int : DAQMXDevice]):
        self.logger = Logger("DAQMXSys")

        self.devicesMap = devicesMap
        

    
    def __str__(self):
        """
        Returns a string representation of the DAQMXSys object.
        """
        s = f"DAQMXSys:\n"
        device : DAQMXDevice
        for device in self.devicesMap.values():
            s += f"  id: {device.id} -> {device.deviceName} ({device.modelName}), nChannels={device.nChannels}, kind={device.getTaskKind()}\n"
      
        return s   


# ────────────────────────────────────────────────── Getter ─────────────────────────────────────────────────────

    def GetDevicesMap(self) -> dict[int : DAQMXDevice]:
        return self.devicesMap
    
# ────────────────────────────────────────────────── Setter ─────────────────────────────────────────────────────

    def SetDevicesMap(self, newMap : dict[int : DAQMXDevice]):
        self.devicesMap = newMap
