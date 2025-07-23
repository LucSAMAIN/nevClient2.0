#! usr/env/bin python3
# nevclient.Controller

# extern modules
import os
import wx
# factories
from nevclient.factories.ParametersFactory import ParametersFactory
from nevclient.factories.PulseFactory import PulseFactory
# logger
from nevclient.utils.Logger import Logger
from nevclient.utils.Logger import log_debug_event
# csv worker
from nevclient.utils.CSVWorker import CSVWorker
# NISCOPE
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
# views
from nevclient.views.EntryFrame import EntryFrame
from nevclient.views.ParametersPanel import ParametersPanel
# psa
from nevclient.model.config.PSA.PSAData import PSAData
from nevclient.model.config.PSA.PSAMode import PSAMode
from nevclient.model.config.PSA.SweepConf import SweepConf
from nevclient.model.config.PSA.TimingConf import TimingConf
from nevclient.model.config.PSA.ChannelConf import ChannelConf
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# enums
from nevclient.model.Enums.SweepDirection import SweepDirection
from nevclient.model.Enums.SamplingFreq import SamplingFreq
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
# services
from nevclient.services.DataManipulation.DAQMXDataServices import DAQMXDataServices
from nevclient.services.DataManipulation.PSADataServices import PSADataServices
from nevclient.services.DataManipulation.PulseDataServices import PulseDataServices
from nevclient.services.DataManipulation.NISCOPEDataServices import NISCOPEDataServices
from nevclient.services.Communication.DAQMXComm import DAQMXComm
# pulses
from nevclient.model.config.Pulse.PulseData import PulseData
from nevclient.model.config.Pulse.PulseConf import PulseConf

class Controller():
    """
    Stores the main data structures.
    Handles the interactions between the user and the views.

    Attributes
    ----------
    niscopeSys    : NISCOPESys
    daqmxSys      : DAQMXSys
    psaData       : PSAData
    paramFac      : ParametersFactory
    psaDMServ     : PSADataServices
    daqmxComm     : DAQMXComm
    pulseFac      : PulseFactory
    pulseDMServ   : PulseDataServices
    niscopeDMServ : NISCOPEDataServices
    """

    def __init__(self,
                 niscopeSys    : NISCOPESys,
                 daqmxSys      : DAQMXSys,
                 psaData       : PSAData,
                 paramFac      : ParametersFactory,
                 psaDMServ     : PSADataServices,
                 daqmxComm     : DAQMXComm,
                 daqmxDMServ   : DAQMXDataServices,
                 pulseFac      : PulseFactory,
                 pulseDMServ   : PulseDataServices,
                 niscopeDMServ : NISCOPEDataServices):
        self.logger = Logger("Controller")

        self.paramFac      = paramFac
        self.pulseFac      = pulseFac
  
        self.niscopeSys    = niscopeSys
        self.daqmxSys      = daqmxSys
        self.psaData       = psaData
   
        self.psaDMServ     = psaDMServ
        self.daqmxDMServ   = daqmxDMServ
        self.pulseDMServ   = pulseDMServ
        self.niscopeDMServ = niscopeDMServ

        self.daqmxComm     = daqmxComm
        
        self.entryFrame     : EntryFrame     = None # later set
        self.parametersData : ParametersData = None # same
        self.csvWorker      : CSVWorker      = None # same
        self.pulseData      : PulseData      = None
        


# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetNiscopeSys(self, newNiscopeSys: NISCOPESys):
        self.niscopeSys = newNiscopeSys

    def SetDaqmxSys(self, newDaqmxSys: DAQMXSys):
        self.daqmxSys = newDaqmxSys

    def SetPsaData(self, newPsaData: PSAData):
        self.psaData = newPsaData

    def SetEntryFrame(self, newEntryFrame: EntryFrame):
        self.entryFrame = newEntryFrame

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetNiscopeSys(self) -> NISCOPESys:
        return self.niscopeSys

    def GetDaqmxSys(self) -> DAQMXSys:
        return self.daqmxSys
    
    def GetPsaData(self) -> PSAData:
        return self.psaData

    def GetEntryFrame(self) -> EntryFrame:
        return self.entryFrame

# ──────────────────────────────────────────────────────────── Event handlers ──────────────────────────────────────────────────────────
# ---- ENTRY FRAME
    def OnEntryFrameOpenItemParametersMenu(self, fileName : str, dirName : str):
        # ---- Manipulation of the model:
        # Build the parameters data
        filePath : str = os.path.join(dirName, fileName)
        self.csvWorker = CSVWorker(filePath)
        self.parametersData = self.paramFac.BuildParametersData(self.csvWorker, self.daqmxSys)
        # Update the sweeper configuration part:
        psaMode : PSAMode
        for psaMode in self.psaData.GetPsaModeMap().values():
            self.psaDMServ.UpdatePSAModelAfterLoadingParameters(psaMode=psaMode,
                                                                csv=self.csvWorker,
                                                                tag=psaMode.GetTag(),
                                                                parametersData=self.parametersData)
        # Build the pulse data instance:
        self.pulseData = self.pulseFac.BuildPulseData(self.parametersData)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)



        # ---- And then we can update the different views
        # Parameters panel & Entry frame
        parametersPanel = ParametersPanel(parent=self.entryFrame.GetPanel(), 
                                          controller=self, 
                                          style=wx.SUNKEN_BORDER,
                                          parametersData=self.parametersData)  
        self.entryFrame.ReplaceParametersPanel(parametersPanel)  
        self.entryFrame.Layout()
        # Sweeper panel:
        curPSAMode : PSAMode        = self.psaData.GetCurPsaMode()
        choices    : list[str]      = list(curPSAMode.GetSweepMap().keys())
        curParam   : CSVParameter   = curPSAMode.GetCurParam()
        sweepConf  : SweepConf      = curPSAMode.GetSweepMap()[curParam.GetName()]
        start, stop, steps, sweepDi = sweepConf.GetStart(), sweepConf.GetStop(), sweepConf.GetSteps(), sweepConf.GetSweepDi()
        self.entryFrame.GetSweeperPanel().InitUpdateSweeperAfterLoadingParam(choices,
                                                                             curParam.GetName(),
                                                                             start,
                                                                             stop,
                                                                             steps,
                                                                             sweepDi)
        # Pulse panel
        self.entryFrame.GetPulsePanel().UpdateOnLoadingParameters(self.pulseData)
        

        
        


# ---- SWEEPER PANEL
    # SWEEPER CONF
    @log_debug_event
    def OnSweeperChangingParameterName(self, newParameter : str):
        # Update the model:
        # First retrieve the CSV parameter:
        param : CSVParameter = self.parametersData.GetParametersMap()[newParameter]
        # Then recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # Finally updates the model accordingly:
        psaMode.SetCurParam(param)
        
        # We also need to update the view:
        sweepView = self.entryFrame.GetSweeperPanel()
        sweepData : SweepConf = psaMode.GetSweepMap()[param.GetName()]
        start, stop, steps = sweepData.GetStart(), sweepData.GetStop(), sweepData.GetSteps()
        sweepView.UpdateStart(start), sweepView.UpdateStop(stop), sweepView.UpdateSteps(steps)
    
    @log_debug_event
    def OnSweeperChangingStart(self, start : float):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the current param:
        param : CSVParameter = psaMode.GetCurParam()
        # and the binded sweep conf:
        sweepConf : SweepConf = psaMode.GetSweepMap()[param.GetName()]
        # Then updates the model accordingly:
        sweepConf.SetStart(start)

    @log_debug_event
    def OnSweeperChangingStop(self, stop : float):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the current param:
        param : CSVParameter = psaMode.GetCurParam()
        # and the binded sweep conf:
        sweepConf : SweepConf = psaMode.GetSweepMap()[param.GetName()]
        # Then updates the model accordingly:
        sweepConf.SetStop(stop)

    @log_debug_event
    def OnSweeperChangingSteps(self, steps : int):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the current param:
        param : CSVParameter = psaMode.GetCurParam()
        # and the binded sweep conf:
        sweepConf : SweepConf = psaMode.GetSweepMap()[param.GetName()]
        # Then updates the model accordingly:
        sweepConf.SetSteps(steps)
    
    @log_debug_event
    def OnSweeperChangingSweepDi(self, sweepDi : SweepDirection):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the current param:
        param : CSVParameter = psaMode.GetCurParam()
        # and the binded sweep conf:
        sweepConf : SweepConf = psaMode.GetSweepMap()[param.GetName()]
        # Then updates the model accordingly:
        sweepConf.SetSweepDi(sweepDi)



    # TIMING CONF
    @log_debug_event
    def OnSweeperChangingDelay(self, delay : float):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the corresponding timing conf:
        timeConf : TimingConf = psaMode.GetTiming()
        # Then updates the model accordingly:
        timeConf.SetDelay(delay)
    
    @log_debug_event
    def OnSweeperChangingInitDelay(self, initDelay : float):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the corresponding timing conf:
        timeConf : TimingConf = psaMode.GetTiming()
        # Then updates the model accordingly:
        timeConf.SetInDelay(initDelay)

    @log_debug_event
    def OnSweeperChangingPeriod (self, period : float):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the corresponding timing conf:
        timeConf : TimingConf = psaMode.GetTiming()
        # Then updates the model accordingly:
        timeConf.SetPeriod(period)

    @log_debug_event
    def OnSweeperChangingSampling(self, sampling : SamplingFreq):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode    = self.psaData.GetCurPsaMode()
        # and the corresponding timing conf:
        timeConf : TimingConf = psaMode.GetTiming()
        # Then updates the model accordingly:
        timeConf.SetSampling(sampling)



    # CHANNEL CONF
    @log_debug_event
    def OnSweeperChangingCouplingChannel(self, newCoupling : NISCOPEChannelVerticalCoupling, chnConfId : int):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode     = self.psaData.GetCurPsaMode()
        # and the corresponding channel conf:
        chnConf : ChannelConf = psaMode.GetChnConfList()[chnConfId]
        # Then updates the model accordingly:
        chnConf.SetVerticalCoupling(newCoupling)

    @log_debug_event
    def OnSweeperChangingRangeChannel(self, newRange : NISCOPEChannelVerticalRange, chnConfId : int):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode     = self.psaData.GetCurPsaMode()
        # and the corresponding channel conf:
        chnConf : ChannelConf = psaMode.GetChnConfList()[chnConfId]
        # Then updates the model accordingly:
        chnConf.SetVerticalRange(newRange)

    @log_debug_event
    def OnSweeperChangingOffsetChannel(self, newOffsetValue : float, chnConfId : int):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode     = self.psaData.GetCurPsaMode()
        # and the corresponding channel conf:
        chnConf : ChannelConf = psaMode.GetChnConfList()[chnConfId]
        # Then updates the model accordingly:
        chnConf.SetOffset(newOffsetValue)

    @log_debug_event
    def OnSweeperChangingActiveChannel(self, checked : bool, chnConfId : int):
        # Update the model
        # First recover the current psa mode instance
        psaMode : PSAMode     = self.psaData.GetCurPsaMode()
        # and the corresponding channel conf:
        chnConf : ChannelConf = psaMode.GetChnConfList()[chnConfId]
        # Then updates the model accordingly:
        chnConf.SetActive(checked)

        # We also need to update the psa panel accordingly:
        activeConfs = self.psaDMServ.GetActiveChannelsConfigurationList(self.psaData.GetCurPsaMode())
        legends     = list(map(self.psaDMServ.GenerateLegends, activeConfs))
        choices     = ["Sweeper"] + legends
        # check if the active changement has an impact
        # on the currenlty selected axis:
        if self.psaData.GetCurPsaMode().GetPsaSimulation().GetXAxisName() not in choices:
            self.psaData.GetCurPsaMode().GetPsaSimulation().SetXAxisName("Sweeper")
        curSelectionStr = self.psaData.GetCurPsaMode().GetPsaSimulation().GetXAxisName()
        # update the view
        self.entryFrame.GetPSAPanel().ReplaceChoicesXAxis(choices, curSelectionStr)
        # update the plot
        X, Y   = self.psaDMServ.GetXData(self.psaData.GetCurPsaMode().GetPsaSimulation()), self.psaDMServ.GetYData(self.psaData.GetCurPsaMode())
        colors = [self.psaDMServ.GetColor(conf=activeConf,
                                          psaSim=self.psaData.GetCurPsaMode().GetPsaSimulation(), 
                                          niscopeDMServ=self.niscopeDMServ,
                                          niscopeSys=self.niscopeSys) for activeConf in activeConfs]
        self.entryFrame.GetPSAPanel().GetPlot().UpdateData(X=X,
                                                           Y=Y,
                                                           XAxisName=curSelectionStr,
                                                           legends=legends,
                                                           colors=colors)
        self.entryFrame.GetPSAPanel().GetPlot().UpdatePlot()





# ---- Parameters panel
    @log_debug_event
    def OnParametersChangingSetUp(self, newSetupName : str):
        self.parametersData.SetCurSetup(newSetupName)
        # Update the view:
        self.entryFrame.GetParametersPanel().FillGrid(self.parametersData)
    
    @log_debug_event
    def OnParametersCellChanged(self, row : int, col : int):
        paramNames = list(self.parametersData.GetParametersMap().keys())
        if col == 0: # ignore edits outside second column
            self.entryFrame.GetParametersPanel().SetGridValue(row, col, paramNames[row])  # reset to original value
            return
        if col == 2: # ignore edits outside second column
            self.entryFrame.GetParametersPanel().SetGridValue(row, col, "+")
            return
        if col == 3: # ignore edits outside second column
            self.entryFrame.GetParametersPanel().SetGridValue(row, col, "-")
            return

        setupName = self.parametersData.GetCurSetup()
        paramName = self.entryFrame.GetParametersPanel().GetGridValue(row, 0)

        csvParam : CSVParameter = self.parametersData.GetParametersMap()[paramName]
        try:
            newValue = float(self.entryFrame.GetParametersPanel().GetGridValue(row, 1))
        except ValueError:
            wx.MessageBox(f"Invalid value entered for '{paramName}'. Please enter a valid number.", 
                          "Input Error", wx.OK | wx.ICON_ERROR)

            oldValue = str(csvParam.GetSetupsValues().get(setupName, "???"))
            self.entryFrame.GetParametersPanel().SetGridValue(row, 1, oldValue)
            return
        except Exception as e:
            wx.MessageBox(f"An error occurred: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            oldValue = str(csvParam.GetSetupsValues().get(setupName, "???"))
            self.entryFrame.GetParametersPanel().SetGridValue(row, 1, oldValue)
            return
        

        # Update the model:
        csvParam.GetSetupsValues()[setupName] = newValue

    @log_debug_event
    def OnParametersSave(self, filePath : str):
        self.csvWorker.SaveToCSV(filePath=filePath, parametersData=self.parametersData)

    @log_debug_event
    def OnParametersGridCellClick(self, row : int, col : int):
        # Only works for the "+" and "-" columns (2 and 3)
        if col != 2 and col != 3:
            return
        
        paramName = self.entryFrame.GetParametersPanel().GetGridValue(row, 0)
        currentValueStr = self.entryFrame.GetParametersPanel().GetGridValue(row, 1)
        def _count_decimal_places(stringNumber):
            """
            This method counts the number of decimal places in a number.

            Parameters
            ----------
            stringNumber : str
                The input string of the number.

            Returns
            -------
            int : 
                The number of decimal places.
            """
            if '.' in stringNumber:
                return len(stringNumber.split('.')[-1])
            return 0
        
        try:
            digitPrecision = _count_decimal_places(currentValueStr)
            currentValue = float(currentValueStr) # now that we have the precision, we can convert it to float for the operation                

            if col == 2: # Clic on "+"
                newValue = currentValue + 10**-digitPrecision
                
            else: # Clic on  "-"
                newValue = currentValue - 10**-digitPrecision
            newValue = round(newValue, digitPrecision) # in case we do not break the ceiling of the digit precision
            
            # We need to ensure we stay within the digit precision
            if len(str(newValue).split('.')[1]) > digitPrecision:
                newValueString = str(newValue)[:len(str(newValue).split('.')[0]) + digitPrecision + 1] # shrink it
            elif len(str(newValue).split('.')[1]) < digitPrecision:
                newValueString = str(newValue) + '0' * (digitPrecision - len(str(newValue).split('.')[1])) # add zeros
            else:
                newValueString = str(newValue)


            # Update the grid cell with the new value
            self.entryFrame.GetParametersPanel().SetGridValue(row, 1, newValueString)
        
            # Update the model:
            setupName = self.parametersData.GetCurSetup()
            self.parametersData.GetParametersMap()[paramName].GetSetupsValues()[setupName] = newValue
                    
        except ValueError:
            # Handle the case where the current value is not a valid number
            wx.MessageBox(f"The current value '{currentValueStr}' for '{paramName}' is not a valid number.", 
                            "Conversion error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Unknown error : {str(e)}", 
                            "Error", wx.OK | wx.ICON_ERROR)
    
    @log_debug_event
    def OnParametersUpdate(self):
        self.daqmxComm.UpdateBackendServer(self.daqmxSys, self.daqmxDMServ)





    # ---- Pulse panel
    # Common stim parameters
    @log_debug_event
    def OnPulseChangeDuration(self, duration : float):
        self.pulseData.GetStimData().SetT(duration)
        self.pulseData.GetCurParameter().GetName()
        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)

    @log_debug_event
    def OnPulseChangeDt(self, dt : float):
        self.pulseData.GetStimData().SetDt(dt)



    # Pulses configuration
    @log_debug_event
    def OnPulseChangingParamBox(self, param : str):
        # ---- Update the model
        # Pulses data:
        csvParam : CSVParameter      = self.parametersData.GetParametersMap()[param]
        self.pulseData.SetCurParameter(csvParam)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)

        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)
    
    @log_debug_event
    def OnPulseChangingAmp(self, pulseId : int, amp : float):
        # ---- Update the model
        # Pulses data:
        PData : PulseData = self.pulseData
        PConf : PulseConf = PData.GetParamToPulsesConfigurationMap()[PData.GetCurParameter().GetName()][pulseId]
        PConf.SetAmp(amp)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)
        
        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)

    @log_debug_event
    def OnPulseChangingWidth(self, pulseId : int, width : float):
        # ---- Update the model
        # Pulses data:
        PData : PulseData = self.pulseData
        PConf : PulseConf = PData.GetParamToPulsesConfigurationMap()[PData.GetCurParameter().GetName()][pulseId]
        PConf.SetWidth(width)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)
        
        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)

    @log_debug_event
    def OnPulseChangingDelay(self, pulseId : int, delay : float):
        # ---- Update the model
        # Pulses data:
        PData : PulseData = self.pulseData
        PConf : PulseConf = PData.GetParamToPulsesConfigurationMap()[PData.GetCurParameter().GetName()][pulseId]
        PConf.SetDelay(delay)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)
        
        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)

    @log_debug_event
    def OnPulseChangingActive(self, pulseId : int, active : bool):
        # ---- Update the model
        # Pulses data:
        PData : PulseData = self.pulseData
        PConf : PulseConf = PData.GetParamToPulsesConfigurationMap()[PData.GetCurParameter().GetName()][pulseId]
        PConf.SetActive(active)
        # Dynamic DAQMX devices:
        self.pulseDMServ.UpdateDAQMXStim(self.pulseData, daqmxDMServ=self.daqmxDMServ, daqmxSys=self.daqmxSys)
        
        # ---- Update the view:
        self.entryFrame.GetPulsePanel().UpdateAll(self.pulseData)

    



    # PSA panel
    @log_debug_event
    def OnPSARunButton(self):
        pass

    @log_debug_event
    def OnPSAStopButton(self):
        pass

    @log_debug_event
    def OnPSAComboBoxXAxis(self, axName : str):
        # Update the model
        self.psaData.GetCurPsaMode().GetPsaSimulation().SetXAxisName(axName)
        
        # Update the plot
        activeConfs = self.psaDMServ.GetActiveChannelsConfigurationList(self.psaData.GetCurPsaMode())
        legends     = list(map(self.psaDMServ.GenerateLegends, activeConfs))
        curSelectionStr = self.psaData.GetCurPsaMode().GetPsaSimulation().GetXAxisName()
        X, Y   = self.psaDMServ.GetXData(self.psaData.GetCurPsaMode().GetPsaSimulation()), self.psaDMServ.GetYData(self.psaData.GetCurPsaMode())
        colors = [self.psaDMServ.GetColor(conf=activeConf,
                                          psaSim=self.psaData.GetCurPsaMode().GetPsaSimulation(), 
                                          niscopeDMServ=self.niscopeDMServ,
                                          niscopeSys=self.niscopeSys) for activeConf in activeConfs]
        self.entryFrame.GetPSAPanel().GetPlot().UpdateData(X=X,
                                                           Y=Y,
                                                           XAxisName=curSelectionStr,
                                                           legends=legends,
                                                           colors=colors)
        self.entryFrame.GetPSAPanel().GetPlot().UpdatePlot()

