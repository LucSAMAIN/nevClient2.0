#! usr/env/bin python3
# nevclient.views.PulsePanel.py

# extern modules
import wx
# templates
from nevclient.views.templates.NevPanel import NevPanel
from nevclient.views.templates.NevSpinCtrl import NevSpinCtrl
from nevclient.views.templates.NevPulsePlot import NevPulsePlot
from nevclient.views.templates.NevText import NevSimpleText, NevSimpleBoldText
from nevclient.views.templates.NevCheckBox import NevCheckBox
from nevclient.views.templates.NevComboBox import NevComboBox
# pulse data
from nevclient.model.config.Pulse.PulseData import PulseData
from nevclient.model.config.Pulse.PulseConf import PulseConf
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter

class PulsePanel(NevPanel):
    def __init__(self, 
                 parent, 
                 controller, 
                 *args, 
                 **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        # ---- ATTRIBUTES
        self.controller = controller

        # ---- WIDGETS    
        # SpinCtrl       
        self.pulse1DelaySpinCtrl = NevSpinCtrl(parent=self)
        self.pulse1WidthSpinCtrl = NevSpinCtrl(parent=self)
        self.pulse1AmpSpinCtrl = NevSpinCtrl(parent=self)
        self.pulse1DelaySpinCtrl.SetMax(20), self.pulse1DelaySpinCtrl.SetMin(0), self.pulse1DelaySpinCtrl.SetDigits(1)
        self.pulse1WidthSpinCtrl.SetMax(10), self.pulse1WidthSpinCtrl.SetMin(0), self.pulse1WidthSpinCtrl.SetDigits(1)
        self.pulse1AmpSpinCtrl.SetMax(1000), self.pulse1AmpSpinCtrl.SetMin(0), self.pulse1AmpSpinCtrl.SetDigits(1)
        
        self.pulse2DelaySpinCtrl = NevSpinCtrl(parent=self)
        self.pulse2WidthSpinCtrl = NevSpinCtrl(parent=self)
        self.pulse2AmpSpinCtrl = NevSpinCtrl(parent=self)
        self.pulse2DelaySpinCtrl.SetMax(20), self.pulse2DelaySpinCtrl.SetMin(0), self.pulse2DelaySpinCtrl.SetDigits(1)
        self.pulse2WidthSpinCtrl.SetMax(10), self.pulse2WidthSpinCtrl.SetMin(0), self.pulse2WidthSpinCtrl.SetDigits(1)
        self.pulse2AmpSpinCtrl.SetMax(1000), self.pulse2AmpSpinCtrl.SetMin(0), self.pulse2AmpSpinCtrl.SetDigits(1)
        
        self.delaysSpinCtrl = list()
        self.widthsSpinCtrl = list()
        self.ampsSpinCtrl   = list()
        self.delaysSpinCtrl.append(self.pulse1DelaySpinCtrl), self.delaysSpinCtrl.append(self.pulse2DelaySpinCtrl)
        self.widthsSpinCtrl.append(self.pulse1WidthSpinCtrl), self.widthsSpinCtrl.append(self.pulse2WidthSpinCtrl)
        self.ampsSpinCtrl.append(self.pulse1AmpSpinCtrl), self.ampsSpinCtrl.append(self.pulse2AmpSpinCtrl)
        # For common stim:
        self.dtSpinCtrl = NevSpinCtrl(parent=self)
        self.dtSpinCtrl.SetValue(0.01), self.dtSpinCtrl.SetDigits(2), self.dtSpinCtrl.SetIncrement(0.01)
        self.TSpinCtrl = NevSpinCtrl(parent=self)
        self.TSpinCtrl.SetValue(20), self.TSpinCtrl.SetDigits(0), self.TSpinCtrl.SetIncrement(1), self.TSpinCtrl.SetMax(100), self.TSpinCtrl.SetMin(1)
        # Text for common stim:
        self.stimTitle = NevSimpleBoldText(parent=self, label="Common stimulus for DAQMX dynamic devices:")
        self.dtText = NevSimpleText(parent=self, label="Δt(ms)")
        self.TText = NevSimpleText(parent=self, label="T(ms)")
        # Combo Parameter box
        self.choicesText = NevSimpleText(parent=self, label="Parameter")
        self.paramComboB = NevComboBox(parent=self, choices=[], style=wx.CB_READONLY) # later set up
        # CheckBox
        self.pulse1CheckBox = NevCheckBox(parent=self)
        self.pulse1CheckBox.SetValue(False) # default value see old code

        self.pulse2CheckBox = NevCheckBox(parent=self)
        self.pulse2CheckBox.SetValue(False)

        self.activesCheckBox  = list()
        self.activesCheckBox.append(self.pulse1CheckBox), self.activesCheckBox.append(self.pulse2CheckBox)

        # Plot
        self.pulsePlot = NevPulsePlot(parent=self, id=wx.ID_ANY, title="Pulse set up vizualisation",
                                      nbPulses=0,
                                      delays=[],
                                      widths=[],
                                      amps=[], 
                                      colors = []
                                    )



        # ---- BINDINGS:
        # for common stim:
        self.TSpinCtrl.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangeDuration)
        self.dtSpinCtrl.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangeDt)        
        # Param choices
        self.paramComboB.Bind(wx.EVT_COMBOBOX, self.OnChangingParamBox)
        # Pulse 1
        self.pulse1DelaySpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingDelay1)
        self.pulse1WidthSpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingWidth1)
        self.pulse1AmpSpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingAmp1)
        self.pulse1CheckBox.Bind(wx.EVT_CHECKBOX, self.OnChangingActive1)
        # Pulse 2
        self.pulse2DelaySpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingDelay2)
        self.pulse2WidthSpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingWidth2)
        self.pulse2AmpSpinCtrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnChangingAmp2)
        self.pulse2CheckBox.Bind(wx.EVT_CHECKBOX, self.OnChangingActive2)
                

        # ---- SIZER
        pulseSizer = wx.BoxSizer(orient=wx.VERTICAL)

        paramChoicesSizerRow = wx.BoxSizer(wx.HORIZONTAL)
        paramChoicesSizerRow.Add(self.choicesText, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=3)
        paramChoicesSizerRow.Add(self.paramComboB, proportion=2, flag=wx.ALL|wx.EXPAND, border=3)

        pulseSizer.Add(paramChoicesSizerRow, flag=wx.EXPAND)

        pulseSizer.Add(self.pulsePlot, proportion=2, flag=wx.EXPAND | wx.ALL, border=0)

        pulseControlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        pulse1ControlSizer = wx.BoxSizer(orient=wx.VERTICAL)
        pulse1CheckBoxTextSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse1CheckBoxTextSizer.Add(self.pulse1CheckBox, flag= wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse1CheckBoxTextSizer.Add(NevSimpleText(parent=self, label="First pulse settings"))
        
        pulse1ControlSizerDelay = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse1ControlSizerWidth = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse1ControlSizerAmp = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        pulse1ControlSizerDelay.Add(NevSimpleText(parent=self, label="Delay (ms)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse1ControlSizerDelay.Add(self.pulse1DelaySpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)

        pulse1ControlSizerWidth.Add(NevSimpleText(parent=self, label="Width (ms)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse1ControlSizerWidth.Add(self.pulse1WidthSpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)

        pulse1ControlSizerAmp.Add(NevSimpleText(parent=self, label="Amp (mV)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse1ControlSizerAmp.Add(self.pulse1AmpSpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        
        pulse1ControlSizer.Add(pulse1CheckBoxTextSizer, flag=wx.BOTTOM | wx.ALIGN_CENTER, border=5)
        pulse1ControlSizer.Add(pulse1ControlSizerDelay, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        pulse1ControlSizer.Add(pulse1ControlSizerWidth, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        pulse1ControlSizer.Add(pulse1ControlSizerAmp, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        
        pulseControlSizer.Add(pulse1ControlSizer,proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)
        


        pulse2ControlSizer = wx.BoxSizer(orient=wx.VERTICAL)
        pulse2CheckBoxTextSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse2CheckBoxTextSizer.Add(self.pulse2CheckBox, flag= wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse2CheckBoxTextSizer.Add(NevSimpleText(parent=self, label="Second pulse settings"))
        
        pulse2ControlSizerDelay = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse2ControlSizerWidth = wx.BoxSizer(orient=wx.HORIZONTAL)
        pulse2ControlSizerAmp = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        pulse2ControlSizerDelay.Add(NevSimpleText(parent=self, label="Delay (ms)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse2ControlSizerDelay.Add(self.pulse2DelaySpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)

        pulse2ControlSizerWidth.Add(NevSimpleText(parent=self, label="Width (ms)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse2ControlSizerWidth.Add(self.pulse2WidthSpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)

        pulse2ControlSizerAmp.Add(NevSimpleText(parent=self, label="Amp (mV)"), flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)
        pulse2ControlSizerAmp.Add(self.pulse2AmpSpinCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        
        pulse2ControlSizer.Add(pulse2CheckBoxTextSizer, flag=wx.BOTTOM | wx.ALIGN_CENTER, border=5)
        pulse2ControlSizer.Add(pulse2ControlSizerDelay, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        pulse2ControlSizer.Add(pulse2ControlSizerWidth, flag=wx.ALL | wx.ALIGN_CENTER, border=0)
        pulse2ControlSizer.Add(pulse2ControlSizerAmp, flag=wx.ALL | wx.ALIGN_CENTER, border=0)

        pulseControlSizer.Add(pulse2ControlSizer, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)


        pulseSizer.Add(pulseControlSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Stim common:
        StimMainSizerV = wx.BoxSizer(wx.VERTICAL)

        stimTitleSizer = wx.BoxSizer(wx.HORIZONTAL)
        stimTitleSizer.Add(self.stimTitle, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=3)


        stimTSizerRow = wx.BoxSizer(wx.HORIZONTAL)
        stimTSizerRow .Add(self.TText, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=3)
        stimTSizerRow .Add(self.TSpinCtrl, proportion=2, flag=wx.ALL|wx.EXPAND, border=3)

        stimdtSizerRow = wx.BoxSizer(wx.HORIZONTAL)
        stimdtSizerRow.Add(self.dtText, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=3)
        stimdtSizerRow.Add(self.dtSpinCtrl, proportion=2, flag=wx.ALL|wx.EXPAND, border=3)

        StimMainSizerV.Add(stimTitleSizer, flag=wx.ALL|wx.EXPAND)
        StimMainSizerV.Add(stimTSizerRow , flag=wx.ALL|wx.EXPAND)
        StimMainSizerV.Add(stimdtSizerRow, flag=wx.ALL|wx.EXPAND)

        pulseSizer.Add(StimMainSizerV, proportion=1, flag=wx.ALL|wx.EXPAND, border=0)
        pulseSizer.AddStretchSpacer(1)   


        
        
        self.SetSizer(pulseSizer)
        self.SetAutoLayout(True)
        
# ──────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────


    def UpdateOnLoadingParameters(self, pulseData : PulseData):
        choices = [paramName for paramName in list(pulseData.GetParamToPulsesConfigurationMap().keys())]
        if not choices:
            return
        # Set the choices for the combo box!
        self.paramComboB.Set(choices)
        
        self.UpdateAll(pulseData)
    
    def UpdatePlot(self, pulseData : PulseData):
        """
        The UpdatePlot method is used to update the pulses vizualisation plot.
        It recovers the PulseData instance via the controller to retrieve all the
        configuration settings.
        """
        PData : PulseData = pulseData
        param = PData.GetCurParameter()
        pulsesColor = ['red', 'blue']
        T = pulseData.GetStimData().GetT()
        
        nbActivePulses = 0
        colors         = []
        delays         = []
        widths         = []
        amps           = []
        PConf : PulseConf
        for i, PConf in enumerate(PData.GetParamToPulsesConfigurationMap()[param.GetName()]):
            if PConf.GetActive():
                delays.append(PConf.GetDelay())
                widths.append(PConf.GetWidth())
                amps.append(PConf.GetAmp())
                colors.append(pulsesColor[i])
                nbActivePulses += 1
        
        self.pulsePlot.UpdateData(nbPulses=nbActivePulses, delays=delays, widths=widths, amps=amps, colors=colors, T=T)
        self.Refresh()
        self.Update()

    def UpdateAll(self, pulseData : PulseData):
        """
        This methods update all the widget present
        on the pulse panel.
        """
        # First recover the important data:
        PData : PulseData = pulseData
        
        param  : CSVParameter       = PData.GetCurParameter()
        pulse1 : PulseConf          = PData.GetParamToPulsesConfigurationMap()[param.GetName()][0]
        pulse2 : PulseConf          = PData.GetParamToPulsesConfigurationMap()[param.GetName()][1]

        pulse1Delay = pulse1.GetDelay()
        pulse2Delay = pulse2.GetDelay()

        pulse1Amp   = pulse1.GetAmp()
        pulse2Amp   = pulse2.GetAmp()

        pulse1Width = pulse1.GetWidth()
        pulse2Width = pulse2.GetWidth()
        
        # parameter combobox:
        choices = [paramName for paramName in list(PData.GetParamToPulsesConfigurationMap().keys())]
        self.paramComboB.SetSelection(choices.index(param.GetName()))
        # checkboxes:
        self.pulse1CheckBox.SetValue(pulse1.GetActive())
        self.pulse2CheckBox.SetValue(pulse2.GetActive())
        # delays:
        self.pulse1DelaySpinCtrl.SetValue(pulse1Delay)
        self.pulse2DelaySpinCtrl.SetValue(pulse2Delay)
        # amps:
        self.pulse1AmpSpinCtrl.SetValue(pulse1Amp)
        self.pulse2AmpSpinCtrl.SetValue(pulse2Amp)
        # widths:
        self.pulse1WidthSpinCtrl.SetValue(pulse1Width)
        self.pulse2WidthSpinCtrl.SetValue(pulse2Width)
        # plot:
        self.UpdatePlot(pulseData)


# ──────────────────────────────────────────────── Event handler methods ─────────────────────────────────────────────────────

    # ---- COMMON STIMULUS 
    def OnChangeDuration(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        duration = spinCtrl.GetValue()
        self.controller.OnPulseChangeDuration(duration)
        
        e.Skip()
    
    def OnChangeDt(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        dt = spinCtrl.GetValue()
        self.controller.OnPulseChangeDt(dt)
        
        e.Skip()

    # ---- PULSE CONF
    def OnChangingParamBox(self, e : wx.Event):
        comboBox = e.GetEventObject()
        newName  = comboBox.GetStringSelection()
        self.controller.OnPulseChangingParamBox(newName)

        e.Skip()
    
    def OnChangingAmp1(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingAmp(pulseId=0, amp=val)

        e.Skip()

    def OnChangingAmp2(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingAmp(pulseId=1, amp=val)
        
        e.Skip()

    def OnChangingDelay1(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingDelay(pulseId=0, delay=val)
        
        e.Skip()

    def OnChangingDelay2(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingDelay(pulseId=1, delay=val)
        
        e.Skip()


    def OnChangingWidth1(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingWidth(pulseId=0, width=val)
        
        e.Skip()


    def OnChangingWidth2(self, e : wx.Event):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnPulseChangingWidth(pulseId=1, width=val)
        
        e.Skip()

    def OnChangingActive1(self, e : wx.Event):
        checkBox = e.GetEventObject()
        val      = bool(checkBox.IsChecked())
        self.controller.OnPulseChangingActive(pulseId=0, active=val)
        
        e.Skip()

    def OnChangingActive2(self, e : wx.Event):
        checkBox = e.GetEventObject()
        val      = bool(checkBox.IsChecked())
        self.controller.OnPulseChangingActive(pulseId=1, active=val)
        
        e.Skip()









    
        
        
