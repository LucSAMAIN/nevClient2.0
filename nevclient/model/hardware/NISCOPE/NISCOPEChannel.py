#! usr/env/bin python3
# nevclient.model.hardware.NISCOPE.NISCOPEChannel

from __future__ import annotations # resolving circular import issues

# niscope
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
# from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice # to break circular import

class NISCOPEChannel():
    """
    Defines the configuration of channel
    for a specififc device.

    Attributes
    ----------
    device : NISCOPEDevice
        The device this channel belongs to.
    verticalRange : NISCOPEChannelVerticalRange
        The vertical range setting of the niscope's channel.
    verticalCoupling : NISCOPEChannelVerticalCoupling
        The vertical coupling setting of the niscope's channel.
    index : int
        The index position of the channel for the corresponding device
    """

    def __init__(self,
                 device           : NISCOPEDevice,
                 verticalRange    : NISCOPEChannelVerticalRange,
                 verticalCoupling : NISCOPEChannelVerticalCoupling,
                 index            : int):
        
        self.index           = index
        self.device           = device
        self.verticalRange    = verticalRange
        self.verticalCoupling = verticalCoupling

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetDevice(self, newDevice: NISCOPEDevice):
        self.device = newDevice

    def SetVerticalRange(self, newVerticalRange: NISCOPEChannelVerticalRange):
        self.verticalRange = newVerticalRange

    def SetVerticalCoupling(self, newVerticalCoupling: NISCOPEChannelVerticalCoupling):
        self.verticalCoupling = newVerticalCoupling
    
    def SetIndex(self, value : int):
        self.index = value

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetDevice(self) -> NISCOPEDevice:
        return self.device

    def GetVerticalRange(self) -> NISCOPEChannelVerticalRange:
        return self.verticalRange

    def GetVerticalCoupling(self) -> NISCOPEChannelVerticalCoupling:
        return self.verticalCoupling
    
    def GetIndex(self) -> int:
        return self.index