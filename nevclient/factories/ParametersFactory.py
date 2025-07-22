#! usr/env/bin python3
# nevclient.factories.ParametersFactory

# utils
from nevclient.utils.Logger import Logger
from nevclient.utils.CSVWorker import CSVWorker
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# DAQMX for bindings
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
# services
from nevclient.services.DataManipulation.DAQMXDataServices import  DAQMXDataServices

class ParametersFactory():
    """
    Defines methods that build complex instances of the parameters'model part. 

    Public methods
    --------------
    BuildParametersData(filePath : str) -> ParametersData:
        Returns a fresh ParametersData instance from a csv file.
    """
    def __init__(self,
                 daqmxDataServices : DAQMXDataServices):
        self.logger = Logger("ParametersFactory")
        self.daqmxDataServices = daqmxDataServices

    def BuildParametersData(self, csv : CSVWorker, daqmxSys : DAQMXSys):
        """
        Returns a fresh ParametersData instance from a csv file.
        And updates the PSA data instance accordingly to the 
        configuration mode column such as '#NCMODE'. 

        Parameters
        ----------
        csv      : CSVWorker
            The csv worker util's instance
        daqmxSys : DAQMXSys
        """
        # (1) Creation of the parameters map
        # Creation of the csv parameters
        # Recover useful structures from the worker
        paramNames     = csv.GetParametersList()
        chInfoMap      = csv.GetParametersChannelInfoMap()
        devicesNameMap = csv.GetParametersDeviceNameMap()
        

        parametersMap = {}
        for parameterName in paramNames:
            setupsValuesMap = csv.GetSetupsValues(parameterName)
            channelInfo     = chInfoMap[parameterName]
            deviceName      = devicesNameMap[parameterName]

            device : DAQMXDevice   = self.daqmxDataServices.FindDAQMXDevice(deviceName, channelInfo, daqmxSys)
            channelId              = int(channelInfo.split('-')[1])
            channel : DAQMXChannel = device.GetChannels()[channelId]
            
            param : CSVParameter = CSVParameter(parameterName, setupsValuesMap, channel)
            parametersMap[parameterName] = param

            
    
        # (2) Take a dummy setup:
        curSetup = next(iter(csv.GetSetupsList()))

        # (3) Retrieve the setups list
        setupsList = csv.GetSetupsList()

        # Return the result
        return ParametersData(parametersMap=parametersMap, curSetup=curSetup, setupsList=setupsList)


    



