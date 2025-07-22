#! usr/env/bin python3
# nevclient.services.Communication.DAQMXComm

# logger
from nevclient.utils.Logger import Logger
# tcpClient
from nevclient.utils.TCPClient import TCPClient
# daqmx
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DDO import DDO
from nevclient.model.hardware.DAQMX.SDO import SDO
from nevclient.model.hardware.DAQMX.DAO import DAO
from nevclient.model.hardware.DAQMX.SAO import SAO
from nevclient.model.Enums.DAQMXDeviceKind import DAQMXDeviceKind
# services
from nevclient.services.DataManipulation.DAQMXDataServices import DAQMXDataServices

class DAQMXComm():
    """
    Set of useful methods helping sending correct message to the backend server
    for DAQMX processes.

    Attributes
    ----------
    tcpClient : TCPClient

    Public methods
    --------------
    - UpdateBackendServer(daqmxSys : DAQMXSys, : TCPClient, startChn : int = 0, endChn : int = -1) -> None

    - GetDAQMXInfo() -> str
    - GetSAO(taskNo : int) -> str
    - GetDAO(taskNo : int) -> str
    - GetSDO(taskNo : int) -> str

    - SetSAO(taskNo : int, data : list) -> str
    - SetSDO(taskNo : int, data : list) -> str
    - SetDAO(taskNo: int, ch_start: int, data: list[list]) -> str
    - SetDAODLEN(taskNo : int, dlenValue : int) -> str
    - SetDAOFREQ(taskNo : int, freq : float) -> str
    """
# ──────────────────────────────────────────────────────────── Methods ────────────────────────────────────────────────────────── 

    def UpdateBackendServer(self, 
                            daqmxSys : DAQMXSys, 
                            daqmxDMServ : DAQMXDataServices,
                            startChn : int = 0, 
                            endChn : int = -1):
        """
        The SendDAQMXUpdatesToBackEndServer method is used to update the backend server's DAQMX system values

        Parameters
        ----------
        daqmxSys  : DAQMXSys
            The currently defined DAQMX system instance
        startChn  : int
        endChn    : int
            These two parameters are passed to the updates method of DAO devices.
        daqmxDMServ: DAQMXDataServices
            An instance of the DAQMX data manipulation services.
        daqmxCommServ : DAQMXComm
            Same idea for the communication services part
        """
        self.logger.majorInfo(f"Starting to send updates to the backend server...")
        try:
            device : DAQMXDevice
            self.logger.deepDebug(f"Entering the device loop with iter: {daqmxSys.GetDevicesMap().values()}")
            for device in daqmxSys.GetDevicesMap().values():
                kind : DAQMXDeviceKind = device.getDeviceKind()
                if   kind == DAQMXDeviceKind.DAO:
                    self._sendUpdatesDAO(device, startChn, endChn, daqmxDMServ)
                elif kind == DAQMXDeviceKind.DDO:
                    self._sendUpdatesDDO(device, daqmxDMServ)
                elif kind == DAQMXDeviceKind.SAO:
                    self._sendUpdatesSAO(device, daqmxDMServ)
                elif kind == DAQMXDeviceKind.SDO:
                    self._sendUpdatesSDO(device, daqmxDMServ)
                else:
                    raise Exception(f"Unkown device kind : {kind}")
            self.logger.majorInfo(f"Succesfully sent the data to the backend server !")
        except Exception as e:
            self.logger.error(f"Exception was raised after the SendDAQMXUpdatesToBackendServer method was called with args, daqmxSys : {daqmxSys}, startChn : {startChn}, endChn : {endChn}.\n {e}")

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
        data = [l[0] for l in data] # we need to serialize of the backend server
        if not(len(data)):
            self.logger.error("SET SAO needs at least one value")
        requestString = f"SET SAO {taskNo} "
        for val in data:
            requestString += str(val) + " "
        return self.tcpClient._request(requestString)
    
    def SetSDO(self, taskNo : int, data : list):
        data = [l[0] for l in data] # we need to serialize of the backend server
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
    

# ──────────────────────────────────────────────────────────── Private methods ────────────────────────────────────────────────────────── 
    def _sendUpdatesSAO(self, 
                        device : SAO, 
                        daqmxDMServ : DAQMXDataServices):
        self.logger.deepDebug(f"Entering the setUpdates method for device {device.GetDeviceName()} of type {device.getDeviceKind()}")
        try:
            self.SetSAO(device.GetId(), daqmxDMServ.GetDeviceData(device))
            self.logger.deepDebug(f"Succesfully send SET SAO for task id={device.GetId()}")
        except Exception as e:
            self.logger.error(f"Exception raised while sending SET SAO for task id={device.GetId()} : {e}")
    
    def _sendUpdatesSDO(self, 
                        device : SDO, 
                        daqmxDMServ : DAQMXDataServices):
        self.logger.deepDebug(f"Entering the setUpdates method for device {device.GetDeviceName()} of type {device.getDeviceKind()}")
        try:
            self.SetSDO(device.GetId(), daqmxDMServ.GetDeviceData(device))
            self.logger.deepDebug(f"Succesfully send SET SDO for task id={device.GetId()}")
        except Exception as e:
            self.logger.error(f"Exception raised while sending SET SDO for id={device.GetId()} : {e}")

    def _sendUpdatesDAO(self, 
                        device : DAO, 
                        startChannel : int, 
                        endChannel : int, 
                        daqmxDMServ : DAQMXDataServices):
        self.logger.deepDebug(f"Entering the setUpdates method for device {device.GetDeviceName()} of type {device.getDeviceKind()}")
        if endChannel == -1:
            data = daqmxDMServ.GetDeviceData(device)[startChannel:]
        else:
            data = daqmxDMServ.GetDeviceData(device)[startChannel:endChannel]
        # Adding the stim:
        def isEmpty(l : list) -> bool:
            for elem in l:
                if type(elem) != list or not isEmpty(elem):
                    return False
            return True
        if not isEmpty(daqmxDMServ.GetDeviceStim(device)):
            self.logger.deepDebug(f"Inside the sendupdates method of DAO we found a stim for device : {device}")
            data_2d = data
            stim_2d = daqmxDMServ.GetDeviceStim(device)
            new_data_2d = []

            for data_ch, stim_ch in zip(data_2d, stim_2d):
                # We add the stim to the data
                updated_part = [d + s for d, s in zip(data_ch, stim_ch)]
                # Handling the cases where len(stim) > len(data) or the opposite
                if len(stim_ch) > len(data_ch):
                    last_val_original = data_ch[-1] if data_ch else 0
                    stim_remainder = stim_ch[len(data_ch):]
                    extended_part = [last_val_original + s for s in stim_remainder]
                    new_data_ch = updated_part + extended_part
                else:
                    data_remainder = data_ch[len(stim_ch):]
                    new_data_ch = updated_part + data_remainder
                
                new_data_2d.append(new_data_ch)

            data = new_data_2d

        try : 
            self.SetDAODLEN(device.GetId(), device.GetDataLength())
            self.logger.deepDebug(f"Succesfully send SET DAO DLEN with dlen value : {device.GetDataLength()}")
            self.SetDAOFREQ(device.GetId(), device.GetFreq())
            self.logger.deepDebug(f"Succesfully send SET DAO FREQ with freq value : {device.GetFreq()}")
            self.SetDAO(device.GetId(), startChannel, data)
            self.logger.deepDebug(f"Succesfully send SET DAO")
            self.RunDao(device.GetId())
            self.logger.deepDebug(f"Succesfully send RUN DAO")
        except Exception as e:
            self.logger.error(f"Exception happened while sending SET DAO / RUN DAO for id={device.GetId()}: {e}")


    def _sendUpdatesDDO(self, 
                        device : DDO, 
                        daqmxDMServ : DAQMXDataServices):
        raise NotImplemented("The SET DDO is not implemented yet")
        