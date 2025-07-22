#! usr/env/bin python3
# nevclient.model.hardware.NISCOPE.NISCOPESys

# logger
from nevclient.utils.Logger import Logger
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice
from nevclient.model.hardware.NISCOPE.NISCOPEUnion import NISCOPEUnion

class NISCOPESys():
    """
    The NISCOPESys class is used to store information about tasks in a convinient way (see the attributes).

    Attributes
    ----------
    devicesMap : dict[int : NISCOPEDevice]
        Mapping devices'id to their corresponding instance.
    unionsMap  : dict[int, NISCOPEUnion]
        Mapping unions'id to their corresponding instance.
    """

    def __init__(self,
                 devicesMap: dict[int, NISCOPEDevice],
                 unionsMap: dict[int, NISCOPEUnion]):
        
        self.logger = Logger("NISCOPESys")

        self.devicesMap = devicesMap
        self.unionsMap = unionsMap

    def __str__(self):
        num_devices = len(self.devicesMap)
        num_unions = len(self.unionsMap)
        return f"NISCOPESys managing {num_devices} devices and {num_unions} unions."

    def __repr__(self):
        return self.__str__()

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetDevicesMap(self, newDevicesMap: dict[int, NISCOPEDevice]):
        self.devicesMap = newDevicesMap

    def SetUnionsMap(self, newUnionsMap: dict[int, NISCOPEUnion]):
        self.unionsMap = newUnionsMap

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetDevicesMap(self) -> dict[int, NISCOPEDevice]:
        return self.devicesMap

    def GetUnionsMap(self) -> dict[int, NISCOPEUnion]:
        return self.unionsMap

   
