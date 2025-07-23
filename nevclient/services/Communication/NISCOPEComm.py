#! usr/env/bin python3
# nevclient.services.Communication.NISCOPEComm

# logger
from nevclient.utils.Logger import Logger
# tcpClient
from nevclient.utils.TCPClient import TCPClient
# NISCOPE
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
from nevclient.model.hardware.NISCOPE.NISCOPEUnion import NISCOPEUnion
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice

class NISCOPEComm():
    """
    Set of useful methods helping sending correct message to the backend server
    for NISCOPE processes.

    Attributes
    ----------
    tcpClient : TCPClient

    Public methods
    --------------
    GetNISCOPEInfo(self) -> str
    GetNSUNUM(self) -> str
    GetNSUTRIG(self, unionNo: int) -> str
    GetNSUDEVS(self, unionNo: int) -> str
    GetNSUCHAN(self, unionNo: int) -> str
    GetNSUDLEN(self, unionNo: int) -> str
    GetNSUFREQ(self, unionNo: int) -> str

    SetNSUDEVS(self, unionId : int, devsIds : list[int]) -> str
    SetNSUCHAN(self, unionId : int, deviceId : int, channelConf : list[tuple[NISCOPEChannelVerticalRange, NISCOPEChannelVerticalCoupling]]) -> str
    SetNSUDLEN(self, unionId : int, dlen : float) -> str
    SetNSUFREQ(self, unionId : int, freq : float) -> str
    """
    def __init__(self,
                 tcpClient : TCPClient):
        self.logger = Logger("NISCOPEComm")
        
        self.tcpClient = tcpClient

    def SendUpdatesBeforePSA(self, 
                          unionId    : int, 
                          delay      : float,
                          period     : float,
                          sampling   : float,
                          niscopeSys : NISCOPESys):
        """
        The SendUpdatesBeforePSA method is used to synchronized the NISCOPE system object
        current state and data with the backend server by sending multiple different
        requests:
        - SET NSU DEVS
        - SET NSU CHAN
        - SET NSU DLEN
        - SET NSU FREQ
        

        It is especially used int the PSA process when the user want to run
        a simulation.

        Parameters:
        -----------
        unionId  : int
            The NISCOPE union id on which to operate the updates.
            I am not sure I understood well how this parameter is defined in the old code.
            To me it seems that "0" is the one value associated to NC mode.
            It also appears to be the most important one. 

        delay    : float
        period   : float
        sampling : float
            These three parameters are the values defined in the timing configuration
            of the sweeper panel. They are used to compute the new value of the 
            union's data length, old code, IDU why :( 
        niscopeSys : NISCOPESys
            The currently defined NISCOPE system instance
        """
        self.logger.info(f"Entering the SendUpdatesBeforePSA method")
        # (1) Sending updates to the backend server about the different devices of the union
        union : NISCOPEUnion = niscopeSys.GetUnionsMap()[unionId]
        devicesIDs = list(union.GetDevicesMap().keys())
        self.logger.deepDebug(f"Inside the SendUpdatesBeforePSA method, niscope devices id list : {devicesIDs}")
        self.SetNSUDEVS(unionId=unionId, devsIds=devicesIDs)
        # (2) Sending updates to the backend server about the configuration of the channels
        for deviceId in devicesIDs:
            device : NISCOPEDevice
            device                   = union.GetDevicesMap()[deviceId]
            channel : NISCOPEChannel
            deviceRanges = []
            deviceCouplings = []
            for channel in device.GetChannels():
                deviceRanges.append(channel.GetVerticalRange())
                deviceCouplings.append(channel.GetVerticalCoupling())

            channelConfiguration     = list(zip(deviceCouplings, deviceRanges))
            self.SetNSUCHAN(unionId=unionId, deviceId=deviceId, channelConf=channelConfiguration)
        # (3) Updating the backend server about the data lenght of the union (SET NSU DLEN)
        dlen = (period + delay) * sampling
        self.SetNSUDLEN(unionId=unionId, dlen=dlen)
        # (4) Updating the backend server about the frequence of the union (SET NSU FREQ)
        self.SetNSUFREQ(unionId=unionId, freq=sampling)

        self.logger.info(f"Succesfully executed the SendUpdatesBeforePSA method")
# ──────────────────────────────────────────────────────────── API GET ────────────────────────────────────────────────────────── 

    def GetNISCOPEInfo(self) -> str:
        return self.tcpClient._request("GET NISCOPEINFO")

    def GetNSUNUM(self) -> str:
        return self.tcpClient._request("GET NSU NUM")

    def GetNSUTRIG(self, unionNo: int) -> str:
        return self.tcpClient._request(f"GET NSU TRIG {unionNo}")
    
    def GetNSUDEVS(self, unionNo: int) -> str:
        return self.tcpClient._request(f"GET NSU DEVS {unionNo}")

    def GetNSUCHAN(self, unionNo: int) -> str:
        return self.tcpClient._request(f"GET NSU CHAN {unionNo}")

    def GetNSUDLEN(self, unionNo: int) -> str:
        return self.tcpClient._request(f"GET NSU DLEN {unionNo}")

    def GetNSUFREQ(self, unionNo: int) -> str:
        return self.tcpClient._request(f"GET NSU FREQ {unionNo}")

# ──────────────────────────────────────────────────────────── API SET ────────────────────────────────────────────────────────── 


    def SetNSUDEVS(self, unionId : int, devsIds : list[int]) -> str:
        """
        The SetNSUDEVS method sends the "SET NSU DEVS" command to the backend server

        Parameters
        ----------
        unionId : int
            The id of the NISCOPE devices union
        devsIds : list[int]
            A list of the ids of the devices contained in the union.
            nDevs = len(devsIds)

        Returns
        -------
        str
            The servers's string answer.
        """
        nDevs = len(devsIds)
        devs_str = " ".join(map(str, devsIds))
        return self.tcpClient._request(f"SET NSU DEVS {unionId} {nDevs} [{devs_str}]")

    def SetNSUCHAN(self, unionId : int, deviceId : int, channelConf : list[tuple[NISCOPEChannelVerticalRange, NISCOPEChannelVerticalCoupling]]) -> str:
        """
        The SetNSUCHAN method sends the "SET NSU CHAN" command to the backend server.
        
        Parameters
        ----------
        unionId : int
            The id of the NISCOPE union.
        deviceId : int 
            The id of the NISCOPE device inside the union.
        channelConf : list[tuple[VerticalRange, VerticalCoupling]]
            A list of the device's channels configurations

        Returns
        -------
        str
            The servers's string answer.
        """
        # Use a list comprehension to format each tuple into the "[range coupling]" string format.
        # Example: (5.0, "DC") becomes "[5.0 DC]"
        self.logger.debug(f"Entering the SetNSUCHAN method with params: unionId {unionId}, deviceId {deviceId}, channelConf {channelConf}")
        formatted_configs = [f"[{v_range} {v_coupling}]" for v_range, v_coupling in channelConf]
        channelConfString = " ".join(formatted_configs)
        command = f"SET NSU CHAN {unionId} {deviceId} {channelConfString}"
        return self.tcpClient._request(command)
        
    def SetNSUDLEN(self, unionId : int, dlen : float) -> str:
        """
        The SetNSUDLEN method sends the "SET NSU DLEN" command to the backend server,
        in order to update the data lenght value of the passed union.

        Parameters
        ----------
        unionId : int
            The id of the NISCOPE union.
        dlen : float
            The data lenght value of the NISCOPE union.

        Returns
        -------
        str
            The servers's string answer.
        """
        command = f"SET NSU DLEN {unionId} {str(dlen)}"
        return self.tcpClient._request(command)

    def SetNSUFREQ(self, unionId : int, freq : float) -> str:
        """
        The SetNSUDLEN method sends the "SET NSU FREQ" command to the backend server,
        in order to update the sampling frequency value of the passed union.

        Parameters
        ----------
        unionId : int
            The id of the NISCOPE union.
        freq : float
            The frequency sampling value of the NISCOPE union.
        
        Returns
        -------
        str
            The servers's string answer.
        """
        command = f"SET NSU FREQ {unionId} {str(freq)}"
        self.logger.debug(f"Sending the SET NSU FREQ following command: {command}")
        return self.tcpClient._request(command)