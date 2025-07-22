#! usr/env/bin python3
# nevclient.services.DataManipulation

# extern modules
import colorsys
# logger
from nevclient.utils.Logger import Logger
# NISCOPE
from nevclient.model.hardware.NISCOPE.NISCOPESys import NISCOPESys
from nevclient.model.hardware.NISCOPE.NISCOPEDevice import NISCOPEDevice
from nevclient.model.hardware.NISCOPE.NISCOPEChannel import NISCOPEChannel

class NISCOPEDataServices():
    """
    Set of useful methods helping manipulating NISCOPE data.

    Public methods
    --------------
    GetTotalNumberOfChannels() -> int
    GetChannelColors(self, niscopeSys : NISCOPESys) -> dict[int, dict[int, str]]
        Associates a color to each channel of every device
        currently defined inside the NISCOPE system
    """
    def __init__(self):
        self.logger = Logger("NISCOPEDataServices")
    
    def GetTotalNumberOfChannels(self, niscopeSys : NISCOPESys) -> int:
        """
        Returns the total number of channels of all the devices
        defined in the NISCOPE system.

        Returns
        -------
        int
        """
        result = 0
        device : NISCOPEDevice
        for device in niscopeSys.GetDevicesMap().values():
            result += device.GetNChannels()
        return result

    def GetChannelColors(self, niscopeSys : NISCOPESys) -> dict[int, dict[int, str]]:
        """
        Generates a unique color for each channel of every NISCOPE device.
        This method iterates through all devices, counts the total number of channels,
        and then assigns a unique, mathematically distributed color in the HSV color
        space to each channel. This avoids using a predefined list and scales to
        any number of channels.

        Parameters
        ----------
        niscopeSys : NISCOPESys
            The NISCOPE system instance
        
        Returns
        -------
        dict[int, dict[int, str]]
            A dictionary where:
            - The key is the a tuple combining the index of the NISCOPE Device
            - The value is a dictionnary mapping every device's channel index to its html string generated color 
        """

        deviceMap = niscopeSys.GetDevicesMap()

        channelColorsMap = {}
        channelCounter = 0


        totalChannelsCounter = self.GetTotalNumberOfChannels(niscopeSys)

        # Iterate through each device and its index
        for deviceIndex, device in deviceMap.items():
            # For every device we map a new dictionnary that maps channel index to color
            ChannelColorMap = {}
            # Iterate through each channel for the current device
            for channelIndex in range(device.GetNChannels()):
                

                # Calculate the Hue (the "color" part) by distributing it evenly
                # This ensures colors are visually distinct
                hue = channelCounter / totalChannelsCounter
                
                saturation = 0.9
                value = 0.95
                
                # Convert the HSV color to RGB. The values are floats from 0.0 to 1.0.
                RGBFloat = colorsys.hsv_to_rgb(hue, saturation, value)
                
                # Convert the RGB float values (0.0-1.0) to integer values (0-255)
                RGBInt = [int(c * 255) for c in RGBFloat]
                
                # Format the RGB integers into a hex color string (e.g., #ff8000)
                hexColor = f'#{RGBInt[0]:02x}{RGBInt[1]:02x}{RGBInt[2]:02x}'
                
                # For every device we map a new dictionnary that maps channel index to color
                ChannelColorMap[channelIndex] = hexColor

            
                channelCounter += 1

            # Add the channels color map to the final dict
            channelColorsMap[deviceIndex] = ChannelColorMap
                
        return channelColorsMap
