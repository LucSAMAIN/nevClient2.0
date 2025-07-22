#! usr/env/bin python3
# nevclient.model.config.PSA.PSAData

# utils
from nevclient.utils.Logger import Logger
# psa
from nevclient.model.config.PSA.PSAMode import PSAMode
from nevclient.model.config.PSA.SweepConf import SweepConf


class PSAData():
    """
    Stores the current state
    of the PSA main instances.

    Attributes
    ----------
    curPsaMode  : PSAMode
        The currently selected mode, i.e. 'null cline'
    psaModeMap  : dict[str : PSAMode]
        Mapping modes'name to their corresponding instance.
    """

    def __init__(self,
                 curPsaMode : PSAMode,
                 psaModeMap : dict[str, PSAMode]):
        
        self.logger = Logger("PSAData")

        self.curPsaMode = curPsaMode
        self.psaModeMap = psaModeMap

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetCurPsaMode(self, newCurPsaMode: PSAMode):
        self.curPsaMode = newCurPsaMode

    def SetPsaModeMap(self, newPsaModeMap: dict[str, PSAMode]):
        self.psaModeMap = newPsaModeMap

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetCurPsaMode(self) -> PSAMode:
        return self.curPsaMode

    def GetPsaModeMap(self) -> dict[str, PSAMode]:
        return self.psaModeMap

    