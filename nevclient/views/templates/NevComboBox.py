import wx

from utils.Theme import getColoursDict

class NevComboBox(wx.ComboBox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetBackgroundColour(colorDict["light"])
        self.SetForegroundColour(colorDict["hard"])