#! usr/bin/env python3
# nevclient.views.EntryFrame.py

import wx, os

from nevclient.views.templates.NevFrame import NevFrame
from nevclient.views.templates.NevStatusBar import NevStatusBar
from nevclient.views.templates.NevMenuBar import NevMenuBar
from nevclient.views.templates.NevPanel import NevPanel

from nevclient.views.PulsePanel import PulsePanel
from nevclient.views.SweeperPanel import SweeperPanel
from nevclient.views.ParametersPanel import ParametersPanel
from nevclient.views.PSAPanel import PSAPanel

from utils.Theme import getThemes, changeTheme


class EntryFrame(NevFrame):
    def __init__(self, 
                 controller, 
                 psaData, 
                 colorMap, 
                 generateLegends,
                 activeChannelConf,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)            
        self.controller = controller

        # ---- WIDGETS:
        self.panel = NevPanel(parent=self)
        # Bars & menus:
        self.menuBar = NevMenuBar()
        self.SetMenuBar(self.menuBar)
        self.statusBar = NevStatusBar(parent=self.panel)
        self.statusBar.SetStatusText("Waiting user to load csv parameters...")
        self.SetStatusBar(self.statusBar)
        # Parameters menu
        parametersMenu = wx.Menu()
        openItemParametersMenu = parametersMenu.Append(id=wx.ID_OPEN, item="Load from csv", helpString="Load parameters from a csv file")
        self.menuBar.Append(parametersMenu, "Parameters")
        # Theme menu
        themeMenu = wx.Menu()
        for themeName in getThemes():
            themeItem = themeMenu.Append(id=wx.ID_ANY, item=f"{themeName}", helpString=f"Switch to '{themeName}' theme.")
            self.Bind(wx.EVT_MENU, lambda e, themeName=themeName : self.OnChangingTheme(e, themeName), themeItem)
        self.menuBar.Append(themeMenu, "Themes")
        # Panels:
        # Pulse
        self.pulsePanel = PulsePanel(parent=self.panel, controller=self.controller, style=wx.SUNKEN_BORDER)
        # Parameters
        self.parametersPanel = NevPanel(parent=self.panel, style=wx.SUNKEN_BORDER)
        # Sweeper
        self.sweeperPanel = SweeperPanel(parent=self.panel, 
                                         controller=self.controller, 
                                         style=wx.SUNKEN_BORDER,
                                         colorMap=colorMap,
                                         psaData=psaData) 
        # PSA
        self.PSAPanel = PSAPanel(parent=self.panel, 
                                 controller=self.controller, 
                                 style=wx.SUNKEN_BORDER,
                                 generateLegends=generateLegends,
                                 activeChannelConf=activeChannelConf,
                                 psaData=psaData)


        # ---- SIZERS
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.middleSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        # Sweeper
        self.leftSizer.Add(self.sweeperPanel, 1, wx.EXPAND)
        # PSA
        self.leftSizer.Add(self.PSAPanel, 1, wx.EXPAND) 
        # Pulse
        self.middleSizer.Add(self.pulsePanel, 1, wx.EXPAND) 
        # Parameters
        self.rightSizer.Add(self.parametersPanel, 1, wx.EXPAND)
        # Main        
        mainSizer.Add(self.leftSizer, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.middleSizer, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.rightSizer, 2, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(mainSizer)
       
    
        # ---- BINDINGS 
        # Menus:
        self.Bind(wx.EVT_MENU, self.OnOpenItemParametersMenu, openItemParametersMenu)
        
        # Screen:
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        
        # ---- END OF INIT 
        self.ApplyTheme()
        self.menuBar.ApplyTheme()
        self.statusBar.ApplyTheme()
        
        self.panel.Refresh()
        self.panel.Layout()
        self.panel.Update()
        self.panel.SetAutoLayout(True)
        self.Centre( wx.BOTH ) 
    







# ──────────────────────────────────────────────── EVENTS HANDLERS ─────────────────────────────────────────────────────


    def OnOpenItemParametersMenu(self,e):
        dirname = './'
        dlg = wx.FileDialog(self, "Choose a file", dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK: # if we clicked on ok
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            dlg.Destroy()
            # We now let the controller handle the rest:
            self.controller.OnEntryFrameOpenItemParametersMenu(filename, dirname)

            self.statusBar.SetStatusText("Parameters loaded !")
        else:
            dlg.Destroy()

        e.Skip()
        

    def OnClose(self, e):
        self.Destroy()

    def OnChangingTheme(self, e, themeName : str):
        """
        Themes menu items function handler.
        It changes the theme to the corresponding 'themeName'.
        To see the available themes see the _themes dict in the 'utils/theme.py' file.

        Parameters
        ---------- 
        e : wx.Event
            The wxpython event object.
        themeName : str 
            The name of the wanted theme.
        """
        changeTheme(themeName)
        
        # We can now update the theme
        self.ApplyTheme()
        self.menuBar.ApplyTheme()
        self.statusBar.ApplyTheme()


    # ──────────────────────────────────────────────── GETTERS ─────────────────────────────────────────────────────
    def GetSweeperPanel(self) -> NevPanel:
        return self.sweeperPanel
    
    def GetPSAPanel(self) -> NevPanel:
        return self.PSAPanel
    
    def GetParametersPanel(self) -> ParametersPanel :
        return self.parametersPanel
    
    def GetPulsePanel(self) -> PulsePanel:
        return self.pulsePanel
    
    def GetPanel(self) -> NevPanel:
        return self.panel
    
    def GetRightSizer(self) -> wx.BoxSizer:
        return self.rightSizer
    
    # ──────────────────────────────────────────────── SETTERS ─────────────────────────────────────────────────────

    def SetParametersPanel(self, newPanel : NevPanel) -> None:
        self.parametersPanel = newPanel
    
    # ──────────────────────────────────────────────── OTHER METHODS ─────────────────────────────────────────────────────

    def ReplaceParametersPanel(self, newPanel : NevPanel) -> None:
        """
        This method is called by the controller to replace the former
        parameters panel to the new one.
        It is called after the user has loaded a CSV file.

        Parameters
        ----------
        newPanel : NevPanel
            The new parameters panel to display in the frame.
        """
        oldPanel = self.parametersPanel
        self.parametersPanel = newPanel
        self.rightSizer.Replace(oldPanel, self.parametersPanel)
        oldPanel.Destroy()

        self.panel.Refresh()
        self.panel.Layout()
        self.panel.Update()
        
        
