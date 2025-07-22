#! usr/env/bin python3
# nevclient.services.Parsing.DAQMXParsing

# logger
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.Enums.DAQMXDeviceKind import DAQMXDeviceKind
from nevclient.model.hardware.DAQMX.DAO import DAO
from nevclient.model.hardware.DAQMX.DDO import DDO
from nevclient.model.hardware.DAQMX.SDO import SDO
from nevclient.model.hardware.DAQMX.SAO import SAO
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel

class DAQMXParsing():
    """
    Set of useful methods helping parsing server's answer about the DAQMX system.

    Public methods
    --------------
    ParseDAQMXInfo(text : str, daqmxSys : DAQMXSys) -> dict[int : DAQMXDevice]:
        Parses the server's answer after calling for DAQMX info and returns
        the corresponding map between devices'id ant their created instance.
    """

    def __init__(self):
        self.logger = Logger("DAQMXParsing")

    def ParseDAQMXInfo(self, text : str,) -> dict[int : DAQMXDevice]:
        """
        Parses the whole #DAQMXINFO reply into a list of TaskInfo objects.
        The list is stored inside the different attributes of the DAQMXData class.
        Usual form of the input: 
        "#DAQMXINFO\nSAO[device-info]…\nDAO[device-info]…\nSDO[device-info]…\n#OK"

        Parameters
        ----------
        text : str
            The body of the answer of the DAQMX reply from the server

        Returns
        -------
        dict[int : DAQMXDevice]:
            The devicesMap of the DAQMX system instance.

        """
        splitLines = text.splitlines()
        self.logger.deepDebug(f"Entering the ParseDAQMXInfo method with the following input text: \n{text}")
        self.logger.deepDebug(f"Split lines list : \n {splitLines}")

        if splitLines[0] != "#DAQMXINFO":
            raise Exception("To use ParseDAQMXInfo function, the input text must start by the '#DAQMXINFO' flag.")
        if splitLines[-1] != "#OK":
            raise Exception("The input text does not end with the usual '#OK' flag.")
        
        result = {}
        for line in splitLines:
            self.logger.deepDebug(f"Line : \n{line}")
            if not line or line[0] == '#': # for the "#OK" or the "#DAQMXINFOS" lines
                continue

            try:
                kind = DAQMXDeviceKind(line[:3])
            except ValueError:        # unknown tag – ignore
                raise Exception(f"Unknown task kind. Defined task kind are : {[m.name for m in DAQMXDeviceKind]}")
            except Exception as e :
                raise Exception(f"Unknown error occured: {e}")
            idx = line.find('[')
            if idx != -1:
                line = line[idx:]  # result is '[6,DACS0,PXI-6704,16,1,0.000000,0]'
            else:
                raise Exception(f"Uncorrect syntax found for an answer line after the DAQMXInfo call: {line}")
            
            
            
            for block in line.split(']'):
                self.logger.deepDebug(f"Block : \n{block}")
                if block.startswith('['):

                    device = self._deviceFromBlock(kind, block)
                    result[device.GetId()] = device

        self.logger.info(f"Successfully parsed a DAQMXInfo.")
        return result
    





# ──────────────────────────────────────────────────────────── Intern methods ────────────────────────────────────────────────────────── 




    def _deviceFromBlock(self, kind : DAQMXDeviceKind, block : str) -> DAQMXDevice:
        """
        Helper function for the ParseDAQMXInfo function

        Parameters
        ----------
        kind : DAQMXDeviceKind
            The kind of the device.
        block : str
            The string to parse.
        
        Returns
        -------
        DAQMXDevice
            The DAQMXDevice object parsed from the string block
        """
        DEVICE_CLASS_MAP = {
            DAQMXDeviceKind.SAO: SAO,
            DAQMXDeviceKind.SDO: SDO,
            DAQMXDeviceKind.DAO: DAO,
            DAQMXDeviceKind.DDO: DDO,
        }

        self.logger.deepDebug(f"Executing the _DeviceFromBlock method")
        f = block[1:].split(',')
        id                 = int(f[0])
        deviceName         = f[1]
        modelName          = f[2]
        nChannels          = int(f[3])
        lData              = int(f[4])
        freq               = float(f[5])
        status             = int(f[6])
        
        device_class = DEVICE_CLASS_MAP.get(kind)
        self.logger.deepDebug(f"Inside the _DeviceFromBlock method, \n kind : {kind}, id : {id}, device_class : {device_class}")
    
        if not device_class:
            raise Exception(f"Wrong task kind was passed : {kind}, no DAQMX device object could be created.")

        device : DAQMXDevice = device_class(id=id, 
                                deviceName=deviceName, 
                                modelName=modelName, 
                                nChannels=nChannels, 
                                state=status, 
                                freq=freq, 
                                dataLength=lData,
                                channels=[]) # see next few lines of code
    
        # creating the DAQMX channels:
        channels = []
        for _ in range(nChannels):
            data = [0.0 for _ in range(lData)] # default value see old code
            stim = [0.0 for _ in range(lData)] #  value see old code
            
            channels.append(DAQMXChannel(device=device, dataLength=lData, data=data, stim=stim))

        device.SetChannels(channels)
               
        return device
    