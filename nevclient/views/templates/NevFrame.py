import wx
from utils.Theme import getColoursDict

class NevFrame(wx.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    """
    ------------------------------------------------------------
    -----------------------METHODS------------------------------
    ------------------------------------------------------------
    """
        

    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colorDict["light"])
        for child in self.GetChildren():
            child.ApplyTheme()
