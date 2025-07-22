import wx
import wx.grid


class NevGrid(wx.grid.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """
    ------------------------------------------------------------
    -----------------------METHODS------------------------------
    ------------------------------------------------------------
    """

    def ApplyTheme(self):        
        font = self.GetLabelFont()
        font.SetFamily(wx.MODERN)
        self.SetLabelFont(font)
