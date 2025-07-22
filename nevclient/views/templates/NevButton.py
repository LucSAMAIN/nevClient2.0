import wx
from utils.Theme import getColoursDict

class NevButton(wx.Button):
    def __init__(self, parent, label, *args, **kwargs):
        super().__init__(parent, label=label, *args, **kwargs)
        
    
    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colorDict["light"])
        self.SetForegroundColour(colorDict["hard"])

    