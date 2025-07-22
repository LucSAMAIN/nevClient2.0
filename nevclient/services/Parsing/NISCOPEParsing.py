#! usr/env/bin python3
# nevclient.services.Parsing.NISCOPEParsing

# extern modules
import re
# logger
from nevclient.utils.Logger import Logger
# NISCOPE
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice
from nevclient.model.Enums.NISCOPEChannelVerticalCoupling import NISCOPEChannelVerticalCoupling
from nevclient.model.Enums.NISCOPEChannelVerticalRange import NISCOPEChannelVerticalRange
from nevclient.model.Enums.NISCOPETriggerCoupling import NISCOPETriggerCoupling
from nevclient.model.Enums.NISCOPETriggerSlope import NISCOPETriggerSlope
from nevclient.model.Enums.NISCOPETriggerType import NISCOPETriggerType
from nevclient.model.hardware.NISCOPE.NISCOPEUnion import NISCOPEUnion
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel

class NISCOPEParsing():
    """
    Set of useful methods helping parsing server's answer about the NISCOPE system.

    Public methods
    --------------
    ParseNISCOPEInfo(self, text: str) -> dict[int : NISCOPEDevice]
    ParseNSUNUM(self, text: str) -> tuple[int, dict[int : NISCOPEUnion]]
    ParseNSUDEVS(self, text: str, unionMap : dict[int : NISCOPEUnion], devicesMap : dict[int : NISCOPEDevice])
    ParseNSUCHAN(self, text: str, unionMap : dict[int : NISCOPEUnion])
    ParseNSUDLEN(self, text: str, unionMap : dict[int : NISCOPEUnion])
    ParseNSUFREQ(self, text: str, unionMap : dict[int : NISCOPEUnion])
    ParseNSUTRIG(self, text: str, unionMap : dict[int : NISCOPEUnion])
    """

    def __init__(self):
        self.logger = Logger("NISCOPEParsing")



    def ParseNISCOPEInfo(self, text: str) -> dict[int : NISCOPEDevice]:
        """
        Parses the NISCOPE information string and fills the deviceMap.
        Usual input text:
        "#NISCOPEINFO\n[<device1-info> <device2-info>...]\n#OK"
        With device-info : [slot,deviceName,modelName,nChannels,chassis,serial]
        

        Parameters
        ----------
        text : str
            The NISCOPE information string to parse.
        
        Returns
        -------
        dict[int : NISCOPEDevice]:
            The map between niscope devices'id and their created instance.
        """
        self.logger.deepDebug(f"Executing the ParseNISCOPEInfo method")
        result = {}
        splitLines = text.splitlines()

        if splitLines[0] != "#NISCOPEINFO":
            self.logger.error("To use ParseNISCOPEInfo function, the input text must start by the '#NISCOPEINFO' flag.")
        
        # creating the different devices
        indiceCounter = 0
        for line in splitLines:
            if not line or line[0] == '#': # for the "#OK" or the "#DAQMXINFOS" lines
                continue

            for block in line.split(']'):
                if block.startswith('['):
                    deviceInfo = self._deviceInfoFromBlock(block, indiceCounter=indiceCounter)
                    result[deviceInfo.id] = deviceInfo
                    indiceCounter += 1


        self.logger.info(f"NISCOPESys successfully parsed the NISCOPE information.")
        return result

    def ParseNSUNUM(self, text: str) -> tuple[int, dict[int : NISCOPEUnion]]:
        """
        Parses the `GET NSU NUM` body from the server's answer.
        Updates the `nUnions` attributes.
        Usual text input format:
        ‘#NSUNUM\n<number-of-unions>\n#OK’ 

        Parameters
        ----------
        text : str
            The string to parse.
        
        Returns
        -------
        tuple[int, dict[int : NISCOPEUnion]]:
            The number of union and the dictionnary mapping niscope unions'id and their
            runtime instance.
        """
        self.logger.deepDebug(f"Executing the ParseNSUNUM method")
        splitLines = text.splitlines()

        if splitLines[0] != "#NSUNUM":
            self.logger.error("To use ParseNSUNUM function, the input text must start by the '#NSUNUM' flag.")
        
        nUnions = int(splitLines[1])
        unionMap = {}  # Initialize the unionMap to store unions by their ID
        indiceCounter = 0
        for _ in range(nUnions):
            union = NISCOPEUnion(
                dlen=0,
                freq=0.0,
                refPosition=0.0,
                triggerType=NISCOPETriggerType.IMMEDIATE,
                triggerSource="0",  
                triggerDevice=0,  # Default device ID
                triggerLevel=0.0,
                triggerSlope=NISCOPETriggerSlope.POSITIVE,
                triggerCoupling=NISCOPETriggerCoupling.DC,  
                triggerHoldoff=0.0,
                triggerDelay=0.0,
                nChannels=0,
                id = indiceCounter,
                devicesMap=dict() # later set up via nsu devs
            )
            unionMap[union.GetId()] = union  # Use the UUID as the key

            indiceCounter += 1

        self.logger.info(f"Successfully parsed the `GET NSU NUM`")
        return nUnions, unionMap

    def ParseNSUDEVS(self, text: str, unionMap : dict[int : NISCOPEUnion], devicesMap : dict[int : NISCOPEDevice]):
        """
        Parses the `GET NSU DEVS` body from the server's answer.
        Updates the NISCOPEUnion(s) contained in the `unionList` attributes.
        Usual text input format:
        ‘#NSUDEVS unionNo\n<device-count> [<device-idx> …]\n#OK’

        When you call the 'GET NSU DEVS unionId' command,
        the servers replies wit a list of all the devices index in the union.
        Basically, every device as a unique index within the range [0, nDevices-1].
        The backend code look wich local device index of the union == global device index of the system.
        And return these global indexes in the response.

        Parameters
        ----------
        text : str
            The string to parse.
        unionMap : dict[int : NISCOPEUnion]
            The NISCOPE system's dictionnary mapping unions'id to their runtime instance.
        devicesMap : dict[int : NISCOPEDevice]
            The NISCOPE system's dictionnary mapping devices'id to their runtime instance. 
        """
        self.logger.deepDebug(f"Executing the ParseNSUDEVS method")
        splitLines = text.splitlines()
        if not splitLines or not splitLines[0].startswith("#NSUDEVS"):
            self.logger.error("To use ParseNSUDEVS function, the input text must start by the '#NSUDEVS' flag.")

        # We need to retrieve the union number from the first line
        parts = splitLines[0].split()
        unionNo = int(parts[1]) 

        # Copy from the old code... Since I have no idea how the real format looks like
        dev_line = splitLines[1]
        start_idx = dev_line.find("[")
        # Number of devices in the union
        n_devices = int(dev_line[:start_idx])

        # Scan list of channel confs (????)
        blks = dev_line[start_idx:].split("]")
        lst = blks[0][1:].split() 

        if len(lst) < n_devices:
            self.logger.error("Device index list too short in NSUDEVS response.")

        union : NISCOPEUnion
        union = unionMap.get(unionNo)
        if union is None:
            self.logger.error(f"Union with ID {unionNo} not found in the unionMap.")

        # Update the union's devices map
        unionDevicesMap = {}
        for i in range(n_devices):
            device_idx = int(lst[i])
            unionDevicesMap[device_idx] = devicesMap[device_idx]
        union.SetDevicesMap(unionDevicesMap)

        self.logger.info(f"Succesfully parsed NSUDEVS for union {unionNo}: {lst}")

    def ParseNSUCHAN(self, text: str, unionMap : dict[int : NISCOPEUnion]):
        """
        Parses the `GET NSU CHAN` body from the server's answer.
        Updates the NISCOPEUnion(s) contained in the `unionList` attributes.
        Usual text input format:
        '#NSUCHAN <unionNo> \n <N_channels> [<range1> <coup1>][<range2> <coup2>]...[<rangeN> <coupN>] \n #OK'

        Parameters
        ----------
        text : str
            The string to parse.
        unionMap : dict[int : NISCOPEUnion]
            The NISCOPE system's dictionnary mapping unions'id to their runtime instance.
        """
        self.logger.deepDebug(f"Executing the ParseNSUCHAN method")
        splitLines = text.splitlines()
        if not splitLines or not splitLines[0].startswith("#NSUCHAN"):
            self.logger.error("To use ParseNSUCHAN function, the input text must start by the '#NSUCHAN' flag.")

        parts = splitLines[0].split()
        unionNo = int(parts[1])

        chan_line = splitLines[1]
        start_idx = chan_line.find("[")

        n_channels = int(chan_line[:start_idx])
        src = chan_line[start_idx:]

        union : NISCOPEUnion
        union = unionMap.get(unionNo)
        if union is None:
            self.logger.error(f"Union with ID {unionNo} not found in the unionMap.")

        # Retrieve an ordered list of the devices indexes:
        device_indexes = list(union.GetDevicesMap().keys())
        device_indexes.sort()  # Ensure the devices are in order because the backend server returns them in order of their index

        channel_blocks = [blk for blk in src.split("]") if blk.startswith("[")] # in the form ["[range coupling", "[range coupling", ... ]
        idx = 0
        for devIndx in device_indexes:
            dev : NISCOPEDevice
            dev = union.GetDevicesMap().get(devIndx)
            chvr_list = [] # temp list to store the config of the cannal vertical range of the current device
            chvc_list = [] # temp list to store the config of the cannal vertical coupling of the current device
            for _ in range(dev.nChannels):
                # If we have more defined channels than the information we received from the server -> error
                if idx >= len(channel_blocks):
                    self.logger.error("Not enough channel blocks for all devices.")
                    break
                lst = channel_blocks[idx][1:].split() # 1: to remove the leading '[', and split to get "range" and "coupling"
                if len(lst) < 2:
                    self.logger.error(f"unexpected response from server ({channel_blocks[idx]})")
                    chvr_list.append(None)
                    chvc_list.append(None)
                else:
                    chvr_list.append(lst[0])
                    chvc_list.append(lst[1])
                idx += 1

            # Update the device of the union
            channel : NISCOPEChannel
            for i, channel in enumerate(dev.GetChannels()):
                channel.SetVerticalRange(NISCOPEChannelVerticalRange(float(chvr_list[i]))) # Convert to the NISCOPEChannelVerticalRange enum
                channel.SetVerticalCoupling(NISCOPEChannelVerticalCoupling(chvc_list[i]))  # Convert to NISCOPEChannelVerticalCoupling enum

        union.SetNChannels(n_channels)
        self.logger.info(f"Succesfully parsed NSUCHAN for union {unionNo}: {n_channels} channels")



    def ParseNSUDLEN(self, text: str, unionMap : dict[int : NISCOPEUnion]):
        """
        Parses the `GET NSU DLEN` body from the server's answer.
        Updates the NISCOPEUnion(s) contained in the `unionList` attributes.
        Usual text input format:
        ‘#NSUDLEN unionNo\n<dlen> [deviceDLen0 deviceDLen1 ...]\n#OK’

        Parameters
        ----------
        text : str
            The string to parse.
        unionMap : dict[int : NISCOPEUnion]
            The NISCOPE system's dictionnary mapping unions'id to their runtime instance.
        """
        self.logger.deepDebug(f"Executing the ParseNSUDLEN method")
        # Entire block up to the opening bracket
        pattern = (
                r'#NSUDLEN\s+(\d+)\s*\r?\n'
                r'\s*(\d+)\s*\[((?:\d+\s*)+)]\s*\r?\n'
                r'\s*#OK\b'
        )

        m = re.search(pattern, text)
        if not m:
            self.logger.error("Malformed NSUDLEN response or missing #OK line.")

        unionNo = int(m.group(1))
        dlen = int(m.group(2))
        lst = m.group(3).split()

        union : NISCOPEUnion
        union = unionMap.get(unionNo)
        if union is None:
            self.logger.error(f"Union with ID {unionNo} not found in unionMap.")

        n_devices = len(union.GetDevicesMap())
        if len(lst) < n_devices:
            self.logger.error("ParseNSUDLEN: data length list too short")
            return None

        # update dlen
        union.SetDlen(dlen)
        
        # Same as fo the ParseNSUCHAN function, we need to retrieve an ordered list of the devices indexes:
        device_indexes = list(union.GetDevicesMap().keys())
        
        # The following line has been commented
        # because since python 3.7
        # keys() are ensured to be returned in the order
        # they have been inserted in the dict
        # device_indexes.sort()  # Ensure the devices are in order because the backend server returns them in order of their index

        for i, devIndex in enumerate(device_indexes):
            dev : NISCOPEDevice
            dev = union.GetDevicesMap().get(devIndex)
            if dev is None:
                self.logger.error(f"Device with index {devIndex} not found in union {unionNo}.")
                continue
            

            # Update the device's actual data length
            devActualDlen = int(lst[i])
            dev.SetActualDlen(devActualDlen)

        self.logger.info(
            f"Succesfully parsed NSUDLEN for union {unionNo}: "
            f"dlen={dlen}, devActualLen={lst}"
        )



    def ParseNSUFREQ(self, text: str, unionMap : dict[int : NISCOPEUnion]):
        """
        Parses the `GET NSU FREQ` body from the server's answer.
        Updates the NISCOPEUnion(s) contained in the `unionList` attributes.
        Usual text input format:
        ‘#NSUFREQ unionNo\n<minSampleRate> [<actualDeviceSampleRate> <actualDeviceSampleRate> ...]\n#OK’

        Parameters
        ----------
        text : str
            The string to parse.
        unionMap : dict[int : NISCOPEUnion]
            The NISCOPE system's dictionnary mapping unions'id to their runtime instance.
        """
        self.logger.deepDebug(f"Executing the ParseNSUFREQ method")
        pattern = (
            r'#NSUFREQ\s+(\d+)\s*\r?\n'                        # union ID
            r'\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*'   # minSampleRate
            r'\[((?:[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*)+)]\s*\r?\n'  # list of sample rates
            r'\s*#OK\b'                                        # terminator
        )

        m = re.search(pattern, text)
        if not m:
            self.logger.error("Malformed NSUFREQ response.")

        unionNo        = int(m.group(1))
        minRate        = float(m.group(2))
        sample_rates   = [float(v) for v in m.group(3).split()]

        union : NISCOPEUnion
        union = unionMap.get(unionNo)
        if union is None:
            self.logger.error(f"Union with ID {unionNo} not found in unionMap.")

        n_devices = len(union.GetDevicesMap())
        if len(sample_rates) < n_devices:
            self.logger.error("ParseNSUFREQ: sample-rate list too short")
            return None

        # Update the min freq rate for the union
        union.SetFreq(minRate)
        
        # Same as for the ParseNSUCHAN function, we need to retrieve an ordered list of the devices indexes:
        device_indexes = list(union.GetDevicesMap().keys())
        
        # The following line has been commented
        # because since python 3.7
        # keys() are ensured to be returned in the order
        # they have been inserted in the dict
        # device_indexes.sort()  # Ensure the devices are in order because the backend server returns them in order of their index

        for i, devIndex in enumerate(device_indexes):
            dev : NISCOPEDevice
            dev = union.GetDevicesMap().get(devIndex)
            if dev is None:
                self.logger.error(f"Device with index {devIndex} not found in union {unionNo}.")
                continue
            
            # Update the device's actual sample rate
            devActualSampleRate = sample_rates[i]
            dev.SetActualFreq(devActualSampleRate)


        self.logger.info(
            f"Parsed NSUFREQ for union {unionNo}: "
            f"minRate={minRate}, devActualSampleRate={sample_rates}"
        )




    def ParseNSUTRIG(self, text: str, unionMap : dict[int : NISCOPEUnion]):
        """
        Parses the `GET NSU TRIG` body from the server's answer.
        Updates the NISCOPEUnion(s) contained in the `unionList` attributes.
        Usual text input format:
        ‘#NSUTRIG unionNo\n<trig> [refPosition trigger_type triggerSource trigger_device triggerLevel trigger_slope trigger_coupling triggerHoldoff triggerDelay]\n#OK’
        
        Parameters
        ----------
        text : str
            The string to parse.
        unionMap : dict[int : NISCOPEUnion]
            The NISCOPE system's dictionnary mapping unions'id to their runtime instance.
        """
        self.logger.deepDebug(f"Executing the ParseNSUTRIG method")
        splitLines = text.splitlines()
        if not splitLines or not splitLines[0].startswith("#NSUTRIG"):
            self.logger.error("To use ParseNSUTRIG function, the input text must start by the '#NSUTRIG' flag.")
        
        # We need to retrieve the union number from the first line
        parts = splitLines[0].split() # Not sure of that since it was not the case in the original code
        unionNo = int(parts[1])


        # Copy from the old code... Since I have no idea how the real format looks like
        trig_line = splitLines[1]
        start_idx = trig_line.find("[")        
        blks = trig_line[start_idx:].split("]")
        lst = blks[0][1:].split()
        if len(lst) < 9:
            self.logger.error("Trigger configuration list too short in NSUTRIG response.")

        union : NISCOPEUnion
        union = unionMap.get(unionNo)
        if union is None:
            self.logger.error(f"Union with ID {unionNo} not found in the unionMap.")

        # We can now fill the union with the parsed data
        union.SetRefPosition(float(lst[0]))
        union.SetTriggerType(NISCOPETriggerType.from_string(lst[1]))
        union.SetTriggerSource(lst[2])
        union.SetTriggerDevice(int(lst[3]))
        union.SetTriggerLevel(float(lst[4]))
        union.SetTriggerSlope(NISCOPETriggerSlope.from_string(lst[5]))
        union.SetTriggerCoupling(NISCOPETriggerCoupling.from_string(lst[6]))
        union.SetTriggerHoldoff(float(lst[7]))
        union.SetTriggerDelay(float(lst[8]))

        self.logger.info(f"Parsed NSUTRIG for union {unionNo}: {lst}")






    def _deviceInfoFromBlock(self, block : str, indiceCounter : int) -> NISCOPEDevice:
        """
        Helper function for the ParseNISCOPEInfo function

        Parameters
        ----------
        block : str
            The string to parse.
        indiceCounter : int
            The indiceCounter of the NISCOPE devices.
        
        Returns
        -------
        NISCOPEDevice
            The NISCOPEDevice object parsed from the string block
        """
        f = block[1:].split(',')
        slot = int(f[0])
        deviceName = str(f[1])
        modelName  = str(f[2])
        nChannels  = int(f[3])
        chassis    = int(f[4])
        serial     = int(f[5])
        
        id = indiceCounter 

        actualFreq = 0.0 # default value
        actualDlen = 0

        device = NISCOPEDevice(id=id,
            slot=slot,
            deviceName=deviceName,
            modelName=modelName,
            nChannels=nChannels,
            chassis=chassis,
            serial=serial,
            actualFreq=actualFreq,
            actualDlen=actualDlen,
            channels = [] # see the next few lines
            )

        # creating the channels:
        channels = []
        self.logger.deepDebug(f"Creating NISCOPE channels for device:{device}")
        for index in range(nChannels):
            self.logger.deepDebug(f"index={index}")
            chn = NISCOPEChannel(device=device,
                           index=index,
                           verticalRange=NISCOPEChannelVerticalRange.ONE,
                           verticalCoupling=NISCOPEChannelVerticalCoupling.DC) # both default values I decided to set
            self.logger.deepDebug(f"created niscope channel with range : {chn.GetVerticalRange()} and coupling : {chn.GetVerticalCoupling()}")
            channels.append(chn)

        device.SetChannels(channels) 
        self.logger.deepDebug(f"Set channels for the device:{device.GetChannels()}")


        return device


    def _buildTotalNumberOfChannelsNISCOPE(self, niscopeSys : NISCOPESys):
        """
        This method returns the total number
        of defined NISCOPE channels.

        Parameters
        ----------
        niscopeSys : NISCOPESys
            The NISCOPE system instance

        Returns
        -------
        int
        """
        totalChannelsCounter = 0
        deviceMap = niscopeSys.GetDeviceMap()
        for deviceInfo in deviceMap.values():
            totalChannelsCounter += deviceInfo.GetNChannels()
        return totalChannelsCounter