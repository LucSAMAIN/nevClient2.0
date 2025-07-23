#! usr/env/bin python3
# nevclient.views.PSAPanel.py

# extern modules
import wx
# views.templates
from nevclient.views.templates.NevPanel import NevPanel
from nevclient.views.templates.NevPSAPlot import NevPSAPlot
from nevclient.views.templates.NevComboBox import NevComboBox
from nevclient.views.templates.NevButton import NevButton
from nevclient.views.templates.NevText import NevSimpleText 
# PSA
from nevclient.model.config.PSA.PSASimulation import PSASimulation
from nevclient.model.config.PSA.ChannelConf import ChannelConf

class PSAPanel(NevPanel):
    """
    The PSAPanel class is used to manage the display of PSA data
    inside the entryframe.
    """
    def __init__(self, parent, 
                 controller,
                 activeChannelConf,
                 generateLegends,
                 psaData, 
                 *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.controller = controller

        # ---- WIDGETS:        
        # ComboBox and text for the XAxis:
        self.comboBoxXAxisText = NevSimpleText(parent=self, label="Select the X axis")
        confs = activeChannelConf
        choices = [generateLegends(conf) for conf in confs]

        self.comboBoxXAxis = NevComboBox(parent=self, style=wx.CB_READONLY, choices=["Sweeper"] + choices)
        self.comboBoxXAxis.SetSelection(0)
        # Run and stop button:
        self.runButton = NevButton(parent=self, label="Run")
        self.stopButton = NevButton(parent=self, label="Stop")
        # The graph:
        self.plot = NevPSAPlot(parent=self, 
                                title = "PSA data graph", 
                                XAxisName="Sweeper",
                                YAxisName=psaData.GetCurPsaMode().GetOperationName(),
                                X=[],
                                Y=[],
                                colors=[],
                                legends=[])

        # ---- BINDINGS:
        self.runButton.Bind(event=wx.EVT_BUTTON, handler=self.OnRunButton)
        self.stopButton.Bind(event=wx.EVT_BUTTON, handler=self.OnStopButton)
        self.comboBoxXAxis.Bind(event=wx.EVT_COMBOBOX, handler=self.OnComboBoxXAxis)

        # ---- SIZERS:
        mainSizerV = wx.BoxSizer(orient=wx.VERTICAL)
        self.controlSizerH = wx.BoxSizer(orient=wx.HORIZONTAL)
        # Sizer addings:
        self.controlSizerH.Add(self.comboBoxXAxisText, flag=wx.ALIGN_CENTER | wx.ALL, border=0)
        self.controlSizerH.Add(self.comboBoxXAxis, flag=wx.ALL | wx.EXPAND, border=3)
        self.controlSizerH.Add(self.runButton, flag=wx.ALL | wx.EXPAND, border=1)
        self.controlSizerH.Add(self.stopButton, flag=wx.ALL | wx.EXPAND, border=1)


        mainSizerV.Add(self.controlSizerH, flag=wx.ALL| wx.EXPAND, proportion=1, border=1)
        mainSizerV.Add(self.plot, flag=wx.ALL | wx.EXPAND, proportion=10, border=1)
        


        # End of innit:
        self.SetSizer(mainSizerV)
        self.SetAutoLayout(1)
        self.ApplyTheme()

# ──────────────────────────────────────────────── METHODS ────────────────────────────────────────────────────

    def UpdatePlot(self, X : list[float], Y : list[list[float]], XAxisName : str, legends : list[str], colors : list[str]):
        """
        Updates the displayed plotting data.
        """
        self.plot.SetX(X), self.plot.SetY(Y)
        self.plot.SetLegends(legends), self.plot.SetColors(colors), self.plot.SetXAxisName(XAxisName)
        self.plot.UpdatePlot()
        
        self.Refresh()
        self.Update()

    def ReplaceChoicesXAxis(self, newChoices : list[str], curSimName : str):
        """
        The ReplaceChoicesXAxis method is called by the SweeperPanel event handler to change the choices possibilities
        when one of the NISCOPE channels is activate / deactivate.

        Parameters:
        ----------
        newChoices : list[str]
        curSimName : str
            The currently selected x axis name for the simulation
        """

        self.comboBoxXAxis.Set(newChoices)
        self.comboBoxXAxis.SetSelection(newChoices.index(curSimName))


    
    
# ──────────────────────────────────────────────── GETTERs ────────────────────────────────────────────────────
    
    def GetPlot(self):
        return self.plot

# ──────────────────────────────────────────────── EVENT HANDLER: ────────────────────────────────────────────────────
    
    def OnRunButton(self, e : wx.Event):
        self.controller.OnPSARunButton()
        
        e.Skip()


    def OnStopButton(self, e : wx.Event):
        self.controller.OnPSAStopButton()

        e.Skip()

    def OnComboBoxXAxis(self, e : wx.Event):
        combo = e.GetEventObject()
        newAx = combo.GetStringSelection()

        self.controller.OnPSAComboBoxXAxis(newAx)

        e.Skip()