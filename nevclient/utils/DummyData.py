#! usr/env/bin python3
# nevclient.utils.DummyData.py

# extern modules
import numpy as np
# psa status:
from nevclient.model.Enums.PSAStatus import PSAStatus
# utils
from nevclient.utils.Logger import Logger    



# Class to simulate the hardware configurations
class DummyData:
    """
    The DummyData class simulates the behavior of a real NEV control server.

    It holds hard-coded data structures and responses that mimic a physical
    hardware setup, allowing for offline testing of the client application.
    The class dynamically constructs response strings from its device dictionaries.

    Attributes
    ----------
    _NISCOPEDevices : list[str]
        A list of strings representing simulated PXI oscilloscope devices.
    _SAODevices : dict[tuple, dict]
        A dictionary for Static Analog Output devices.
        Keys are (slot, name, model) tuples.
        Values are dictionaries of device properties (nChannels, chassis, etc.).
    _DAODevices : dict[tuple, dict]
        A dictionary for Dynamic Analog Output devices, following the same
        structure as _SAODevices.
    _SDODevices : dict[tuple, dict]
        A dictionary for Static Digital Output devices, following the same
        structure as _SAODevices.
    _NISCOPEUnions : dict[int, dict[str, str]]
        A dictionary holding canned data for simulated hardware unions.
    DAQMXINFO : str
        A dynamically generated string response for a DAQMX info request.
    NISCOPEINFO : str
        A dynamically generated string response for a NISCOPE info request.
    NSUNUM : str
        A string response reporting the number of simulated unions.
    step : int
        The current step of a simulated Parameter Sweep Analysis (PSA).
    status : PSAStatus
        The current status of the simulated PSA.
    param : str
        The current parameter value for the simulated PSA.
    """

    def __init__(self):
        self.logger = Logger(name="DummyData")
        # ---- NI-SCOPE: A tiny "system" with PXI oscilloscopes
        self._NISCOPEDevices = [
            "[2,DEV0,NI5122,2,1,123456]",      # slot, name, model, N_ch, chassis, serial
            "[3,DEV1,NI5122,2,1,234567]",
        ]

        # ---- DAQmx: A tiny "system" for different DAQmx device types
        self._SAODevices = {
            (2, "DACS0", "PXI-6704"): {"nChannels": 16, "chassis": 1, "freq": 0.0, "state": 0},
            (3, "DACS1", "PXI-6704"): {"nChannels": 16, "chassis": 1, "freq": 0.0, "state": 0},
        }

        self._DAODevices = {
            (0, "DACD0", "PXI-6733"): {"nChannels": 8, "bufferSize": 1024, "freq": 100000.0, "state": 0},
            (1, "DACD1", "PXI-6733"): {"nChannels": 8, "bufferSize": 1024, "freq": 100000.0, "state": 0},
        }

        self._SDODevices = {
            (4, "DACS0", "PXI-6704"): {"nChannels": 8, "chassis": 1, "freq": 0.0, "state": 0},
            (5, "DACS1", "PXI-6704"): {"nChannels": 8, "chassis": 1, "freq": 0.0, "state": 0},
        }


        # ---- Per-union canned data for NI-SCOPE
        self._NISCOPEUnions = {
            0: {
                "NSUDEVS": "#NSUDEVS 0\n2 [0 1]\n#OK",
                "NSUCHAN": "#NSUCHAN 0\n4 [5.000000 DC][5.000000 DC][5.000000 DC][5.000000 DC]\n#OK",
                "NSUDLEN": "#NSUDLEN 0\n1024 [1024 1024 1024 1024]\n#OK",
                "NSUFREQ": "#NSUFREQ 0\n1000000.000000 [1000000.000000 1000000.000000 1000000.000000]\n#OK",
                "NSUTRIG": "#NSUTRIG 0\n[0.500000 EDGE 0 0 0.000000 POSITIVE DC 0.000000 0.000000]\n#OK"
            }
        }
        # self._NewNISCOPEUnions = {
        #     0: {
        #         "NDEVS"                 : 2,
        #         "DEVICES_ID"            : [0, 1],
        #         "NCHAN"                 : 4, 
        #         "CHAN_DATA"             : [{"RANGE": VerticalRange(5.0), "COUPLING": VerticalCoupling("DC")}, 
        #                                     {"RANGE": VerticalRange(5.0), "COUPLING": VerticalCoupling("DC")}, 
        #                                     {"RANGE": VerticalRange(5.0), "COUPLING": VerticalCoupling("DC")}
        #                                   ],
        #         "UNION_DLEN"            :  1024,
        #         "CHAN_DLEN"             : [1024, 1024, 1024, 1024],
        #         "UNION_FREQ"            : 1000000.000000,
        #         "CHAN_FREQ"             : [1000000.000000, 1000000.000000, 1000000.000000],
        #         "TRIG"                  : {"REF_POS": 0.5,
        #                                     "TRIG_TYPE": TriggerType("EDGE"),
        #                                     "TRIG_SOURCE": 0,
        #                                     "TRIG_DEVICE": 0,
        #                                     "TRIG_LEVEL":  0.0,
        #                                     "TRIG_SLOPE": TriggerSlope("POSITIVE"),
        #                                     "TRIG_COUPLING": TriggerCoupling("DC"),
        #                                     "TRIG_HOLDOFF": 0.0,
        #                                     "TRIG_DELAY": 0.0
        #                                 }
        #     }
        # }

        # ---- Single-value replies, dynamically constructed
        self.NISCOPEINFO = "#NISCOPEINFO\n" + "".join(self._NISCOPEDevices) + "\n#OK"
        self.NSUNUM      = f"#NSUNUM\n{len(self._NISCOPEUnions)}\n#OK"
        
        # Dynamically build DAQMXINFO from the device dictionaries
        self.DAQMXINFO = self._build_daqmx_info()

        # ---- PSA Status
        self.dynamic = False
        self.steps = 0
        self.status : PSAStatus = PSAStatus(PSAStatus.CONFIGURED)
        self.paramValue = 0.0
        self.paramValueHistory = []
        self.dataHistory = []
        self.maxSteps = 0
        self.nOutputs = 0 # nChannels
        self.increase = 0.0

    # ───────────────────────────────────────────────── INTERNAL METHODS ─────────────────────────────────────────────────────

    def _build_daqmx_info(self):
        """Constructs the full DAQMXINFO response string from device dictionaries."""
        
        def format_sao_sdo(key, props):
            # Format for SAO and SDO: [slot,name,model,N_ch,chassis,freq,state]
            return f"[{key[0]},{key[1]},{key[2]},{props['nChannels']},{props['chassis']},{props['freq']:.6f},{props['state']}]"

        def format_dao(key, props):
            # Format for DAO: [slot,name,model,N_ch,bufferSize,freq,state]
            return f"[{key[0]},{key[1]},{key[2]},{props['nChannels']},{props['bufferSize']},{props['freq']:.6f},{props['state']}]"

        sao_info = "SAO" + "".join([format_sao_sdo(k, v) for k, v in self._SAODevices.items()])
        dao_info = "DAO" + "".join([format_dao(k, v) for k, v in self._DAODevices.items()])
        sdo_info = "SDO" + "".join([format_sao_sdo(k, v) for k, v in self._SDODevices.items()]) # SDO has same format as SAO

        return f"#DAQMXINFO\n{sao_info}\n{dao_info}\n{sdo_info}\n#OK"

    # ───────────────────────────────────── PUBLIC METHODS CALLED BY THE TCPCLIENT ─────────────────────────────────────────

    def GetDAQMXInfo(self):
        return self.DAQMXINFO, ""

    def GetNISCOPEInfo(self):
        return self.NISCOPEINFO, ""

    def GetNSUNUM(self):
        return self.NSUNUM, ""

    def GetNSUDEVS(self, unionNo: int):
        return self._NISCOPEUnions[unionNo]["NSUDEVS"], ""

    def GetNSUCHAN(self, unionNo: int):
        return self._NISCOPEUnions[unionNo]["NSUCHAN"], ""

    def GetNSUDLEN(self, unionNo: int):
        return self._NISCOPEUnions[unionNo]["NSUDLEN"], ""

    def GetNSUFREQ(self, unionNo: int):
        return self._NISCOPEUnions[unionNo]["NSUFREQ"], ""

    def GetNSUTRIG(self, unionNo: int):
        return self._NISCOPEUnions[unionNo]["NSUTRIG"], ""

    def GetPSAStat(self):
        self.steps += 1
        if self.steps > self.maxSteps:
            self.status = PSAStatus(PSAStatus.COMPLETE)
            # return the old value
            if self.dynamic:
                self.logger.debug(f"steps {self.steps}, maxsteps {self.maxSteps}, paramhistory {self.paramValueHistory}")
                paramValue = sum([sum(l)/len(l) for l in self.paramValueHistory])/len(self.paramValueHistory)
            else:
                paramValue = self.paramValue
            return f"#PSASTAT\n {self.steps} {paramValue} {self.status}#OK", ""
        
        self.status = PSAStatus(PSAStatus.RUNNING)

        # Generation of the new sweeper value:
        if self.dynamic:
            for i in range(len(self.paramValue)):
                self.paramValue[i] += self.increase
            paramValue = sum(self.paramValue)/len(self.paramValue)
        else:
            self.paramValue += self.increase
            paramValue = self.paramValue

        self.paramValueHistory.append(self.paramValue.copy())

        return f"#PSASTAT\n {self.steps} {paramValue} {self.status}#OK", ""
        

    def GetPSAData(self, start : int, end : int):
        self._generatePSAData()
        
        header = f"#PSADATA {start} {end}\n"
        data = ""
        for i in range(start, end):
            if self.dynamic:
                data += str(sum(self.paramValueHistory[i])/len(self.paramValueHistory[i])) + "\n"
            else:
                data += str(self.paramValueHistory[i]) + "\n"
            dataList = self.dataHistory[i]
            # Format the list as a string like "[1.1 2.2 3.3]"
            data += "[" + " ".join(map(str, dataList)) + "]\n"
        
        end = "#OK"        

        return header + data + end, ""




    

    def SetPSA(self, maxSteps : int, dummyBaseParamValue : "float or list", nOutputs : int, dynamic : bool, start:float, end:float):
        """"
        The SetPSA method is used to set up the default values of the PSA simulation
        before running it.

        Parameters
        ----------
        maxSteps : int
            The number of steps the user selected in the sweeper panel.
        dummyBaseParamValue : float or list
            The current value of the DAQMX parameters / device selected 
            in the sweeper panel. I call this value "dummyBase" because
            it will be used to generate random values to be returned.
        nOutputs : int
            The size of the data list the backend server is supposed
            to respond after sending the GetPSAData command.
        dynamic : bool
            This parameter tell the method that the device is actually a dynamic
            device such as DAO or DDO. Which also means that their data
            is stored as 2D-list and not simple list of values.
        """
        self.dynamic = dynamic
        if self.dynamic:
            self.paramValue = [dummyBaseParamValue]
        else:
            self.paramValue = dummyBaseParamValue
        self.logger.debug(f"Set dummy base param value:{dummyBaseParamValue} of type {type(dummyBaseParamValue)}")
        self.maxSteps = maxSteps
        self.steps = 0
        self.status = PSAStatus.IDLE
        self.nOutputs = nOutputs
        self.increase = (end-start)/maxSteps
        self.dataHistory = []
        self.paramValueHistory = []

    def RunPSA(self):
        self.status = PSAStatus.RUNNING

    # ────────────────────────────────────────────── OTHER USEFUL METHODS ──────────────────────────────────────────────

    def _generatePSAData(self):
        # new data generation !
        # The new parameter value has already been generated
        # before during the GET PSA STAT
        num_samples = self.nOutputs
        x = np.linspace(0, 2 * np.pi, num_samples)
        # The core signal depends on the parameter
        signal = self.paramValue * np.sin(x) 
        # Add some random noise to make it look real
        noise = np.random.normal(0, 0.1, num_samples) 
        
        # We'll generate two channels of data for this example
        waveform_ch1 = list(signal + noise)
        
        # Store the generated data for this step
        self.dataHistory.append(waveform_ch1)