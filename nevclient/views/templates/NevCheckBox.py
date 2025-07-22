import wx

from utils.Theme import getColoursDict

class NevCheckBox(wx.CheckBox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colour=colorDict["light"])
        self.SetForegroundColour(colour=colorDict["hard"])


