#! usr/env/bin python3
# nevclient.services.DataManipulation.PSADataServices

# extern modules
import re
# logger
from nevclient.utils.Logger import Logger
# csvworker
from nevclient.utils.CSVWorker import CSVWorker
# psa
from nevclient.model.config.PSA.ChannelConf import ChannelConf
from nevclient.model.config.PSA.PSAMode import PSAMode
from nevclient.model.config.PSA.SweepConf import SweepConf
from nevclient.model.config.PSA.PSASimulation import PSASimulation
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# enum
from nevclient.model.Enums.SweepDirection import SweepDirection
# services
from nevclient.services.DataManipulation.NISCOPEDataServices import NISCOPEDataServices
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys

class PSADataServices():
    """
    Set of useful methods helping manipulating PSA data.

    Public methods
    --------------
    GetActiveChannelsConfigurationList() -> list[ChannelConf]
        Returns a list of all the defined active channels inside the current
        psa mode.
    GenerateLegends(self, conf : ChannelConf) -> str
        Generates a legend for the passed channel configuration
        instance.

    """
    def __init__(self):
          self.logger = Logger("PSADataServices")

    def ResetY(self, psaMode : PSAMode) -> None:
        """
        The ResetY method is used to reset the Y data
        attribute of the passed PSAData instance.
        It clears the old Y dictionnary's values
        and replace them with empty list.

        Parameters
        ----------
        psaMode : PSAMode
        """
        psaData : PSASimulation = psaMode.GetPsaSimulation()
        newY = psaData.GetY()
        newY.clear()
        conf : ChannelConf
        for conf in self.GetActiveChannelsConfigurationList(psaMode):
            newY[(conf.GetNiscopeChn().GetDevice().GetId(), conf.GetNiscopeChn().GetIndex())] = []
        psaData.SetY(newY)

    def GetActiveChannelsConfigurationList(self, psaMode : PSAMode) -> list[ChannelConf]:
        """
        Returns a list of all the defined active channels inside the current
        psa mode.
        Parameters
        ----------
        psaMode : PSAMode
            The current chosend psaMode.

        Returns
        -------
        list[ChannelConf]
        """
        confs = psaMode.GetChnConfList()
        return [conf for conf in confs if conf.GetActive()]

    def UpdatePSAModelAfterLoadingParameters(self, psaMode : PSAMode, csv : CSVWorker, tag : str, parametersData : ParametersData):
        """
        Updates the psa mode sweep map attributes after the user
        has loaded a csv file.

        Parameters
        ----------
        psaMode  : PSAMode
            The psaMode's instance to update
        csv      : CSVWorker
            The csv worker util's instance.
        tag      : str
            The tag of the mode we are looking for inside
            the csv file, i.e. '#NCMODE'
        parametersData : ParametersData
            The ParametersData instance used to recover
            the CSV parameter instance from the name of the parameter.
        """
        # sweep :
        modeMap = csv.GetParametersModeMap(tag=tag)
        
        sweepMap = {}
        for parameterName in list(modeMap.keys()):
            # recover the csv parameter instance
            param : CSVParameter = parametersData.GetParametersMap()[parameterName]
            # recover the mode string
            modeString = modeMap.get(parameterName, None)
            result = self._parseModeData(modeString)
            if result == None:
                continue
            start, stop, steps = result
            # Create the sweep conf instance
            # and updates the sweep map
            sweepConf = SweepConf(param, 
                                  start, 
                                  stop, 
                                  steps, 
                                  sweepDi=SweepDirection.DOWN) # default value
            sweepMap[parameterName] = sweepConf

        # updates the model:
        psaMode.SetSweepMap(sweepMap)
        if sweepMap:
            defaultCSVParam : CSVParameter = parametersData.GetParametersMap()[next(iter(sweepMap.keys()))]
            psaMode.SetCurParam(defaultCSVParam)
        



    def GenerateLegends(self, conf : ChannelConf) -> str:
        """
        Generates a legend for the passed channel configuration
        instance.

        Parameters
        ----------
        conf : ChannelConf
            The conf the caller wants to generate the legend from.
        
        Returns
        -------
        str: The generated legend string
        """
        
        return f"{conf.GetNiscopeChn().GetDevice().GetDeviceName()} {conf.GetNiscopeChn().GetDevice().GetId()} chn {conf.GetNiscopeChn().GetIndex()}"

    def GetXData(self, psaMode : PSAMode) -> list[float]:
        """ 
        This function returns the correct
        X data for plotting.
        Either the sweeper of a Y data of one of the
        NISCOPE active channels

        Parameters
        ----------
        psaMode : PSAMode

        Returns
        -------
        list[float]
        """
        psaData : PSASimulation = psaMode.GetPsaSimulation()
        if psaData.GetXAxisName() == "Sweeper":
            return psaData.GetXSweeper()
        
        self.logger.deepDebug(f"Inside GetXData method of PSAData class, axisName:{psaData.GetXAxisName()}")
        self.logger.deepDebug(f"Inside GetXData method of PSAData class, Y:{psaData.GetY()}")
        deviceId, channelId = self._parseLegend(psaData.GetXAxisName())
        if deviceId != None and channelId != None:
            return list(map(psaMode.GetOperation(), psaData.GetY()[(deviceId, channelId)]))
        self.logger.warning("GetX method failed, returning the XSweeper...")
        return psaData.GetXSweeper()
    
    def GetYData(self, psaMode : PSAMode) -> list[list[float]]:
        """
        This method returns the correct Y 
        Data for plotting.
        It uses the correct NISCOPE devices
        ordered to returns the good data.

        Parameters
        ----------
        psaMode : PSAMode

        Returns 
        -------
        list[list[float]]
        """
        psaData : PSASimulation = psaMode.GetPsaSimulation()
        
        result = []
        confs : list[ChannelConf]
        confs = self.GetActiveChannelsConfigurationList(psaMode)
        for conf in confs:
            deviceId = conf.GetNiscopeChn().GetDevice().GetId()
            channelId = conf.GetNiscopeChn().GetIndex()
            result.append(list(map(psaMode.GetOperation(), psaData.GetY()[(deviceId, channelId)])))
        self.logger.debug(f"Quitting the Get Y Data result : {result}")
        return result
    
    def GetColor(self, conf : ChannelConf, psaSim : PSASimulation, niscopeDMServ : NISCOPEDataServices, niscopeSys : NISCOPESys) -> str:
        """
        Returns the associated color of the passed channel configuration instance.

        Parameters
        ----------
        conf : ChannelConf
        psaSim : PSASimulation
        niscopeDMServ : NISCOPEDataServices
        niscopeSys : NISCOPESys

        Returns
        -------
        str: The color's string
        """
        chnId    = conf.GetNiscopeChn().GetIndex()
        devId    = conf.GetNiscopeChn().GetDevice().GetId()
        colorMap = niscopeDMServ.GetChannelColors(niscopeSys=niscopeSys)

        return colorMap[devId][chnId]
        
        




# ──────────────────────────────────────────────────────────── Intern methods ──────────────────────────────────────────────────────────
    
    def _parseLegend(self, legendStr : str) -> tuple[int,int]:
        """
        Helping function to recover the 
        NISOPE's device and channel information
        from the plot legend.
        Legend mus have the following syntax:
        {NISCOPE device name} {device id} chn {channel id}

        Parameters
        ----------
        legendStr : str

        Returns
        -------
        (int, int)
            NISCOPE device and channel ids
        """
        match = re.search(r'^.*?(\S+) chn (\d+)$', legendStr)
        if match:
            deviceId = match.group(1)
            channelId = match.group(2)
            return int(deviceId), int(channelId)

        self.logger.error(f"The _parseLegend was not able to correctly parsed the following passed legend: {legendStr}")
        return None, None




    def _parseModeData(self, nc : str) -> tuple[float, float, int]:
            """
            This function is used to parse the tag mode column (i.e. '#NCMODE').

            Parameters
            ----------
            nc : str
                The string to parse
            
            Returns
            -------
            tuple[float, float, int]:
                The recovered data start, stop, steps
            """
            pattern = r"#\[(\d+\.\d+), (\d+\.\d+), (\d+)\]"
            match = re.search(pattern, nc)

            if match:
                start = float(match.group(1))
                end = float(match.group(2))
                steps = int(match.group(3))

                return (start, end, steps)
                
            
            self.logger.warning(f"The _parseModeData was called with string : {nc} but no match could be found. Returning None value...")
            return None
