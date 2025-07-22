#! usr/env/bin python3
# nevclient.utils.CSVWorker

# extern modules
import pandas as pd

# utils
from nevclient.utils.Logger import Logger
# sweep
from nevclient.model.config.PSA.SweepConf import SweepConf
# parameters
from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter


class CSVWorker():
    """
    CSV Worker class is used to manage a unique csv file of a specific type.

    The syntax that the csv file must implement is defined below:

    CSV ATTRIBUTE RULES  
    First line reserved for attribute definitions; place ‘#’ before the attribute name, e.g. *#ID*.  
    Supported attributes:  
    - ID (required): parameter ID number.  
    - COMMENT (optional): comment text.  
    - DEV (required): device name as registered in the PXI system; plan to allow $N to specify slot N (not yet supported).  
    - CH (required): channel type and number, e.g. AO-0 or DO-3.  
    - PIN (optional): LSI-chip pin number.  
    - LABEL (required): parameter name.  
    - NCMODE (required): null-cline-mode setting


    Attributes
    ----------
    df       : pd.DataFrame
        The pandas dataframe containing all the data from the csv file
    filePath : str
        The file path of the csv file to parse.
    mode     : 
    """

    _REQUIRED_ATTRIBUTES = {"#ID", "#DEV", "#CH", "#LABEL", "#NCMODE"}

    def __init__(self, filePath : str):
        self.logger   = Logger("CSVWorker")
        
        self.filePath = filePath


        df = pd.read_csv(filePath, dtype=str).fillna("nan")
        file_columns = set(df.columns)
        missing_columns = self._REQUIRED_ATTRIBUTES - file_columns
        if not self._REQUIRED_ATTRIBUTES.issubset(file_columns):
            raise ValueError(f"The CSV file is missing required columns: {', '.join(missing_columns)}")

        self.df = df
        self.logger.info(f"Succesfully read the csv file : \n{df}")


# ──────────────────────────────────────────────────────────── Public methods ──────────────────────────────────────────────────────────
    
    def GetSetupsList(self) -> list[str]:
        """
        Returns a list of the setups'names.

        Returns
        -------
        list[str]
        """
        return list([str(col) for col in self.df.columns if str(col)[0] != "#"])
    
    def GetParametersList(self) -> list[str]:
        """
        Returns a list of the parameters'names.

        Returns
        -------
        list[str]
        """
        return list(self.df["#LABEL"])
    
    def GetParametersChannelInfoMap(self) -> dict[str :str]:
        """
        Returns a map between parameters'name and their channel info.

        Returns
        -------
        dict[str : str]
        """
        paramNames   = self.GetParametersList()

        result = {}
        for i, paramName in enumerate(paramNames):
            channelInfo = self.df.at[i, "#CH"]
            result[paramName] = str(channelInfo)

        return result
    
    def GetParametersDeviceNameMap(self) -> dict[str :str]:
        """
        Returns a map between parameters'name and their binded device name.

        Returns
        -------
        dict[str : str]
        """
        paramNames   = self.GetParametersList()

        result = {}
        for i, paramName in enumerate(paramNames):
            devName = self.df.at[i, "#DEV"]
            result[paramName] = str(devName)

        return result

    def GetParametersModeMap(self, tag : str) -> dict[str :str]:
        """
        Returns a map between parameters'name and their binded mode string.

        Parameters
        ----------
        tag : str
            The tag of the mode, i.e. '#NCMODE'

        Returns
        -------
        dict[str : str]
        """
        paramNames   = self.GetParametersList()

        result = {}
        for i, paramName in enumerate(paramNames):
            ncMode = self.df.at[i, tag]
            if ncMode != "nan":
                result[paramName] = str(ncMode)

        return result
    
    def GetSetupsValues(self, parameterName: str) -> dict[str, float]:
        """
        Returns a map between setups'name and their corresponding value
        for a specific parameter's name.

        Parameters
        ----------
        parameterName : str
            The name of the parameter we want to recover the
            setups values map from.

        Returns
        -------
        dict[str, float]
            A dictionary mapping setup names to their float values.
        """
        # Find the row corresponding to the parameter name
        param_row = self.df[self.df['#LABEL'] == parameterName]

        # Check if the parameter was found
        if param_row.empty:
            self.logger.warning(f"Parameter '{parameterName}' not found in the CSV file.")
            return {}

        # Get the list of all setup columns
        setupsNames = self.GetSetupsList()
        
        result = {}
        # Extract the values for each setup from that specific row
        for setup_name in setupsNames:
            # Get the value as a string from the first (and only) row found
            value_str = param_row[setup_name].iloc[0]
        
            # Convert the value to float and store it
            result[setup_name] = float(value_str)
        
        return result



    def SaveToCSV(self, filePath : str, parametersData : ParametersData):
        """
        Saves the current state of parameters to a CSV file.

        This method constructs a pandas DataFrame from a map of CSVParameter
        objects and saves it to the specified file path. It preserves the
        structure required by the CSVWorker for reading, including all required
        and optional attributes.

        Parameters
        ----------
        filePath : str
            The path to the file where the CSV data will be saved.
        parametersData : parametersData
            The model runtime instance.
        """
        self.logger.debug("Entering the save method.")
        # Create a copy to avoid side effects if the save operation fails
        toSaveDf = self.df.copy()

        allSetupNames = self.GetSetupsList()
        # Iterate through the parameters in the model and update the DataFrame
        param : CSVParameter
        for name, param in parametersData.GetParametersMap().items():
            rowIndex = toSaveDf.index[toSaveDf['#LABEL'] == name]

            if rowIndex.empty:
                self.logger.warning(f"Parameter '{name}' not found in the original DataFrame. Skipping.")
                continue
        

            # 1. NOT UPDATING WITH THE DATA OF NC MODE !!

            # 2. Update the values for all relevant setup columns
            for setupName, value in param.GetSetupsValues().items():
                self.logger.debug(f"Inside the loop for recovering the data: rowIndex={rowIndex}, setupName={setupName}, value={value}.")
                toSaveDf.at[rowIndex.item(), setupName] = value

        # Save the updated DataFrame to the specified CSV file
        try:
            toSaveDf.to_csv(filePath, index=False)
            self.logger.info(f"Successfully saved parameters to '{filePath}' by updating the existing data.")
        except IOError as e:
            self.logger.error(f"Failed to save CSV file to '{filePath}'. An I/O error occurred: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while saving to '{filePath}': {e}")

    

    

        