#! usr/env/bin python3
# nevclient.services.DataManipulation.PulseDataServices

# extern modules
import numpy as np
# logger
from nevclient.utils.Logger import Logger
# pulse
from nevclient.model.config.Pulse.PulseData import PulseData
from nevclient.model.config.Pulse.PulseConf import PulseConf
# services
from nevclient.services.DataManipulation.DAQMXDataServices import DAQMXDataServices
# daqmx
from nevclient.model.hardware.DAQMX.DAQMXSys import DAQMXSys
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData

class PulseDataServices():
    """
    Set of useful methods helping manipulating Pulse data.

    Public methods
    --------------
    UpdateDAQMXStim(pulse : PulseData, daqmxDMServ : DAQMXDataServices) -> None
        Updates the dynamix DAQMX devices stimulus attributes after
        the user decided to change the configuration on the pulse
        panel. This method also call a DAQMXDataServices instance
    """
    def __init__(self):
          self.logger = Logger("PulseDataServices")

# ──────────────────────────────────────────────────────────── Public methods ──────────────────────────────────────────────────────────

    def UpdateDAQMXStim(self,
                        pulse          : PulseData,
                        daqmxDMServ    : DAQMXDataServices,
                        daqmxSys       : DAQMXSys):
        """
        This method is mainly used by the pulse panel
        when the user decide to interact with one of
        the configuration settings (delay, amp, active, ...)

        Parameters
        ----------
        pulse          : PulseData
            The runtime PulseData instance.
        daqmxDMServ    : DAQMXDataServices
        daqmxSys       : DAQMXSys
        """    
        self.logger.debug("Calling the UpdateDAQMXStim service")
        # (1) first compute the 
        # common parameters (stim common)
        # sampling frequence
        # and data lenght
        dlen, freq = self._computeCommonParam(pulse)
        

        # (2) secondly compute the waveformes
        # (pulses)
        confs = pulse.GetParamToPulsesConfigurationMap()[pulse.GetCurParameter().GetName()]
        T = pulse.GetStimData().GetT()
        dt = pulse.GetStimData().GetDt()
        _, y = self._computeStimulus(T, dt, confs)
        # we now have the wave form (pulses)
        # defined by the user inside the corresponding panel
        # we can set the DAQMX devices accordingly.
        

        # (3) Updates the DAQMX system
        channel      = pulse.GetCurParameter().GetChannel()
        bindedDevice = channel.GetDevice()
        channelId    = channel.GetIndex()
        daqmxDMServ.StimUpdate(daqmxSys, dlen, freq)
        daqmxDMServ.PulseUpdate(daqmxSys, bindedDevice, channelId, y)


# ──────────────────────────────────────────────────────────── Intern methods ──────────────────────────────────────────────────────────

    def _computeStimulus(self, T : float, dt : float, confs : list[PulseConf]) -> tuple[np.array, np.array]:
        """
        This private method is used to compute
        the actual pulse data generated from
        the configuration settings.

        Parameters
        ----------
        T    : int
        dt   : float
            These two parameters are the one defined in the
            Stim panel.
        confs : list[PulseConf]
            The pulse configurations of the parameter
            we are dealing with 

        Returns
        -------
        tuple[np.array, np.array]:
            The timing and actual data arrays.
        """
        self.logger.deepDebug("Entering the _computeStimulus method")
        # Time and amp set up
        t = np.arange(0, T, dt) # of size dlen !
        data = np.zeros(len(t))         

        conf : PulseConf
        for conf in confs:
            if not conf.GetActive():
                continue
            
            # Retrieving the configuration data
            delay_ms = conf.GetDelay()
            width_ms = conf.GetWidth()
            amp_mv = conf.GetAmp()
            
            # Computing indexes
            start_index = int(delay_ms / dt)
            width_index = int(width_ms / dt)
            end_index = start_index + width_index

            
    
            effective_end_index = np.minimum(end_index, len(data))
            data[start_index:effective_end_index] += amp_mv
        
        self.logger.deepDebug(f"Computed stimulus: {data/1000} of size {len(data)}")
        return t, data/1000 # we work in mv
    
    def _computeCommonParam(self, pulse : PulseData):
        """
        The _computeCommonParam method is used internally to
        compute the actual stimulus based on the attributes.
        It returns the new data lenght integer value
        and sampling frequency float value.

        Parameters
        ----------
        pulse     : PulseData
            The runtime PulseData instance.

        Returns
        -------
        tuple[int, float]:
            dlen, freq
        """
        self.logger.deepDebug("Entering the _computeCommonParam method")
        # because old code was doing:
        # L_data = int(T / dt) + 1
        # freq = 1000.0 / dt
        T  = pulse.GetStimData().GetT()
        dt = pulse.GetStimData().GetDt()
        dlen = int(np.ceil(T/dt))
        freq = 1000.0 / dt

        return dlen, freq
