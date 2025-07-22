import wx
from utils.Theme import getColoursDict

class NevMenuBar(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """
    ------------------------------------------------------------
    -----------------------METHODS------------------------------
    ------------------------------------------------------------
    """

    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(colorDict["hard"])
        self.SetBackgroundColour(colorDict["soft"])