#! usr/bin/env python3
# nevclient.model.data.TimingConf.py

# utils
from nevclient.utils.Logger import Logger
# Enums
from nevclient.model.Enums.SamplingFreq import SamplingFreq
class TimingConf():
    """
    Defines the different settings for timing configuration
    during the PSA/Sweeping process

    Attributes
    ----------
    delay    : float
    inDelay  : float
    sampling : SamplingFreq
    period   : float
        The different common settings for the
        timing configuration.
    """

    def __init__(self, delay               : float,
                       inDelay             : float,
                       sampling            : SamplingFreq,
                       period              : float):
        self.logger     = Logger("TimingConf")

        self.delay               = delay
        self.inDelay             = inDelay
        self.sampling            = sampling
        self.period              = period


# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetDelay(self) -> float:
        return self.delay
    def GetSampling(self) -> SamplingFreq:
        return self.sampling
    def GetPeriod(self) -> float:
        return self.period
    def GetInDelay(self) -> float:
        return self.inDelay

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetDelay(self, value : float):
        self.delay = value
    def SetSampling(self, value : SamplingFreq):
        self.sampling = value
    def SetPeriod(self, value : float):
        self.period = value
    def SetInDelay(self, value : float):
        self.inDelay = value