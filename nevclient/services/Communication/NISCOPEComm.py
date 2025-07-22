#! usr/env/bin python3
# nevclient.services.Communication.NISCOPEComm

# logger
from nevclient.utils.Logger import Logger
# tcpClient
from nevclient.utils.TCPClient import TCPClient
# NISCOPE
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling

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