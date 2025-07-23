#! usr/env/bin python3
# nevclient.factories.PSAFactory

# extern modules
import numpy as np
# utils
from nevclient.utils.Logger import Logger
# psa
from nevclient.model.config.PSA.PSAData import PSAData
from nevclient.model.config.PSA.PSAMode import PSAMode
from nevclient.model.config.PSA.TimingConf import TimingConf
from nevclient.model.Enums.SamplingFreq import SamplingFreq
from nevclient.model.config.PSA.ChannelConf import ChannelConf
from nevclient.model.config.PSA.PSASimulation import PSASimulation
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice
# services
from nevclient.services.DataManipulation.NISCOPEDataServices import NISCOPEDataServices
from nevclient.services.DataManipulation.PSADataServices import PSADataServices

class PSAFactory():
    """
    Defines methods that build complex instances of the psa'model part. 

    Attributes
    ----------
    niscopeDataServ : NISCOPEDataServices
        The niscope data manipulation services' instance.
    psaDMServ : PSADataServices

    Public methods
    --------------
    BuildPSAData(niscopeSys : NISCOPESys) -> PSAData:
        Returns a fresh PSAData instance from a csv file.
    """
    def __init__(self, 
                 niscopeDataServ : NISCOPEDataServices,
                 psaDMServ : PSADataServices):
        self.logger = Logger("PSAFactory")

        self.niscopeDataServ = niscopeDataServ
        self.psaDMServ       = psaDMServ

    def BuildPSAData(self, niscopeSys : NISCOPESys) -> PSAData:
        """
        Returns a fresh PSAData instance.

        Parameters
        ----------
        niscopeSys : NISCOPESys
            The currently defined runtime instance
            of the NISCOPE system

        Returns
        -------
        PSAData
        """

        # Creation of the psa modes and associated map
        psaModeMap = dict()

        # NC Mode:
        mean              = lambda arr: np.mean(arr)
        sweepConf         = None # same idea
        timingConf        = TimingConf(delay=50.0, 
                                       inDelay=100.0, 
                                       sampling=SamplingFreq.K50,
                                       period=100.0) # default values see old code i guess
        # creation of the channel conf instances
        self.logger.deepDebug("Creation of the channel conf instances ")
        channelConfList = list()
        device : NISCOPEDevice
        for device in niscopeSys.GetDevicesMap().values():
            self.logger.deepDebug(f"niscopeDev={device}")
            niscopeChannel : NISCOPEChannel
            for niscopeChannel in device.GetChannels():
                conf = ChannelConf(niscopeChannel,
                                   offset=0.0,
                                   verticalCoupling=niscopeChannel.GetVerticalCoupling(),
                                   verticalRange=niscopeChannel.GetVerticalRange(),
                                   active=True)
                channelConfList.append(conf)
        
        sweepMap = dict() # without loading no sweep data can be generated
        curParam = None # at initialization no csv file was loaded
        NCMode = PSAMode(
            name="null-cline",
            niscopeUnion=niscopeSys.GetUnionsMap()[0], # we link the nc mode to the first union defined
            operation=mean,
            psaSimulation=None,
            timing = timingConf,
            chnConfList=channelConfList,
            operationName="mean",
            sweepMap=sweepMap,
            curParam=curParam,
            tag="#NCMODE") 
        # also create the simulation instance:
        YMap = dict()
        activeConf : ChannelConf
        for activeConf in self.psaDMServ.GetActiveChannelsConfigurationList(NCMode):
            chnId = activeConf.GetNiscopeChn().GetIndex()
            devId = activeConf.GetNiscopeChn().GetDevice().GetId()
            
            YMap[(devId,chnId)] = []
        psaSimulationData = PSASimulation(XSweeper=[],
                               Y=YMap,
                               XAxisName="Sweeper",
                               status=None,
                               stage=0,
                               lastSValue=0,
                               start=0,
                               end=0)
        NCMode.SetPsaSimulation(psaSimulationData)
        
        psaModeMap[NCMode.GetName()] = NCMode

    
        return PSAData(curPsaMode=NCMode,
                       psaModeMap=psaModeMap)

