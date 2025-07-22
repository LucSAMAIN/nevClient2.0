import wx
from utils.Theme import getColoursDict

class NevStatusBar(wx.StatusBar):
    def __init__(self, parent, *args, **kwargs):
        """
        Useful parameters:
        - parent : The parent window of the status bar (usually a frame)
        """
        super().__init__(parent, *args, **kwargs)

    """
    ------------------------------------------------------------
    -----------------------METHODS------------------------------
    ------------------------------------------------------------
    """

    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(colorDict["hard"])
        self.SetBackgroundColour(colorDict["soft"])