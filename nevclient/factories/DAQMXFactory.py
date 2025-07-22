#! usr/env/bin python3
# nevclient.factories.DAQMXFactory

# utils
from nevclient.utils.Logger import Logger
# DAQMX for bindings
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
# services
from nevclient.services.Parsing.DAQMXParsing import DAQMXParsing
from nevclient.services.Communication.DAQMXComm import DAQMXComm

class DAQMXFactory():
    """
    Defines methods that build complex instances of the DAQMX's model part. 

    Attributes
    ----------
    daqmxComm : DAQMXComm
        DAQMXComm's services intance.
    daqmxPars : DAQMXParsing
        DAQMXParsing's services instance.

    Public methods
    --------------
    BuildDAQMXSys() -> DAQMXSys:
        Returns a fresh DAQMXSys instance by calling the .
    """
    def __init__(self,
                 daqmxComm : DAQMXComm,
                 daqmxPars : DAQMXParsing):
        self.logger = Logger("ParametersFactory")

        self.daqmxComm = daqmxComm
        self.daqmxPars = daqmxPars

    def BuildDAQMXSys(self) -> DAQMXSys:
        """
        Returns a fresh DAQMXSys instance after calling the
        backend server and parsing the answer.

        Returns
        -------
        DAQMXSys
        """
        # Let's call the backend server to recover information:
        info = self.daqmxComm.GetDAQMXInfo()
        # And then parse it:
        devicesMap = self.daqmxPars.ParseDAQMXInfo(info)


        return DAQMXSys(devicesMap)


    



