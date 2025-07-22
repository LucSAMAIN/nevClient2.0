#! usr/env/bin python3
# neclient.model.hardware.DAQMXChannel.py

from __future__ import annotations # to break circular import

class DAQMXChannel():
    """
    Defines the configuration
    of every channel for a specified
    DAQMXDevice.

    Attributes
    ----------
    device     : DAQMXDevice
        Channels belong to a specific DAQMX device.
    dataLength : int
        The data lenght of the channel's data.
        For static devices this parameter
        is set to 1.
        Whereas for dynamic devices it will be
        updated depending of the configuration.
    data       : list[float]
        The actual data stored by the channel.
    stim       : list[float]
        The stimulus to add.
        Both of the data and stim array need to
        be of size dataLength.
    index      : int
        The index position of the channel for the
        corresponding device.
    """

    def __init__(self, 
                 device     : DAQMXDevice,
                 dataLength : int,
                 data       : list[float],
                 stim       : list[float],
                 index      : int):
        self.device     = device
        self.index     = index
        self.dataLength = dataLength
        self.data       = data
        self.stim       = stim

# ──────────────────────────────────────────────────────────── Getters ────────────────────────────────────────────────────────── 

    def GetDevice(self) -> DAQMXDevice:
        return self.device
    def GetDataLenght(self) -> int:
        return self.dataLength
    def GetData(self) -> list[float]:
        return self.data
    def GetStim(self) -> list[float]:
        return self.stim
    def GetIndex(self) -> int:
        return self.index

# ──────────────────────────────────────────────────────────── Setters ────────────────────────────────────────────────────────── 

    def SetDevice(self, device : DAQMXDevice):
        self.device = device
    def SetDataLength(self, dataLength : int):
        self.dataLength = dataLength
    def SetData(self, data : list[float]):
        self.data = data
    def SetStim(self, stim : list[float]):
        self.stim = stim
    def SetIndex(self, index : int):
        self.index = index
