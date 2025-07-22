#! usr/env/bin python3
# nevclient.services.DataManipulation.DAQMXDataServices

# logger
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel

class DAQMXDataServices():
    """
    Set of useful methods helping manipulating DAQMX data.

    Public methods
    --------------
    FindDAQMXDevice:
        Returns an instance of a DAQMX device from csv name
        specifics : device name and channel info string.
    """

    def __init__(self):
        self.logger = Logger("DAQMXDataServices")

    def FindDAQMXDevice(self, deviceName : str, channelInfo : str, daqmxSys : DAQMXSys) -> DAQMXDevice:
        """
        This methods aims to retrieve the DAQMXDevice object by using information stored in the CSV parameter file.
        It is used to bind the parameters to the different DAQMX tasks and their channels.

        Parameters
        ----------
        deviceName  : str
            The name of the device
        channelInfo : str
            The channel information, e.g. "AO-0" or "DO-3"
        daqmxSys    : DAQMXSys
            The currently defined DAQMX system.
        
        Returns
        -------
        DAQMXDevice
            The DAQMXDevice object corresponding to the taskName and channelInfo.
            If not found or any other issue, returns None.
        """
        self.logger.deepDebug(f"Executing the FindDAQMXDevice method")

        if '-' not in channelInfo:
            self.logger.error(f"Invalid channel info format was passed in the GetDAQMXDevice method: {channelInfo}.")
            return None
        
        parts = channelInfo.split('-')
        channelType = parts[0]
        channelNum  = int(parts[1])
        
        device : DAQMXDevice
        for device in daqmxSys.GetDevicesMap().values():
            if not device.GetDeviceName() == deviceName:
                continue
            if   (channelType == "DO" and device.isDigital()) or \
                 (channelType == "AO" and device.isAnalog()):
                if channelNum < device.nChannels:
                    self.logger.deepDebug(f"Found matching device: {device.GetDeviceName()} for channel {channelNum}.")
                    return device
                # we keep looking
                self.logger.warning(f"Device '{deviceName}' found, but channel number {channelNum} is out of bounds (nChannels={device.GetnChannels()}).")

        self.logger.error(f"No suitable device found for taskName='{deviceName}' and channelInfo='{channelInfo}', returning a None value.")
        return None

    def GetDeviceData(self, dev : DAQMXDevice) -> list[list[float]]:
        """
        Return all the data of a device by serializing its channel's
        data.

        Parameters
        ----------
        dev : DAQMXDevice
            The device from which the caller wants to recover the
            serialized data.

        Returns
        -------
        list[list[float]]
        """
        result = []

        chn : DAQMXChannel
        for chn in dev.GetChannels():
            result.append(chn.GetData())
        
        return result
    
    def GetDeviceStim(self, dev : DAQMXDevice) -> list[list[float]]:
        """
        Return all the stimulus'data of a device 
        by serializing its channel's stimulus.

        Parameters
        ----------
        dev : DAQMXDevice
            The device from which the caller wants to recover the
            serialized stimulus'data.

        Returns
        -------
        list[list[float]]
        """
        result = []

        chn : DAQMXChannel
        for chn in dev.GetChannels():
            result.append(chn.GetStim())
        
        return result