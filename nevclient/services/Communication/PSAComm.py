#! usr/env/bin python3
# nevclient.services.Communication.PSAComm

# logger
from nevclient.utils.Logger import Logger
# tcpClient
from nevclient.utils.TCPClient import TCPClient
# NISCOPE
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling

class PSAComm():
    """
    Set of useful methods helping sending correct message to the backend server
    for NISCOPE processes.

    Attributes
    ----------
    tcpClient : TCPClient

    Public methods
    --------------
    GetPSAStat(self) -> str
    GetPSAData(self, start : int, end : int) -> str

    SetPSA(self, unionId: int, paramConf: tuple, rangeConf: tuple, skipSamples: int) -> str

    """
    def __init__(self,
                 tcpClient : TCPClient):
        self.logger = Logger("PSAComm")
        
        self.tcpClient = tcpClient

# ──────────────────────────────────────────────────────────── API GET ────────────────────────────────────────────────────────── 

    def GetPSAStat(self) -> str:
        return self.tcpClient._request("GET PSA STAT")
    
    def GetPSAData(self, start : int, end : int) -> str:
        if end == None or end == -1:
            end = ""
        return self.tcpClient._request(f"GET PSA DATA {start}-{end}")

# ──────────────────────────────────────────────────────────── API SET ────────────────────────────────────────────────────────── 

    def SetPSA(self, unionId: int, paramConf: tuple, rangeConf: tuple, skipSamples: int) -> str:
        """
        Sends the "SET PSA" command to the backend server to configure a Parameter Sweep Analysis.

        This method constructs the command string from the provided configuration
        and sends it to the server.

        Parameters
        ----------
        unionId : int
            The ID of the NISCOPE union to use for the analysis.
        paramConf : tuple
            A tuple containing the parameter to sweep, in the format
            (task_type, device_id, channel_index).
            Example: ("SAO", 0, 5) for channel 5 of device with ID 0.
        rangeConf : tuple
            A tuple defining the sweep range, in the format
            (start_value, end_value, number_of_steps).
            Example: (0.0, 5.0, 101)
        skipSamples : int
            The number of initial samples to discard at each step to allow
            the system to stabilize.
        
        Returns
        -------
        str
            The servers's string answer.
        """
        # Format the parameter and range configurations into the required string format "[...]"
        # Example: "[SAO 0 5]" and "[0.0 5.0 101]"
        param_str = f"[{paramConf[0]} {paramConf[1]} {paramConf[2]}]"
        range_str = f"[{rangeConf[0]} {rangeConf[1]} {rangeConf[2]}]"

        # Construct the full command string using an f-string for clarity
        command = f"SET PSA {unionId} {param_str} {range_str} {skipSamples}"
        self.tcpClient._request(command)
   

# ──────────────────────────────────────────────────────────── API RUN ────────────────────────────────────────────────────────── 

    def RunPSA(self):
        return self.tcpClient._request(f"RUN PSA")