#! usr/bin/env python3
# nevclient.views.SweeperPanel.py

# extern modules
import wx
# enums
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
from nevclient.model.Enums.SweepDirection import SweepDirection
from nevclient.model.Enums.SamplingFreq import SamplingFreq
# templates
from nevclient.views.templates.NevPanel import NevPanel
from nevclient.views.templates.NevText import NevSimpleText, NevSimpleBoldText, NevSimpleTextWithColor
from nevclient.views.templates.NevSpinCtrl import NevSpinCtrl
from nevclient.views.templates.NevComboBox import NevComboBox
from nevclient.views.templates.NevCheckBox import NevCheckBox
# NISCOPE
from nevclient.model.config.PSA.ChannelConf import ChannelConf

class SweeperPanel(NevPanel):
    def __init__(self, parent, 
                 controller, 
                 psaData, 
                 colorMap, 
                 *args, **kwargs):
        """
        The SweeperPanel class is a view used inside the entry frame to display information about the sweeper configuration.
        It includes the NISCOPE devices channel connection and voltage / timing configuration to run the PSA.
        """
        super().__init__(parent=parent, *args, **kwargs)
        self.controller = controller


        
        # ---- PANELS
        self.panelSweepAndTimingConfig = NevPanel(parent=self, style=wx.SUNKEN_BORDER)
        self.panelSweepConfig = NevPanel(parent=self.panelSweepAndTimingConfig)
        self.panelTimingConfig = NevPanel(parent=self.panelSweepAndTimingConfig)
        self.panelChannelSetting = NevPanel(parent=self, style=wx.SUNKEN_BORDER)

        # ---- SWEEPER
        # TEXTS
        sweepConfigText = NevSimpleBoldText(parent=self.panelSweepConfig , label="Sweep configuration")
        startText = NevSimpleText(parent=self.panelSweepConfig , label="Start (mV)")
        
        sweepDirectionText = NevSimpleText(parent=self.panelSweepConfig , label="Sweep\ndirection")
        stopText = NevSimpleText(parent=self.panelSweepConfig , label="Stop (mV)")
        stepsText = NevSimpleText(parent=self.panelSweepConfig , label="Steps")

        timingConfigText = NevSimpleBoldText(parent=self.panelTimingConfig, label="Timing configuration")
        initDelayText = NevSimpleText(parent=self.panelTimingConfig, label="Initial\ndelay(ms)")
        periodText = NevSimpleText(parent=self.panelTimingConfig, label="Period(ms)")
        delayText = NevSimpleText(parent=self.panelTimingConfig, label="Delay(ms)")
        samplingText = NevSimpleText(parent=self.panelTimingConfig, label="Sampling(Hz)")

        channelSettingText = NevSimpleBoldText(parent=self.panelChannelSetting, label="Channel settings")

        ncParamText = NevSimpleBoldText(parent=self.panelSweepAndTimingConfig , label="NC Parameter selected:")

        # SPINCTRL
        self.startSpin = NevSpinCtrl(parent=self.panelSweepConfig)
        self.startSpin.SetDigits(3), self.startSpin.SetMax(1000), self.startSpin.SetIncrement(0.001) # V

        self.stopSpin = NevSpinCtrl(parent=self.panelSweepConfig)
        self.stopSpin.SetDigits(3), self.stopSpin.SetMax(1000), self.stopSpin.SetIncrement(0.001)

        self.stepsSpin = NevSpinCtrl(parent=self.panelSweepConfig)
        self.stepsSpin.SetDigits(0), self.stepsSpin.SetMax(1000)
        
        self.initdelaySpin = NevSpinCtrl(parent=self.panelTimingConfig)
        self.initdelaySpin.SetDigits(1), self.initdelaySpin.SetIncrement(0.1)

        self.periodSpin = NevSpinCtrl(parent=self.panelTimingConfig)
        self.periodSpin.SetDigits(1), self.periodSpin.SetIncrement(0.1)

        self.delaySpin = NevSpinCtrl(parent=self.panelTimingConfig)
        self.delaySpin.SetDigits(1), self.delaySpin.SetIncrement(0.1)

        # COMBOBOX:
        self.parameterComboBox = NevComboBox(parent=self.panelSweepAndTimingConfig, 
                                             style=wx.CB_READONLY, 
                                             choices=[]) # will later be updated via the InitUpdateSweeperAfterLoadingParam method
        self.sweepDirectionComboBox = NevComboBox(parent=self.panelSweepConfig, 
                                                  style=wx.CB_READONLY, 
                                                  choices=list(map(str, SweepDirection.get_all_members()))
                                                  )
        self.samplingComboBox = NevComboBox(parent=self.panelTimingConfig, 
                                            style=wx.CB_READONLY, 
                                            choices=list(map(str, SamplingFreq.get_all_members())) # ? to do : switch to real values
                                            )
        self.samplingComboBox.SetSelection(0)


        # ---- CHANNELS:
        self.channelSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.channelSizer.Add(channelSettingText, flag=wx.ALL, border=3)

        self.channelsCouplingComboBox = []
        self.channelsRangeComboBox = []
        self.channelsText = []
        self.channelsOffset = []
        self.channelActive = []
        


        channelConfList = psaData.GetCurPsaMode().GetChnConfList()
        channelRangeChoices = list(map(str,NISCOPEChannelVerticalRange.get_all_members()))
        channelCouplingChoices = list(map(str,NISCOPEChannelVerticalCoupling.get_all_members()))
        for channelC in channelConfList:
            niscopeChannel = channelC.GetNiscopeChn()
            NISCOPEDevice  = niscopeChannel.GetDevice()

            channelCoupling = niscopeChannel.GetVerticalCoupling()
            channelRange    = niscopeChannel.GetVerticalRange()
            channelColor    = colorMap[NISCOPEDevice.GetId()][niscopeChannel.GetIndex()]
            channelActive   = channelC.GetActive()
            channelOffset   = channelC.GetOffset()

            # Text
            channelText = NevSimpleTextWithColor(color=channelColor, 
                                                    parent=self.panelChannelSetting, 
                                                    label=f"Dev {NISCOPEDevice.GetId()} chn {niscopeChannel.GetIndex()}")
            # Channel combo boxes
            couplingComboBox = NevComboBox(parent=self.panelChannelSetting, 
                                            choices=channelCouplingChoices, 
                                            style=wx.CB_READONLY)
            
            couplingComboBox.SetSelection(channelCouplingChoices.index(str(channelCoupling)))
            rangeComboBox = NevComboBox(parent=self.panelChannelSetting, 
                                        choices=channelRangeChoices, 
                                        style=wx.CB_READONLY)
            
            
            rangeComboBox.SetSelection(channelRangeChoices.index(str(channelRange)))
            # Channel offset:
            offset = NevSpinCtrl(parent=self.panelChannelSetting)
            # offset config see oldcode "niscopeChannelBox class, method _channel_line_on_grid"
            offset.SetValue(channelOffset), offset.SetDigits(3), offset.SetMax(10), offset.SetMin(-10)
            
            # Active or not:
            active = NevCheckBox(parent=self.panelChannelSetting)
            active.SetValue(channelActive)

            # Sizer
            channelSizerMainH = wx.BoxSizer(orient=wx.HORIZONTAL)
            channelSizerVLeft = wx.BoxSizer(orient=wx.VERTICAL)
            channelSizerVRight = wx.BoxSizer(orient=wx.VERTICAL)

            channelSizerVLeft.Add(active, flag=wx.ALL, border=0)
            channelSizerVLeft.Add(channelText, flag=wx.ALL, border=1)
            channelSizerVLeft.Add(offset, flag=wx.ALL, border=0)
            channelSizerVRight.Add(couplingComboBox, flag=wx.ALL | wx.EXPAND, border=1)
            channelSizerVRight.Add(rangeComboBox, flag=wx.ALL | wx.EXPAND, border=1)
            
            channelSizerMainH.Add(channelSizerVLeft, flag=wx.ALL, proportion=0, border=1)
            channelSizerMainH.Add(channelSizerVRight, flag=wx.ALL | wx.EXPAND, proportion=2,border=1)

            # Updating class attributes
            self.channelSizer.Add(channelSizerMainH, flag=wx.ALL, border=3)
            self.channelsCouplingComboBox.append(couplingComboBox)
            self.channelsRangeComboBox.append(rangeComboBox)
            self.channelsText.append(channelText)
            self.channelsOffset.append(offset)
            self.channelActive.append(active)


        # ---- SIZERS
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.topSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.ncParamSizer  = wx.BoxSizer(orient=wx.VERTICAL)
        self.ncParamSizer.Add(ncParamText, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=1)
        self.ncParamSizer.Add(self.parameterComboBox)
        
        # Sweep Configuration
        sweepConfigSizer = wx.BoxSizer(orient=wx.VERTICAL)
        sweepConfigSizer.Add(sweepConfigText, flag=wx.BOTTOM | wx.TOP, border=3)

        fgsSweep = wx.FlexGridSizer(rows=4, cols=2, vgap=3, hgap=3) # vgap/hgap pour l'espacement

        fgsSweep.Add(startText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsSweep.Add(self.startSpin, flag=wx.EXPAND)

        fgsSweep.Add(sweepDirectionText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsSweep.Add(self.sweepDirectionComboBox, flag=wx.EXPAND)

        fgsSweep.Add(stopText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsSweep.Add(self.stopSpin, flag=wx.EXPAND)

        fgsSweep.Add(stepsText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsSweep.Add(self.stepsSpin, flag=wx.EXPAND)
        fgsSweep.AddGrowableCol(1, proportion=1)

        sweepConfigSizer.Add(fgsSweep, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.panelSweepConfig.SetSizer(sweepConfigSizer)

        # Timing configuration
        timingConfigSizer = wx.BoxSizer(orient=wx.VERTICAL)
        timingConfigSizer.Add(timingConfigText, flag=wx.BOTTOM | wx.TOP, border=3)

        fgsTiming = wx.FlexGridSizer(rows=4, cols=2, vgap=3, hgap=3)

        fgsTiming.Add(initDelayText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsTiming.Add(self.initdelaySpin, flag=wx.EXPAND)

        fgsTiming.Add(periodText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsTiming.Add(self.periodSpin, flag=wx.EXPAND)

        fgsTiming.Add(delayText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsTiming.Add(self.delaySpin, flag=wx.EXPAND)

        fgsTiming.Add(samplingText, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        fgsTiming.Add(self.samplingComboBox, flag=wx.EXPAND)
        # The second column can take more space
        fgsTiming.AddGrowableCol(1, proportion=1)

        timingConfigSizer.Add(fgsTiming, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        self.panelTimingConfig.SetSizer(timingConfigSizer)



        



        
        self.topSizer.Add(self.ncParamSizer, flag=wx.ALL, border=3)
        self.topSizer.Add(self.panelSweepConfig, flag=wx.ALL, border=1)
        self.topSizer.Add(self.panelTimingConfig, flag=wx.ALL, border=1)
        self.panelSweepAndTimingConfig.SetSizer(self.topSizer)

        
        self.panelChannelSetting.SetSizer(self.channelSizer)

        
        self.mainSizer.Add(self.panelSweepAndTimingConfig, flag=wx.ALL, border=3)
        self.mainSizer.Add(self.panelChannelSetting, flag=wx.ALL, border=3)


        # ---- BINDINGS
        # Sweeper
        self.parameterComboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingParameterName)
        self.startSpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingStart)
        self.stopSpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingStop)
        self.stepsSpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingSteps)
        self.sweepDirectionComboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingSweepDirection)
        # Timing
        self.delaySpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingDelay)
        self.initdelaySpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingInitDelay)
        self.periodSpin.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingPeriod)
        self.samplingComboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingSampling)
        # Channel 
        for comboBox in self.channelsCouplingComboBox:
            comboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingCouplingChannel)
        for comboBox in self.channelsRangeComboBox:
            comboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingRangeChannel)
        for spinCtrl in self.channelsOffset:
            spinCtrl.Bind(event=wx.EVT_SPINCTRLDOUBLE, handler=self.OnChangingOffsetChannel)
        for checkbox in self.channelActive:
            checkbox.Bind(event=wx.EVT_CHECKBOX, handler=self.OnChangingActiveChannel)


        # ---- END OF INNIT
        self.ApplyTheme()
        self.SetSizer(self.mainSizer)
        self.SetAutoLayout(True)

    # ────────────────────────────────────────────────── Methods  ───────────────────────────────────────────────────────────────

    def UpdateStart(self, value : float):
        self.startSpin.SetValue(value)
    def UpdateStop(self, value : float):
        self.stopSpin.SetValue(value)
    def UpdateSteps(self, value : int):
        self.stepsSpin.SetValue(value)

    # ────────────────────────────────────────────────── EVENT HANDLERS  ────────────────────────────────────────────────────────
    # ---- SWEEP CONF
    def OnChangingParameterName(self, e):
        comboBox = e.GetEventObject()
        curParam = comboBox.GetStringSelection()
        self.controller.OnSweeperChangingParameterName(curParam)
        e.Skip()
        
    def OnChangingStart(self, e):
        spinCtrl = e.GetEventObject()
        newStart = float(spinCtrl.GetValue())
        self.controller.OnSweeperChangingStart(newStart)

        e.Skip()
    
    def OnChangingStop(self, e):
        spinCtrl = e.GetEventObject()
        newStop  = float(spinCtrl.GetValue())
        self.controller.OnSweeperChangingStop(newStop)
        
        e.Skip()
    
    def OnChangingSteps(self, e):
        spinCtrl = e.GetEventObject()
        newSteps = int(spinCtrl.GetValue())
        self.controller.OnSweeperChangingSteps(newSteps)
        
        e.Skip()
    
    def OnChangingSweepDirection(self, e):
        comboBox          = e.GetEventObject()
        newSweepDirection = SweepDirection.from_string(comboBox.GetStringSelection())
        self.controller.OnSweeperChangingSweepDi(newSweepDirection)

        e.Skip()

    # ---- TIMING CONF
    def OnChangingDelay(self, e):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnSweeperChangingDelay(val)

        e.Skip()

    def OnChangingInitDelay(self, e):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnSweeperChangingInitDelay(val)

        e.Skip()

    def OnChangingPeriod(self, e):
        spinCtrl = e.GetEventObject()
        val      = float(spinCtrl.GetValue())
        self.controller.OnSweeperChangingPeriod(val)

        e.Skip()
    
    def OnChangingSampling(self, e):
        comboBox = e.GetEventObject()
        sampling = SamplingFreq.from_string(comboBox.GetStringSelection())
        self.controller.OnSweeperChangingSampling(sampling)

        e.Skip()

    # ---- CHANNEL CONF
    def OnChangingCouplingChannel(self, e):
        comboBox    = e.GetEventObject()
        newCoupling = NISCOPEChannelVerticalCoupling.from_string(comboBox.GetStringSelection())
        chnConfId   = self.channelsCouplingComboBox.index(comboBox)
        self.controller.OnSweeperChangingCouplingChannel(newCoupling, chnConfId)

        e.Skip()

    def OnChangingRangeChannel(self, e):
        comboBox = e.GetEventObject()
        newRange =NISCOPEChannelVerticalRange.from_string(comboBox.GetStringSelection())
        chnConfId   = self.channelsRangeComboBox.index(comboBox)
        self.controller.OnSweeperChangingRangeChannel(newRange, chnConfId)

        e.Skip()
    
    def OnChangingOffsetChannel(self, e):
        spinCtrl = e.GetEventObject()
        newOffsetValue = float(spinCtrl.GetValue())
        chnConfId   = self.channelsOffset.index(spinCtrl)
        self.controller.OnSweeperChangingOffsetChannel(newOffsetValue, chnConfId)
        e.Skip()

    def OnChangingActiveChannel(self, e):
        checkbox = e.GetEventObject()
        checked = e.IsChecked()
        chnConfId   = self.channelActive.index(checkbox)
        self.controller.OnSweeperChangingActiveChannel(checked, chnConfId)

        e.Skip()


    
        
    # ────────────────────────────────────────────────── METHODS ────────────────────────────────────────────────────────
    
    def InitUpdateSweeperAfterLoadingParam(self, choicesName : list[str], 
                                           curParamName : str,
                                           start : float , 
                                           stop : float, 
                                           steps : int, 
                                           sweepDi : SweepDirection):
        """
        This method is used by the controller to update the choices
        of the parameter combobox after the user loaded csv parameters.
        It also updates the corresponding start, stop and steps param.

        Parameters
        ----------
        choicesName  : list[str]
            The list of all the parameters you can select in the combobox
        curParamName : str
            The selection for the choices'names.
        start        : float
        stop         : float
        steps        : int
        sweepDi      : SweepDirection
            The different configuration settings.
        """
        # Parameter box
        self.parameterComboBox.Set(choicesName)
        self.parameterComboBox.SetSelection(choicesName.index(curParamName))
        # Start
        self.startSpin.SetValue(start)
        # Stop
        self.stopSpin.SetValue(stop)
        # Steps
        self.stepsSpin.SetValue(steps)
        # sweep dir
        self.sweepDirectionComboBox.SetSelection(SweepDirection.get_all_members().index(sweepDi))
        

        # Forcing the updates of the panel:
        self.Layout()
        self.Refresh()
        self.Update()

    

    # ────────────────────────────────────────────────── SETTER ────────────────────────────────────────────────────────

    def SetStartValue(self, value: float):
        self.startSpin.SetValue(value)

    
