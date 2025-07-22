#! usr/env/bin python3
# nevclient.factories.NISCOPEFactory

# utils
from nevclient.utils.Logger import Logger
# services
from nevclient.services.Communication.NISCOPEComm import NISCOPEComm
from nevclient.services.Parsing.NISCOPEParsing import NISCOPEParsing
# niscope
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys

class NISCOPEFactory():
    """
    Defines methods that build complex instances of the NISCOPE's model part. 

    Attributes
    ----------
    niscopeComm : NISCOPEComm
        NISCOPEComm's services intance.
    niscopePars : NISCOPEParsing
        NISCOPEParsing's services instance.

    Public methods
    --------------
    BuildDAQMXSys() -> DAQMXSys:
        Returns a fresh DAQMXSys instance by calling the .
    """
    def __init__(self,
                 niscopeComm : NISCOPEComm,
                 niscopePars : NISCOPEParsing):
        self.logger = Logger("NISCOPEFactory")

        self.niscopeComm = niscopeComm
        self.niscopePars = niscopePars

    def BuildNISCOPESys(self) -> NISCOPESys:
        """
        Returns a fresh DAQMXSys instance after calling the
        backend server and parsing the answer.

        Returns
        -------
        NISCOPESys
        """
        # First call to get the NISCOPE info
        info = self.niscopeComm.GetNISCOPEInfo()
        # Then parse it
        # It creates the NISCOPDE devices
        mapDevices = self.niscopePars.ParseNISCOPEInfo(info)

        # After we have to create the unions:
        nsuNumInfo = self.niscopeComm.GetNSUNUM()
        _, unionMap = self.niscopePars.ParseNSUNUM(nsuNumInfo)
        
        niscopeSystem = NISCOPESys(mapDevices, unionsMap=unionMap)
        # Loading the unions as done in the original "load_unions" function
        for unionId in unionMap.keys():
            # GET NSU DEVS unionId
            # This will fill the unions with the devices
            tempstr = self.niscopeComm.GetNSUDEVS(unionId)
            self.niscopePars.ParseNSUDEVS(tempstr, niscopeSystem.GetUnionsMap(), niscopeSystem.GetDevicesMap())

            # GET NSU CHAN unionId
            # That sets up the channels for every device in every union
            tempstr = self.niscopeComm.GetNSUCHAN(unionId)
            self.niscopePars.ParseNSUCHAN(tempstr, unionMap)

            # GET NSU DLEN unionId
            # This sets up the data length for every device in every union
            tempstr = self.niscopeComm.GetNSUDLEN(unionId)
            self.niscopePars.ParseNSUDLEN(tempstr, unionMap)

            # GET NSU FREQ unionId
            # This sets up the sampling frequency for every device in every union
            tempstr = self.niscopeComm.GetNSUFREQ(unionId)
            self.niscopePars.ParseNSUFREQ(tempstr, unionMap)

            # GET NSU TRIG unionId
            # This sets up the trigger information for every union (no links to devices I think)
            tempstr = self.niscopeComm.GetNSUTRIG(unionId)
            self.niscopePars.ParseNSUTRIG(tempstr, unionMap)

        self.logger.info("The NISCOPE system has successfully been initialized.")
        return niscopeSystem


    



