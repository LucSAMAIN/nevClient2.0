import wx

from utils.Theme import getColoursDict

class NevSpinCtrl(wx.SpinCtrlDouble):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colorDict["soft"])
        self.SetForegroundColour(colorDict["hard"])

class NevNamedSpinCtrl(wx.SpinCtrlDouble):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name


    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colorDict["soft"])
        self.SetForegroundColour(colorDict["hard"])
        
    def GetName(self):
        return self.name