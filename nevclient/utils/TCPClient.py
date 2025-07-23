#! usr/env/bin python3
# app.utils.TCPClient.py

# extern modules
from __future__ import annotations
import socket
# utils
from nevclient.utils.Logger import Logger
from nevclient.utils.DummyData import DummyData
# parameters
from nevclient.model.config.Parameters.CSVParameter import CSVParameter
from nevclient.model.config.PSA.SweepConf import SweepConf
# psa
from nevclient.model.config.PSA.PSAData import PSAData
# services
from nevclient.services.DataManipulation.PSADataServices import PSADataServices




_END_OK, _END_ERR = b"#OK", b"#NG"


class TCPClient:
    """
    Thin, blocking TCP client for the NEV control server.

    You can use the class in a ``with`` statement, or call :py:meth:`_close`
    manually.  When *simulate* is *True* the socket layer is bypassed and
    hard-coded answers held in :class:`DummyData` are returned instead.

    Parameters
    ----------
    host : str, default ``"localhost"``
        Server hostname or IP address.
    port : int, default ``9000``
        TCP port used by the NEV server.
    timeout : float, keyword-only, default ``5.0``
        Read / write timeout (seconds).
    bufsize : int, keyword-only, default ``8192``
        Size of each ``recv`` chunk.
    simulate : bool, keyword-only, default ``False``
        Activate dummy mode (no network traffic).
    """
    SIMULATE = False


    def __init__(
        self,
        host: str = "localhost",
        port: int = 9000,
        *,
        timeout: float = 5.0,
        bufsize: int = 8192, # chunk
        psa : PSA = None # sometimes needed inside the simulate method
    ):
        self.logger = Logger("TCPClient")

        self.host, self.port = host, port
        self.timeout, self.bufsize = timeout, bufsize
        self.sock: socket.socket = None
        
        self.psa = psa

        self.logger.debug(f"SIMULATE var: {TCPClient.SIMULATE}")
        if TCPClient.SIMULATE:
            self.logger.debug("Creating TCPClient instance in simulate mode")
            self.simulate = True
            self._simData: DummyData = DummyData()
            self._dao_pending: bool = False
        else:
            
            self.simulate = False
            self._connect()
            
        
        

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._close()




    # ───────────────────────────────────────────────── INTERN METHODS ─────────────────────────────────────────────────────

    def _close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    # make the request to the backend
    def _request(self, cmd: str) -> str:
        """
        Send *cmd* to the server (or simulator) and return the body.
        
        Parameters
        ----------
        cmd : str
            The command to send to the backend server, e.g. ``"GET SAO 6"``

        Returns
        -------
        str
            The answer's body from the server.
        """
        if self.simulate:
            body, err = self._simulate(cmd)
        else:
            self._send(cmd + "\n")
            body, err = self._recv_until_marker()

        if err:
            raise Exception(err)
        if "FAILED" in body:
            # PSA STAT fail:
            errMessage = body.split()[5]
            raise Exception(errMessage)


        return body

    # socket primitives
    def _connect(self):
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.sock.settimeout(self.timeout)

    def _send(self, text: str):
        self.sock.sendall(text.encode())

    def _recv_until_marker(self) -> tuple[str, str]:
        buf = bytearray()
        while True:
            chunk = self.sock.recv(self.bufsize)
            if not chunk:
                self.logger.error("Connection closed by the server")
            buf.extend(chunk)
            if _END_OK in buf or _END_ERR in buf:
                break
        data = buf.decode()
        if "#NG" in data:
            _, _, err = data.partition("#NG")
            return "", err.strip()
        body, *_ = data.partition("#OK")
        return body.strip(), None
    


    # ────────────────────────────────────────────────── SIMULATE MEHOD ─────────────────────────────────────────────────────

    
    def _simulate(self, cmd: str) -> tuple[str, str]:
        """
        Return the answer that a real server would send for *cmd*.

        Parameters
        ----------
        cmd : str
            Command line sent by the user, e.g. ``"GET SAO 6"``.

        Returns
        -------
        tuple[str, str]
            *(body, error_message)* – if an operation is unsupported
            *error_message* is a brief description, otherwise it is ``""``.
        """
        tokens = cmd.strip().split()
        verb   = tokens[0]
        self.logger.deepDebug(f"_simulate : {cmd}")




        # ────────────────────────────────────── GET ──────────────────────────────────────
        if verb == "GET":
            if tokens[1] == "DAQMXINFO":
                return self._simData.GetDAQMXInfo()
            elif tokens[1] == "NISCOPEINFO":
                return self._simData.GetNISCOPEInfo()


            elif tokens[1] == "NSU":
                if tokens[2] == "NUM":
                    return self._simData.GetNSUNUM()
                elif tokens[2] == "TRIG":
                    return self._simData.GetNSUTRIG(int(tokens[3]))
                elif tokens[2] == "DEVS":
                    return self._simData.GetNSUDEVS(int(tokens[3]))
                elif tokens[2] == "CHAN":
                    return self._simData.GetNSUCHAN(int(tokens[3]))
                elif tokens[2] == "DLEN":
                    return self._simData.GetNSUDLEN(int(tokens[3]))
                elif tokens[2] == "FREQ":
                    return self._simData.GetNSUFREQ(int(tokens[3]))
            
            elif tokens[1] == "PSA":
                if tokens[2] == "STAT":
                    return self._simData.GetPSAStat()
                if tokens[2] == "DATA":
                    # GET PSA DATA <start>-<end>
                    startEndString = tokens[3]
                    start = startEndString.split('-')[0]
                    end = startEndString.split('-')[1]
                    if not(end): # case we want the whole thing
                        end = len(self._simData.paramValueHistory)

                    return self._simData.GetPSAData(int(start), end)


        # ────────────────────────────────────── SET ──────────────────────────────────────


        if verb == "SET":
            if tokens[1] == "SAO":
                return f"#OK", ""
            elif tokens[1] == "SDO":
                return f"#OK", ""
            elif tokens[1] == "DAO":          # step 1
                if len(tokens) ==  4: # SET DAO <taskNo> <ch_start>"
                    task_no = int(tokens[2])
                    ch_start = int(tokens[3])
                    self._dao_pending = True                   # we are now waiting for a data block
                    return f"#SETDAO {task_no} #OK\n", ""
                elif tokens[2] == "DLEN":
                    self.logger.deepDebug(f"_simulate : SET DAO DLEN")
                    task_no = int(tokens[3])
                    dlen    = int(tokens[4])
                    return "#OK", ""
                elif tokens[2] == "FREQ":
                    task_no = int(tokens[3])
                    freq    = float(tokens[4])
                    return "#OK", ""
            elif tokens[1] == "NSU":
                if tokens[2] == "DEVS":
                    if len(tokens) < 6:
                        return "#NG", "syntax: SET NSU DEVS <unionNo> <nDevs> [<deviceId>, <deviceId>, ... <deviceId>]"
                    return f"#OK", ""
                if tokens[2] == "CHAN":
                    if len(tokens) < 6:
                        return "#NG", "syntax: SET NSU CHAN <unionId> <deviceId> [<range> <coupling>] [<range> <coupling>] ..."
                    return "#OK", ""
                if tokens[2] == "DLEN":
                    if len(tokens) != 5:
                        return "#NG", "syntax: SET NSU DLEN <unionId> <dlenValue>"
                    return "#OK", ""
                if tokens[2] == "FREQ":
                    if len(tokens) != 5:
                        return "#NG", "syntax: SET NSU FREQ <unionId> <freqValue>"
                    return "#OK", ""
            if tokens[1] == "PSA":
                #SET PSA unionNo [(SAO|DAO|SDO) device-idx channel-id] [start end steps] <skip-samples> — ‘#OK’ or ‘#NG !error\n’
                steps = int(tokens[8][:-1])
                start = float(tokens[6][1:])
                end = float(tokens[7])
                deviceId = int(tokens[4])
                channelId = int(tokens[5][:-1])
                # Recovering the sweeper parameter value:
                curParam     : CSVParameter = self.psa.GetCurPsaMode().GetCurParam()
                sweeperData  : SweepConf    = self.psa.GetCurPsaMode().GetSweepMap()[curParam.GetName()]
                
                self.logger.debug(f"parsed sweeper data : start={start}, stop={end}, steps={steps}")
                self.logger.debug("VS")
                self.logger.debug(f"sweeper data start : {sweeperData.GetStart()}, stop : {sweeperData.GetStop()}, steps :{sweeperData.GetSteps()}")
                device = curParam.GetChannel().GetDevice()

                # list (dynamic) vs simple value (static)
                if device.isDynamic():
                    dynamic = True
                else:
                    dynamic = False
                # And also the number of NISCOPE channels that are connected (for the plotting)
                # I understood that everh channel we see on the gui correspond to the number
                # of output you want to see...
                nNiscopeChannel = len(PSADataServices().GetActiveChannelsConfigurationList(self.psa.GetCurPsaMode()))

                self.logger.debug(f"Steps in the SET PSA cmd: {steps}")
                
                self._simData.SetPSA(steps, start, nNiscopeChannel, dynamic, start, end)
                return "#OK", ""

        # ────────────────────────────────────── RUN ──────────────────────────────────────


        if verb == "RUN":
            if tokens[1] == "DAO":
                return "#OK", ""
            if tokens[1] == "PSA":
                self._simData.RunPSA()
                return "#OK", ""
        

        # ────────────────────────────────────── STOP ──────────────────────────────────────


        if verb == "STOP":
            if tokens[1] == "DAO":
                return "#OK", ""
            if tokens[1] == "PSA":
                return "#OK", ""





        # ───────────────── DAO data block ─────────────────
        # in this mode no header are needed
        if self._dao_pending:                 # we are in “data mode”
            if not cmd.rstrip().endswith("#OK"):
                return "", "data block must terminate with #OK"
            self._dao_pending = False                      # back to idle state
            return "#OK\n", ""



        return "", f"unimplemented: {cmd}"
    





# ─────────────────────────────────────────────── Setters ────────────────────────────────────────────────────────


    def SettingPSA(self, newPsa : PSAData):
        self.psa = newPsa