#! usr/env/bin python3
# nevclient.Controller

# extern modules
import os
import wx
# factories
from nevclient.factories.ParametersFactory import ParametersFactory
# logger
from nevclient.utils.Logger import Logger
from nevclient.utils.Logger import log_debug_event
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
from nevclient.services.DataManipulation.PSADataServices import PSADataServices

class Controller():
    """
    Stores the main data structures.
    Handles the interactions between the user and the views.

    Attributes
    ----------
    niscopeSys : NISCOPESys
    daqmxSys   : DAQMXSys
    psaData    : PSAData
    paramFac   : ParametersFactory
    psaDMServ  : PSADataServices
    """

    def __init__(self,
                 niscopeSys : NISCOPESys,
                 daqmxSys   : DAQMXSys,
                 psaData    : PSAData,
                 paramFac   : ParametersFactory,
                 psaDMServ  : PSADataServices):
        self.logger = Logger("Controller")

        self.paramFac   = paramFac
        self.niscopeSys = niscopeSys
        self.daqmxSys   = daqmxSys
        self.psaData    = psaData

        self.psaDMServ  = psaDMServ
        
        self.entryFrame     : EntryFrame     = None # later set
        self.parametersData : ParametersData = None # same
        


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
        # Manipulation of the model:
        # Build the parameters data
        filePath : str = os.path.join(dirName, fileName)
        self.parametersData = self.paramFac.BuildParametersData(filePath, self.daqmxSys)
        # Update the sweeper configuration part:
        psaMode : PSAMode
        for psaMode in self.psaData.GetPsaModeMap().values():
            self.psaDMServ.UpdatePSAModelAfterLoadingParameters(psaMode=psaMode,
                                                                filePath=filePath,
                                                                tag=psaMode.GetTag(),
                                                                parametersData=self.parametersData)


        # And then we can update the different views
        # The parameters panel & the entry frame
        parametersPanel = ParametersPanel(parent=self.entryFrame.GetPanel(), 
                                          controller=self, 
                                          style=wx.SUNKEN_BORDER,
                                          parametersData=self.parametersData)  
        self.entryFrame.ReplaceParametersPanel(parametersPanel)  
        self.entryFrame.Layout()
        # Sweeper conf:
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



# ---- Parameters panel
    def OnParametersChangingSetUp(self, newSetupName : str):
        self.parametersData.SetCurSetup(newSetupName)
        # Update the view:
        self.entryFrame.GetParametersPanel().FillGrid(self.parametersData)
        pass