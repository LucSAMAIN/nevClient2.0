#! usr/bin/env python3
# nevclient.model.data.PulseData

# logger
from nevclient.utils.Logger import Logger
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
# pulse and stim conf
from nevclient.model.config.Pulse.PulseConf import PulseConf
from nevclient.model.config.Pulse.StimConf import StimConf

class PulseData():
    """
    The PulseData class is used to manage the data that the user
    selects inside the Pulse panel of the entryframe.
    It changes the data for the specified parameter selected
    in the corresponding combobox.
    From what I have understood, only parameters binded to dynamic devices
    can be selected inside the combobox.
    This means that PulseData class only manage information of DAQMX
    dynamic devices.

    Attributes
    ----------
    nbPulses                                : int
        The number of different pulses the user can define for every
        parameters.
    CSVParamToPulsesConfigurationMap        : dict[CSVParameter : list[PulseConf]]
        This map helps to store the configuration of every parameters.
        Keys are the name of the parameter and values are the corresponding
        list of PulseConfiguration instance.
    curParameterName                        : CSVParameter
        Same idea as before but for parameter being currently defined.
    stimData                                : StimConf
        The stimulus Data instance managing the data displayed inside the 
        Stim panel.
    """

    def __init__(self,
                 nbPulses                                : int,
                 curParameterName                        : CSVParameter,
                 CSVParamToPulsesConfigurationMap        : dict,
                 stimData                                : StimConf):
        self.nbPulses                                = nbPulses
        self.curParameterName                        = curParameterName
        self.CSVParamToPulsesConfigurationMap = CSVParamToPulsesConfigurationMap
        self.stimData                                = stimData

    
# ────────────────────────────────────────────────── Setters ─────────────────────────────────────────────────────

    def SetCurParameter(self, newName : CSVParameter) -> None:
        self.curParameterName = newName
    def SetNbPulses(self, newnbPulses : int) -> None:
        self.nbPulses = newnbPulses
    def SetCSVParamToPulsesConfigurationMap(self, dico : dict) -> None:
        self.CSVParamToPulsesConfigurationMap = dico

# ────────────────────────────────────────────────── Getters ─────────────────────────────────────────────────────

    def GetCSVParamToPulsesConfigurationMap(self) -> dict:
        return self.CSVParamToPulsesConfigurationMap
    def GetCurParameter(self) -> CSVParameter:
        return self.curParameterName
    def GetNbPulses(self) -> int:
        return self.nbPulses
    def GetStimData(self) -> StimConf:
        return self.stimData