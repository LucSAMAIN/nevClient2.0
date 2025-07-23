#! usr/env/bin python3
# nevclient.__main__

# extern modules
import sys
import wx
# logger
from nevclient.utils.Logger import Logger
# factories
from nevclient.factories.DAQMXFactory import DAQMXFactory
from nevclient.factories.NISCOPEFactory import NISCOPEFactory
from nevclient.factories.PSAFactory import PSAFactory
from nevclient.factories.ParametersFactory import ParametersFactory
from nevclient.factories.PulseFactory import PulseFactory
# communication
from nevclient.services.Communication.DAQMXComm import DAQMXComm
from nevclient.services.Communication.NISCOPEComm import NISCOPEComm
from nevclient.services.Communication.PSAComm import PSAComm
# parsings
from nevclient.services.Parsing.DAQMXParsing import DAQMXParsing
from nevclient.services.Parsing.NISCOPEParsing import NISCOPEParsing
# data manipulation services
from nevclient.services.DataManipulation.NISCOPEDataServices import NISCOPEDataServices
from nevclient.services.DataManipulation.PSADataServices import PSADataServices
from nevclient.services.DataManipulation.DAQMXDataServices import DAQMXDataServices
from nevclient.services.DataManipulation.PulseDataServices import PulseDataServices
# processes services
from nevclient.services.Processes.PSAProcesses import PSAProcesses
# tcp client
from nevclient.utils.TCPClient import TCPClient
# views 
from nevclient.views.EntryFrame import EntryFrame
# controller
from nevclient.Controller import Controller
# psa
from nevclient.model.config.PSA.PSAData import PSAData

class Main():
    def __init__(self):
        self.logger = Logger("Main")
    
    def main(self):
        self.logger.info("Starting the nevclient application...")
        

        # Creation of the tcpclient:
        tcpClient = TCPClient()

        # Creation of services:
        daqmxComm   = DAQMXComm(tcpClient=tcpClient)
        niscopeComm = NISCOPEComm(tcpClient=tcpClient)
        psaComm     = PSAComm(tcpClient=tcpClient)
        
        daqmxPars   = DAQMXParsing()
        niscopePars = NISCOPEParsing()

        daqmxDM     = DAQMXDataServices()
        niscopeDM   = NISCOPEDataServices()
        PSADM       = PSADataServices()
        pulseDM     = PulseDataServices()

        psaProc     = PSAProcesses(tcpClient=tcpClient)

        # Creation of the factories:
        daqmxFac   = DAQMXFactory(daqmxComm=daqmxComm, daqmxPars=daqmxPars)
        niscopeFac = NISCOPEFactory(niscopeComm=niscopeComm, niscopePars=niscopePars)
        psaFac     = PSAFactory(niscopeDataServ=niscopeDM, psaDMServ=PSADM)
        paramFac   = ParametersFactory(daqmxDataServices=daqmxDM)
        pulseFac   = PulseFactory()


        # Initialization of the system before starting the app
        daqmxSystem   = daqmxFac.BuildDAQMXSys()
        niscopeSystem = niscopeFac.BuildNISCOPESys()

        # Creation of main config stuctures:
        psaData = psaFac.BuildPSAData(niscopeSystem)
        
        # Other useful data structures:
        colorMap = niscopeDM.GetChannelColors(niscopeSys=niscopeSystem)
        generateLegends = lambda conf: PSADM.GenerateLegends(conf)
        activeChannelConf = PSADM.GetActiveChannelsConfigurationList(psaData.GetCurPsaMode())
        
        # Creation of the wx app:
        app = wx.App()


        # Creation of the controller
        controller = Controller(niscopeSys=niscopeSystem, 
                                daqmxSys=daqmxSystem, 
                                psaData=psaData,
                                paramFac=paramFac,
                                psaDMServ=PSADM,
                                daqmxComm=daqmxComm,
                                daqmxDMServ=daqmxDM,
                                pulseFac=pulseFac,
                                pulseDMServ=pulseDM,
                                niscopeDMServ=niscopeDM,
                                psaProc=psaProc,
                                niscopeComm=niscopeComm,
                                psaComm=psaComm)

        # Creation of the views:
        entryFrame = EntryFrame(parent=None, size=(1500,1000), title="Nev client",
                   controller=controller,
                   psaData=psaData,
                   colorMap=colorMap,
                   generateLegends=generateLegends,
                   activeChannelConf=activeChannelConf)
        
        # setting the entryframe to the controller
        controller.SetEntryFrame(entryFrame)

        # Showing the entryframe:
        controller.GetEntryFrame().Show()    

        # Starting the main loop:
        app.MainLoop()

        

        self.logger.info("Exiting the nevclient application...")


if __name__ == "__main__":
    # Parsing the line parameters
    TCPClient.SIMULATE = True if "--simulate" in sys.argv else False
    Logger.DEBUG = True if "--debug" in sys.argv else False
    Logger.DEEP_DEBUG = True if "--deepDebug" in sys.argv else False
    m = Main()
    m.main()