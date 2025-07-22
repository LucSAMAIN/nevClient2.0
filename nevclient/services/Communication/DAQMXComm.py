#! usr/env/bin python3
# nevclient.services.Communication.DAQMXComm

# logger
from nevclient.utils.Logger import Logger
# tcpClient
from nevclient.utils.TCPClient import TCPClient

class DAQMXComm():
    """
    Set of useful methods helping sending correct message to the backend server
    for DAQMX processes.

    Attributes
    ----------
    tcpClient : TCPClient

    Public methods
    --------------
    GetDAQMXInfo() -> str
    GetSAO(taskNo : int) -> str
    GetDAO(taskNo : int) -> str
    GetSDO(taskNo : int) -> str

    SetSAO(taskNo : int, data : list) -> str
    SetSDO(taskNo : int, data : list) -> str
    SetDAO(self, taskNo: int, ch_start: int, data: list[list]) -> str
    SetDAODLEN(self, taskNo : int, dlenValue : int) -> str
    SetDAOFREQ(self, taskNo : int, freq : float) -> str
    """

# ──────────────────────────────────────────────────────────── API GET ────────────────────────────────────────────────────────── 


    def __init__(self,
                 tcpClient : TCPClient):
        self.logger = Logger("DAQMXComm")
        
        self.tcpClient = tcpClient

    def GetDAQMXInfo(self) -> str:
        return self.tcpClient._request("GET DAQMXINFO")
    
    def GetSAO(self, taskNo : int) -> str:
        return self.tcpClient._request(f"GET SAO {taskNo}")
    
    def GetDAO(self, taskNo : int) -> str:
        return self.tcpClient._request(f"GET DAO {taskNo}")
    
    def GetSDO(self, taskNo : int) -> str:
        return self.tcpClient._request(f"GET SDO {taskNo}")
    

# ──────────────────────────────────────────────────────────── API SET ────────────────────────────────────────────────────────── 


    def SetSAO(self, taskNo : int, data : list) -> str:
        if not(len(data)):
            self.logger.error("SET SAO needs at least one value")
        requestString = f"SET SAO {taskNo} "
        for val in data:
            requestString += str(val) + " "
        return self.tcpClient._request(requestString)
    
    def SetSDO(self, taskNo : int, data : list):
        if not(len(data)):
            self.logger.error("SET SDO needs at least one value")
        requestString = f"SET SDO {taskNo} "
        for val in data:
            requestString += str(val) + " "
        return self.tcpClient._request(requestString)
    
    def SetDAO(self, taskNo: int, ch_start: int, data: list[list]) -> str:
        """
        Send a dynamic‐AO waveform to the server, exactly like the legacy
        client does.

        Parameters
        ----------
        taskNo : int          ID returned in the #DAQMXINFO banner
        ch_start : int        first channel to update
        data : list[list[float]]  

        Returns
        -------
        str
            The servers's string answer.
        """
        if not data:
            self.logger.error("SET DAO needs at least one value")

        # 1) hand-shake  ──────────────────────────────────────────────────
        self.tcpClient._request(f"SET DAO {taskNo} {ch_start}")

        # 2) data block  ─────────────────────────────────────────────────
        payload = " ".join(map(str, [map(str, dataList) for dataList in data])) + " #OK"
        return self.tcpClient._request(payload) 

    def SetDAODLEN(self, taskNo : int, dlenValue : int) -> str:
        """
        Send "SET DAO DLEN {DAQMXDevice Id} {dlenValue} to the backend server.

        Parameters
        ----------
        taskNo : int
            The DAQMX device id.
        dlenValue : int
            The new data lenght value.

        Returns
        -------
        str
            The servers's string answer. 
        """
        cmd = f"SET DAO DLEN {taskNo} {dlenValue}"
        return self.tcpClient._request(cmd)
    
    def SetDAOFREQ(self, taskNo : int, freq : float) -> str:
        """
        Send "SET DAO FREQ {DAQMX device id} {freq value} to the backend server.

        Parameters
        ----------
        taskNo : int
            The DAQMX device id
        freq : float
            The new frequence value of the device.

        Returns
        -------
        str
            The servers's string answer.
        """
        cmd = f"SET DAO FREQ {taskNo} {freq}"
        return self.tcpClient._request(cmd)
    

# ──────────────────────────────────────────────────────────── API RUN ────────────────────────────────────────────────────────── 


    def RunDao(self, taskNo : int):
        return self.tcpClient._request(f"RUN DAO {taskNo}")