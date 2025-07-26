#! usr/env/bin python3
# nevclient.factories.PulseFactory

# logger
from nevclient.utils.Logger import Logger
# pulse
from nevclient.model.config.Pulse.PulseData import PulseData
from nevclient.model.config.Pulse.PulseConf import PulseConf
from nevclient.model.config.Pulse.StimConf import StimConf
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# daqmx
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice

class PulseFactory():
    """
    Defines methods that build complex instances of the pulse'model part. 

    Attributes
    ----------

    Public methods
    --------------
    """
    def __init__(self):
        self.logger = Logger("PulseFactory")

    def BuildPulseData(self, parametersData : ParametersData) -> PulseData:
        """
        Builds the pulse data after the user loaded the csv file.

        Parameters
        ----------
        parametersData : ParametersData
            The parameters'data instance generated
            by the corresponding factory just after
            the user has decided to load the csv file.

        Retunrs
        -------
        """
        nbPulses = 2

        params       : list[CSVParameter] = list(parametersData.GetParametersMap().values())
        

        # stim data:
        stimData = StimConf()

        # creation of the pulses'configuration
        paramToPulsesConfigurationMap : dict[str : list[PulseConf]] = {}
        param : CSVParameter
        for param in params:
            channel      : DAQMXChannel = param.GetChannel()
            bindedDevice : DAQMXDevice  = channel.GetDevice()
            if not bindedDevice.isDynamic():
                continue 
            confList : list[PulseConf] = []
            for i in range(nbPulses):
                confList.append(PulseConf(id=i,
                                          delay=5.0,
                                          width=5.0,
                                          amp=100.0,
                                          param=param,
                                          active=True if i == 0 else False))
            paramToPulsesConfigurationMap[param.GetName()] = confList
        
        
        defaultParam : CSVParameter       = parametersData.GetParametersMap()[next(iter(paramToPulsesConfigurationMap.keys()))]
        return PulseData(nbPulses=nbPulses, 
                  curParameter=defaultParam, 
                  paramToPulsesConfigurationMap=paramToPulsesConfigurationMap, 
                  stimData=stimData)