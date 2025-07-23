#! usr/env/bin python3
# nevclient.services.Parsing.PSAParsing

# extern modules
import re
# psa
from nevclient.model.Enums.PSAStatus import PSAStatus
from nevclient.model.config.PSA.PSAData import PSAData
# services
from nevclient.services.DataManipulation.PSADataServices import PSADataServices
# logger
from nevclient.utils.Logger import Logger

class PSAParsing():
    """
    Set of useful methods helping parsing server's answer about the PSA processes.

    Public methods
    --------------
    ParsingPSAStat(self, body : str) -> tuple[int, float, PSAStatus]
    ParsingPSAData(self, body : str, psa : PSAData, psaDmServ : PSADataServices) -> tuple[int, int, list, dict]
    """
    def __init__(self):
        self.logger = Logger("PSAParsing")


    def ParsingPSAStat(self, body : str) -> tuple[int, float, PSAStatus]:
        """
        The _ParsingPSAStat method a helper function used in the RunPSA method to
        parse the stat data recovered from the backend server.

        Parameters
        ----------
        body : str
            The full response string from the backend server.
            e.g., "#PSASTAT\\n10 1.25 RUNNING\\n"
        
        Returns
        -------
        tuple[int, float, PSAStatus]:
            The data parsed from the body string.
        """
        # Regex to capture the required fields:
        # - (\d+): An integer for the points
        # - ([-\d.eE]+): A float for the parameter value
        # - (\w+): A word for the status (RUNNING, FAILED, etc.)
        # The pattern ignores the header and handles whitespaces, including newlines.
        pattern = re.compile(r"#PSASTAT\s+(\d+)\s+([-\d.eE]+)\s+(\w+)#OK")
        
        match = pattern.search(body)
        
        if not match:
            self.logger.error(f"Failed to parse PSA STAT with regex. Body: '{body}'")
            return None
            
        try:
            # The groups are the parts of the string captured by parentheses ()
            stage = int(match.group(1))
            lastSValue = float(match.group(2))
            status = PSAStatus.from_string(match.group(3))
            # The C code might add an error message after 'FAILED'. 
            # The regex above correctly ignores it, but you get the 'FAILED' status.
            return stage, lastSValue, status

        except (ValueError, IndexError) as e:
            self.logger.error(f"Error converting parsed PSA data: {e}, Match groups: {match.groups()}")
            return None
        
    def ParsingPSAData(self, body : str, psa : PSAData, psaDmServ : PSADataServices) -> tuple[int, int, list, dict]:
        """
        Parses the multi-line data stream from a 'GET PSA DATA' command.

        This function reads from a stream-like object (e.g., a socket file
        descriptor) line by line, interpreting the structured data until it
        receives a termination signal.

        Parameters
        ----------
        body : str
            The raw string answer from the backend server after
            sending the GET PSA DATA request.
        psa  : PSAData
            The PSA runtime instance.
        psaDmServ : PSADataServices
        
        Returns
        -------
        tuple[int, int, list, dict]:
            Corresponding to the following data: start, end, XSweeper, Y
        """
        self.logger.debug(f"Entering the ParsingPSAData method with body:\n{body}")
        # 0. Recover useful data:
        nChannels = len(psaDmServ.GetActiveChannelsConfigurationList(psa.GetCurPsaMode()))

        # 1. Validate and strip the header.
        header_pattern = re.compile(r"^#PSADATA\s+(\d+)\s+\d+\n")
        match = header_pattern.match(body)
        if not match:
            self.logger.error(f"Error: Invalid or missing header in response:\n{body}")
            return None
        # Recovering the start value
        start = int(match.group(1))
        # Remove the header to isolate the data payload
        payload_string = header_pattern.sub("", body, count=1)

        # 2. Define the regex to find one complete data block.
        # A block is a float parameter, followed by one or more lines
        # that are lists enclosed in square brackets.
        block_pattern = re.compile(
            r"(?P<param>[-+]?\d*\.\d+|\d+)\n"  # Group 'param': Captures the float parameter line
            r"(?P<data>(?:\[.*?\]\s*)+)"   # Group 'data': Captures all subsequent data lines
        )

        dataByStep = []
        # 3. Find all data blocks in the payload string.
        for i, match in enumerate(block_pattern.finditer(payload_string)):
            try:
                # Extract the named groups from the match
                paramString = match.group("param")
                dataString = match.group("data")

                channel_lines = dataString.strip().split('\n')

                stepData_raw = []
                for i, line in enumerate(channel_lines):
                    line = line.strip()
                    if not line:
                        continue
                    # Remove brackets and split numbers
                    numbers_str = line.strip('[]').split()
                    channel_values = [float(val) for val in numbers_str]
                    stepData_raw.append(channel_values)
                
                # Append the structured data for this step
                """
                list[[int, float, list[list[float]]]]
                    A list of list of which the first item is the step number
                    then the sweeper parameter value for this stage and
                    then the actual data for every channel
                """
                if len(stepData_raw) != nChannels:
                    self.logger.error(f"Number of parsed channels data : {len(stepData_raw)} is different from active channels : {nChannels}")
                    return None
                data = [start+i, float(paramString), stepData_raw]
                dataByStep.append(data)

            except (ValueError, IndexError) as e:
                self.logger.error(f"! Error parsing data block: {e}")
                return None
            
        # Update the end parameter:
        end =  start + i
        # Updating the data attributes:
        XSweeper = []
        Y = {}
        for _, sweepValue, data in dataByStep:
            XSweeper.append(sweepValue)
            for i, conf in enumerate(psaDmServ.GetActiveChannelsConfigurationList(psa.GetCurPsaMode())):
                deviceId = conf.GetNiscopeChn().GetDevice().GetId()
                channelId = conf.GetNiscopeChn().GetIndex()
                val = Y.get((deviceId, channelId), [])
                val.append(data[i])
                Y[(deviceId, channelId)] = val
            
        return start, end, XSweeper, Y