#! usr/env/bin python3
# nevclient.model.config.Parameters.ParametersData

# utils
from nevclient.utils.Logger import Logger
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter

class ParametersData():
    """
    Stores useful data structures about the CSV parameters.

    Attributes
    ----------
    parametersMap : dict[str : CSVParameter]
        Mapping parameters'name to their corresponding instance.
    curSetup      : str
        The currently selected setup.
    setupsList    : list[str]
        The list of all the setups'name
    """

    def __init__(self,
                 parametersMap: dict[str, CSVParameter],
                 curSetup: str,
                 setupsList : list[str]):
        
        self.logger = Logger("ParametersData")

        self.parametersMap = parametersMap
        self.curSetup      = curSetup
        self.setupsList    = setupsList

# ──────────────────────────────────────────────────────────── Setters ──────────────────────────────────────────────────────────

    def SetParametersMap(self, parametersMap: dict[str, CSVParameter]):
        self.parametersMap = parametersMap

    def SetCurSetup(self, curSetup: str):
        self.curSetup = curSetup

    def SetSetupsList(self, setupsList : list[str]):
        self.setupsList = setupsList

# ──────────────────────────────────────────────────────────── Getters ──────────────────────────────────────────────────────────

    def GetParametersMap(self) -> dict[str, CSVParameter]:
        return self.parametersMap

    def GetCurSetup(self) -> str:
        return self.curSetup
    
    def GetSetupsList(self) -> list[str]:
        return self.setupsList