#! usr/env/bin python3
# nevclient.services.Processes.PSAProcesses.py

# extern modules:
import wx
import re
import threading
from time import sleep

# logger
from nevclient.utils.Logger import Logger
# psa
from nevclient.model.config.PSA.PSAData import PSAData
from nevclient.model.config.PSA.PSASimulation import PSASimulation
from nevclient.model.config.PSA.PSAMode import PSAMode
from nevclient.model.config.PSA.SweepConf import SweepConf
from nevclient.model.config.PSA.TimingConf import TimingConf
# daqmx
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
# tcp
from nevclient.utils.TCPClient import TCPClient
# views
from nevclient.views.templates.NevPanel import NevPanel
# services
from nevclient.services.DataManipulation.PSADataServices import PSADataServices
from nevclient.services.DataManipulation.NISCOPEDataServices import NISCOPEDataServices
from nevclient.services.DataManipulation.DAQMXDataServices import DAQMXDataServices
from nevclient.services.Communication.DAQMXComm import DAQMXComm
from nevclient.services.Communication.NISCOPEComm import NISCOPEComm
from nevclient.services.Communication.PSAComm import PSAComm
from nevclient.services.Parsing.PSAParsing import PSAParsing
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# enums
from nevclient.model.Enums.SweepDirection import SweepDirection
from nevclient.model.Enums.PSAStatus import PSAStatus


class PSAProcesses():
    """
    Defines the different complex PSA processes.

    Attributes
    ----------
    psaBookMark : int
        The current number of points received since the start of the PSA simulation.
        This value is used to check if the number of points has been increased after the
        last GET PSA DATA call.
    stopEvent : threading.Event
        A thread flag to know if the stop button was pushed or not.
        It allows us to make the thread aware about the fact that it
        needs to stop
    tcpClient : TCPClient
            A runtime instance of the TCPClient.

    Public methods
    -------
    RunPSA:
        Begin the run psa process by doing
        multiple calls to the backend server
        and setting up the correct attributes
        in the different model classes but also
        for itself before the simulation starts.
    StopPSA:
        Stop the PSA simulation.
    """
    def __init__(self,
                 tcpClient,
                 psaBookMark = 0,
                 stopEvent = threading.Event()):
        self.logger = Logger("PSAServices")

        self.tcpClient = tcpClient 
        self.psaBookMark = 0
        self.stopEvent = threading.Event() 

# ──────────────────────────────────────────────────────────── Public API interface ──────────────────────────────────────────────────────────

    def RunPSA(self, psa     : PSAData, 
               daqmxSys      : DAQMXSys, 
               niscopeSys    : NISCOPESys, 
               psaPanel      : NevPanel,
               psaDmServ     : PSADataServices,
               daqmxComm     : DAQMXComm,
               daqmxDmServ   : DAQMXDataServices,
               niscopeComm   : NISCOPEComm,
               niscopeDmServ : NISCOPEDataServices,
               psaComm       : PSAComm):
        """
        The RunPSA method is called by the PSA panel when the user
        presses the "run" button in the bottom control part of the panel.
        The method is following these main steps:
        - Sending DAMQX updates to the server.
        - Sending NISCOPE updates about the list of the devices with active channels of the NC Mode union.
          But also the data length and the sampling frequence of this union.
        - Sending the SET PSA command

        Parameters
        ----------
        psa : PSAData
            The PSAData model instance.
        daqmxSys : DAQMXSys
            The DAQMX system instance currently defined.
        niscopeSys: NISCOPESys
            The NISCOPE system instance currently defined.
        psaPanel  : NevPanel
            The panel to update.
        psaDmServ : PSADataServices
        daqmxComm : DAQMXComm
        daqmxDmServ : DAQMXDataServices
        niscopeComm : NISCOPEComm
        niscopeDmServ : NISCOPEDataServices
        psaComm       : PSAComm
        """
        self.tcpClient.SettingPSA(psa) # useful in simulate mode only
        self.logger.info("Executing the RunPSA method !")
        # (0) Preparing the PSAData instance:
        # first we need to update the union with the actual
        # active NISCOPE Channels defined in the channel panel!
        # this a very important step since everything we do after will be base
        # on the order in wich these devices are passed
        # NOTES:
        # Specifically, as of Python 3.7, the order of keys in a dictionary is guaranteed to be the insertion order. This means that when you add key-value pairs to a dictionary, the order in which you added them is preserved, and when you iterate over the dictionary's keys, values, or items, they will be returned in that same insertion order.
        activeList = psaDmServ.GetActiveChannelsConfigurationList(psa.GetCurPsaMode())
        # We need to correctly set the orderedChannelConf to the psa model:
        self.logger.debug(f"In the run psa method activeList : {activeList}")
        self._PrepareForPSASimulation(psa.GetCurPsaMode(), psaDMServ=psaDmServ)
        # (1) Updating the DAQMX devices information in the backend
        daqmxComm.UpdateBackendServer(daqmxDMServ=daqmxDmServ,
                                      daqmxSys=daqmxSys)

        # (2) Updating the NC mode union devices information
        # COMMENT : 
        # This part is not clear at ALL to me.
        # In the old code the word "union" is used for a lot of different things,
        # I am really struggling to understand how the vocabulary is used.
        # Because at the initizalisation of the NISCOPE system,
        # we send a 'GET NSU NUM' to the backend server
        # in order to set up new union.
        # However, when studying the PSA + Sweepr part of the old nevclient,
        # they set two different modes : NC and BD which both have a unique
        # so-called 'union' attribute, respectively 0 and 1.
        # In this old code, when you want to start the PSA,
        # it send the backend server union commands : 'SET NSU ...'
        # based on this two modes.
        # Which makes me wonder why the we used the 'GET NSU NUM' in the first place ???
        # It feels like we are overwriting over the things we set up during
        # the initialization of the NISCOPE system without the code telling anything about it.
        # So that's why I was first saying "it is not clear at all to me" because
        # I can not find a sense of this behaviour in the code and how the 
        # so-called 'unions' really work and what they really mean... 

        # recover useful data
        psaMode = psa.GetCurPsaMode()
        timingConf : TimingConf = psaMode.GetTiming()
        delay    = timingConf.GetDelay()
        sampling = timingConf.GetSampling().value
        period   = timingConf.GetPeriod()

        # update the niscope system:
        niscopeDmServ.SetUnionDevices(psaMode.GetNiscopeUni().GetId(), [conf.GetNiscopeChn().GetDevice().GetId() for conf in activeList] , niscopeSys)
        niscopeComm.SendUpdatesBeforePSA(unionId = psaMode.GetNiscopeUni().GetId(), 
                                         delay=delay, 
                                         period=period, 
                                         sampling=sampling, 
                                         niscopeSys=niscopeSys)

        # (3) We can finally send the 'SET PSA' command to the backend server
        sweepConf      :  SweepConf     = psaMode.GetSweepMap()[psaMode.GetCurParam().GetName()]
        sweepdirection : SweepDirection = sweepConf.GetSweepDi()
        param          : CSVParameter   = sweepConf.GetParam()
        channel        : DAQMXChannel   = param.GetChannel()
        device         : DAQMXDevice    = channel.GetDevice()
        
        deviceKindString                = str(device.getDeviceKind())
        paramConf = (deviceKindString, device.GetId(), channel.GetIndex())

        start = sweepConf.GetStart()
        stop  = sweepConf.GetStop()
        steps = sweepConf.GetSteps()
        self.logger.debug(f"Sweep direction from the sweeperManager : {sweepdirection}")
        if sweepdirection  == SweepDirection.DOWN:
            self.logger.debug("Sweep direction is down")
            sweeperConf = (start, stop, steps)
        else:
            self.logger.debug("Sweep direction is up")
            sweeperConf = (stop, start, steps)
        self.logger.info(f"Running psa with sweeper conf : start={start}, stop={stop}, steps={steps}")
        ss = delay * sampling # see old code saying : "number of samples to skip fetching"
        psaComm.SetPSA(unionId= psaMode.GetNiscopeUni().GetId(),
                       paramConf=paramConf, 
                       rangeConf=sweeperConf, 
                       skipSamples=ss)
        # (4) Freezing everything (init delay)
        initDelay = timingConf.GetInDelay()
        sleep(initDelay/1000)
        # (4) Sending the 'RUN PSA' command to the server:
        psaComm.RunPSA()
        self.logger.debug(f"Sent the run psa command ?")
        self.psaBookMark = 0 # new psa simulation
        
        # (5) Entering the loop retrieving the PSA data:
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self._psa_worker_loop, args=[psa, psaPanel, psaDmServ, psaComm, niscopeDmServ, niscopeSys])
        thread.daemon = True # Allows the app to exit even if the thread is running
        thread.start()

        wx.CallAfter(psaPanel.runButton.Disable)
        wx.CallAfter(psaPanel.stopButton.Enable)
       


        self.logger.majorInfo("Succesfully executed the RunPSA method !")
    
    def StopPSA(self, psaPanel : NevPanel):
        self.stopEvent.set()
        wx.CallAfter(psaPanel.runButton.Enable)
        wx.CallAfter(psaPanel.stopButton.Disable)

# ──────────────────────────────────────────────────────────── Intern Methods ──────────────────────────────────────────────────────────

    def _psa_worker_loop(self, 
                         psa : PSAData, 
                         psaPanel : NevPanel, 
                         psaDmServ : PSADataServices, 
                         psaComm : PSAComm,
                         niscopeDMServ : NISCOPEDataServices,
                         niscopeSys : NISCOPESys):
        psaData = psa.GetCurPsaMode().GetPsaSimulation()
        psaParsing = PSAParsing()
        while not self.stopEvent.is_set():
            # (A) get the psa stat:
            psaStatBody = psaComm.GetPSAStat()
            self.logger.deepDebug(f"Raw psaStat : {psaStatBody}")
            # parsing it:
            stage, lastSValue, status = psaParsing.ParsingPSAStat(psaStatBody)
            # update the psa data instance:
            psaData.SetStage(stage)
            psaData.SetLastSValue(lastSValue)
            psaData.SetStatus(status)
            nbPoints = psaData.GetStage()


            if psaData.GetStatus() == PSAStatus.RUNNING:
                self.logger.info(f"Stage : {nbPoints}. Sweep value : {psaData.GetLastSValue()}")
            else: # either a bug or completed
                break

            # (B) get the psa data
            # We first need to ensure that the we have recieved new values:
            if nbPoints > self.psaBookMark:
                PSADataString = psaComm.GetPSAData(start=0, end=-1) # we take everything
                self.logger.deepDebug(f"Parsed PSA DATA: {PSADataString}")

                # parsing
                start, end, XSweeper, Y = psaParsing.ParsingPSAData(PSADataString, psa, psaDmServ)
                # updating the data:
                self.logger.debug(f"XSWEEPER : {XSweeper}")
                psaData.SetXSweeper(XSweeper)
                psaData.SetEnd(end)
                psaData.SetStart(start)
                psaData.SetY(Y)
                
            
                # plot the data
                wx.CallAfter(self._UpdatePlot, psa, psaDmServ, psaPanel, niscopeDMServ, niscopeSys)


                # updatge the psabookmark:
                self.psaBookMark = nbPoints
            
            

            sleep(0.1)
        wx.CallAfter(psaPanel.runButton.Enable)
        wx.CallAfter(psaPanel.stopButton.Disable)


    def _UpdatePlot(self, psa : PSAData, psaDMServ: PSADataServices, psaPanel : NevPanel, niscopeDMServ : NISCOPEDataServices, niscopeSys : NISCOPESys):
        psaSim : PSASimulation = psa.GetCurPsaMode().GetPsaSimulation()

        X         = psaDMServ.GetXData(psa.GetCurPsaMode())
        Y         = psaDMServ.GetYData(psa.GetCurPsaMode())
        XAxisName = psaSim.GetXAxisName()

        activeConfs = psaDMServ.GetActiveChannelsConfigurationList(psa.GetCurPsaMode())
        legends     = list(map(psaDMServ.GenerateLegends, activeConfs))
        colors      = [psaDMServ.GetColor(conf=activeConf,
                                                psaSim=psaSim, 
                                                niscopeDMServ=niscopeDMServ,
                                                niscopeSys=niscopeSys) for activeConf in activeConfs]
        


        psaPanel.GetPlot().UpdateData(X, Y, XAxisName, colors, legends)
        psaPanel.GetPlot().UpdatePlot()
        


    

    def _PrepareForPSASimulation(self, psaMode : PSAMode, psaDMServ : PSADataServices):
        """
        This method is the first step inside the RUN PSA process.
        It helps setting up the PSAData instance attributes.
        """
        psaData : PSASimulation = psaMode.GetPsaSimulation()
        # Empty or None values
        psaData.SetStage(0)
        psaData.SetStart(0)
        psaData.SetLastSValue(None)
        psaData.SetStatus(None)
        psaData.SetXSweeper([])
        # Resetting the Y dict
        psaDMServ.ResetY(psaMode)