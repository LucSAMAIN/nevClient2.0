#! usr/env/bin python3
# nevclient.model.config.PSA.ChannelConf.py

# utils
from nevclient.utils.Logger import Logger
# Enums
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
# Hardware
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel

class ChannelConf():
    """
    Defines the configuration for every
    NISCOPE channel.

    Attribute:
    ----------
    niscopeChn       : NISCOPEChannel
        The NISCOPE channel instance related to this configuration instance.
    channelId        : int
        The id of the corresponding NISCOPEChannel instance.
    offset           : float
        The offset to set before plotting PSA data.
    verticalCoupling : NISCOPEChannelVerticalCoupling
        Enum member for the vertical coupling setting.
    verticalRange    : NISCOPEChannelVerticalRange
        Enum member for the vertical range setting. 
    active           : bool
        Does the channel is active for this NISCOPE mode
        or not ?
    """
    def __init__(self,
                 niscopeChn       : NISCOPEChannel,
                 offset           : float,
                 verticalCoupling : NISCOPEChannelVerticalRange,
                 verticalRange    : NISCOPEChannelVerticalRange,
                 active           : bool):
        self.logger = Logger("ChannelConf")

        self.niscopeChn       = niscopeChn
        self.offset           = offset
        self.verticalCoupling = verticalCoupling
        self.verticalRange    = verticalRange
        self.active           = active


# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetNiscopeChn(self) -> NISCOPEChannel:
        return self.niscopeChn
    def GetOffset(self) -> float:
        return self.offset
    def GetVerticalCoupling(self) -> NISCOPEChannelVerticalCoupling:
        return self.verticalCoupling
    def GetVerticalRange(self) -> NISCOPEChannelVerticalRange:
        return self.verticalRange
    def GetActive(self) -> bool:
        return self.active

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetNiscopeChn(self, niscopeChn : NISCOPEChannel):
        self.niscopeChn = niscopeChn
    def SetOffset(self, offset : float):
        self.offset = offset
    def SetVerticalCoupling(self, verticalCoupling : NISCOPEChannelVerticalCoupling):
        self.verticalCoupling = verticalCoupling
    def SetVerticalRange(self, verticalRange : NISCOPEChannelVerticalRange):
        self.verticalRange = verticalRange
    def SetActive(self, value : bool):
        self.active = value