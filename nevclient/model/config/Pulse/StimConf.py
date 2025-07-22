#! usr/env/bin python3
# nevclient.model.Pulse.StimConf

class StimConf():
    """
    Stores the common configuration
    settings T and dt.

    Attributes
    ----------
    T  : int
        The total lenght of the pulse.
    dt : float
        The sampling precision.
    """
    def __init__(self, T=20, dt=0.01): # default values see old code
        self.T  = T
        self.dt = dt
# ────────────────────────────────────────────────── Getters ─────────────────────────────────────────────────────
    def GetT(self) -> int:
        return self.T
    def GetDt(self) -> float:
        return self.dt
# ────────────────────────────────────────────────── Setters ─────────────────────────────────────────────────────
    def SetT(self, newT:int):
        self.T = newT
    def SetDt(self, newDt:float):
        self.dt = newDt