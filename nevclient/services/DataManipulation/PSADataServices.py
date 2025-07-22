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
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# enum
from nevclient.model.Enums.SweepDirection import SweepDirection

class PSADataServices():
    """
    Set of useful methods helping manipulating PSA data.

    Public methods
    --------------
    GetActiveChannelsConfigurationList() -> list[ChannelConf]
        Returns a list of all the defined active channels inside the current
        psa mode.

    """
    def __init__(self):
          self.logger = Logger("PSADataServices")


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

    def UpdatePSAModelAfterLoadingParameters(self, psaMode : PSAMode, filePath : str, tag : str, parametersData : ParametersData):
        """
        Updates the psa mode sweep map attributes after the user
        has loaded a csv file.

        Parameters
        ----------
        psaMode  : PSAMode
            The psaMode's instance to update
        filePath : str
            The file path to the csv file containing all
            the data.
        tag      : str
            The tag of the mode we are looking for inside
            the csv file, i.e. '#NCMODE'
        parametersData : ParametersData
            The ParametersData instance used to recover
            the CSV parameter instance from the name of the parameter.
        """
        csv = CSVWorker(filePath=filePath)
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

        # updates the mode:
        psaMode.SetSweepMap(sweepMap)
        if sweepMap:
            defaultCSVParam : CSVParameter = parametersData.GetParametersMap()[next(iter(sweepMap.keys()))]
            psaMode.SetCurParam(defaultCSVParam)


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
