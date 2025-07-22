import wx
from utils.Theme import getColoursDict



class NevText(wx.StaticText):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def ApplyTheme(self):
        raise NotImplementedError("Subclasses must implement ApplyTheme")



class NevTitleText(NevText):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(colorDict["hard"])
        self.SetBackgroundColour(colorDict["light"])
        font = self.GetFont()
        font.MakeBold()
        font.SetFamily(wx.MODERN)
        font.SetPointSize(20)
        self.SetFont(font)


            

class NevSimpleText(NevText):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(colorDict["hard"])
        self.SetBackgroundColour(colorDict["light"])
        font = self.GetFont()
        font.SetFamily(wx.MODERN)
        self.SetFont(font)

class NevSimpleTextWithColor(NevText):
    def __init__(self, parent, color:str,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.color = color
    
    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(self.color)
        self.SetBackgroundColour(colorDict["light"])
        font = self.GetFont()
        font.SetFamily(wx.MODERN)
        self.SetFont(font)


class NevSimpleBoldText(NevText):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
    def ApplyTheme(self):
        colorDict = getColoursDict()
        self.SetForegroundColour(colorDict["hard"])
        self.SetBackgroundColour(colorDict["light"])
        font = self.GetFont()
        font.MakeBold()
        font.SetFamily(wx.MODERN)
        self.SetFont(font)




