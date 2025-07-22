#! usr/env/bin python3
# nevclient.services.DataManipulation.DAQMXDataServices

# extern import
import numpy as np
# logger
from nevclient.utils.Logger import Logger
# DAQMX
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
from nevclient.model.hardware.DAQMX.DAQMXDevice import DAQMXDevice
from nevclient.model.hardware.DAQMX.DAQMXChannel import DAQMXChannel
from nevclient.model.hardware.DAQMX.DAQMXDynamicDevice import DAQMXDynamicDevice

class DAQMXDataServices():
    """
    Set of useful methods helping manipulating DAQMX data.

    Public methods
    --------------
    FindDAQMXDevice(self, deviceName : str, channelInfo : str, daqmxSys : DAQMXSys) -> DAQMXDevice:
        Returns an instance of a DAQMX device from csv name
        specifics : device name and channel info string.
    StimUpdate(self, daqmxSys : DAQMXSys, dlen : int, freq : float) -> None:
        Updates all the dynamic DAQMX devices based on the T and dt configuration
    GetDeviceData(self, dev : DAQMXDevice) -> list[list[float]]:
        Returns all the data of a device by serializing its channel's
        data.
    GetDeviceStim(self, dev : DAQMXDevice) -> list[list[float]]:
        Returns all the stimulus'data of a device by serializing its channel's stimulus.
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
        Returns all the data of a device by serializing its channel's
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
        Returns all the stimulus'data of a device 
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
    

    def StimUpdate(self, daqmxSys : DAQMXSys, dlen : int, freq : float):
        """
        Updates all the dynamic DAQMX devices based on the T and dt configuration
        settings set by the user in the stim panel. It is especially called by the PulseDataServices
        to update the DAQMX model.

        Parameters
        ----------
        dlen : int
            The new data lenght to set.
        freq : float
            The new sampling frequency value.
        """
        DAQMXDev : DAQMXDevice
        for DAQMXDev in daqmxSys.GetDevicesMap().values():
            if not DAQMXDev.isDynamic():
                continue
            DAQMXDev.SetDataLength(dlen)
            DAQMXDev.SetFreq(freq)


    def PulseUpdate(self, daqmxSys : DAQMXSys, device : DAQMXDynamicDevice, chn : int, stim : np.array):
        """
        This methods updates the waveforms (pulses for the user)
        defined in the gui panel.
        The data is computed by the pulse data services and sent
        to this method so we can easily updates the devices accordingly.

        Attention
        ---------
        ALL THE DYNAMIC DEVICES WILL SEE THEIR STIM VALUE
        RESET EXCEPT THE CURRENTLY SELECTED ONE.
        THIS BEHAVIOUR IS STRANGE BUT DEFINED AS
        SUCH IN THE OLD CODE. ONE MIGHT WANT TO
        UPDATE THIS IN THE FUTURE. I WOULD BE 
        PRETTY EASY : 
        - FIRST NEED TO ENSURE THAT THE FIRST PULSE
        IS DEACTIVE BY DEFAULT. IT PREVENTS TO SET 
        A DEFAULT STIM TO ALL THE DYNAMIC DEVICES
        WHEN CSV FILE IS LOADED.
        - SECONDLY CHANGE THE CORRESPONDING _computeAndSync
        PRIVATE METHOD IN THE PULSE DATA SERVICES TO
        COMPUTE THE STIM DATA FOR EVERY DEVICES.
        - LASTLY UPDATE THIS METHOD BY PASSING
        A LIST OF DEVICES AND CHANNELS INSTEAD OF ONLY ONE
        AND CHANGE THE FORMAT OF THE STIM PARAMETER.

        Parameters
        ----------
        daqmxSys     : DAQMXSys
            The daqmxs system instance.
        device       : DAQMXDevice
            The DAQMX device instance we need to set the new stim value.
        chn          : int
            The device's channel on which the pulse parameter is binded.
        stim         : np.array
            The pulse waveform to set. 
        """
        self.logger.debug("The PulseUpdate service has been called.")
        # converting the np.array accordingly:
        stim  = list(stim.astype(float).tolist()) # must be of size dlen
        if len(stim) != device.GetDataLength():
            raise Exception(f"Inside the PulseUpdate service tried to set a stim of length : {len(stim)} != device.lData : {device.GetDataLength()} for device: {device}")
        
        for dev in daqmxSys.GetDevicesMap().values():
            if not dev.isDynamic():
                continue
            # cleaning every stim attribute for every of channel of every dynamic device
            for channel in dev.GetChannels():
                channel.SetStim([])
        
        device.GetChannels()[chn].SetStim(stim)
        self.logger.debug("The PulseUpdate service has been succesfully executed.")