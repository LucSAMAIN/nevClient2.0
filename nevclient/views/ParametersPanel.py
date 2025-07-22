#! usr/env/bin python3
# nevclient.views.ParametersPanel.py

# extern imports
import pandas as pd   # add this with the other imports
import wx
import wx.grid as gridlib

# model
from nevclient.views.templates.NevGrid import NevGrid
from nevclient.views.templates.NevPanel import NevPanel
from nevclient.views.templates.NevText import NevSimpleText
from nevclient.views.templates.NevComboBox import NevComboBox
from nevclient.views.templates.NevButton import NevButton

from nevclient.model.config.Parameters.ParametersData import ParametersData
from nevclient.model.config.Parameters.CSVParameter import CSVParameter




class ParametersPanel(NevPanel):
    """
    The ParametersPanel class is used to display csv parameters of a specific setup chosen by the user.
    It allows the user to select a setup from a list of checkboxes, view the parameters associated with that setup,
    and modify the values of those parameters. The changes can be saved to a CSV file.
    Plus it makes the link with the DAQMX tasks by using the paramBindings attribute,
    and methods to update the changes made on the GUI.

    Attributes
    ----------
    controller : Controller
        The instance of the controller class used in the main file to interact with the nevclient model.
    trueCheckbox : NevCheckBox
        The currently selected set up checkbox
    """
    def __init__(self, parent, 
                 controller, 
                 parametersData,
                 *args, 
                 **kwargs):
        super().__init__(parent, *args, **kwargs)
        

        # ATTR
        self.controller = controller # MAIN controller
        
        
        



        

        # WIDGETS
        # CHECKBOXES
        paramData : ParametersData = parametersData

        choices = paramData.GetSetupsList()
        self.setUpComboBox = NevComboBox(parent=self, choices=choices)
        self.setUpComboBox.Bind(event=wx.EVT_COMBOBOX, handler=self.OnChangingSetUp)
        currentSetup = paramData.GetCurSetup()
        self.setUpComboBox.SetSelection(choices.index(currentSetup))


        # SAVE BUTTON
        self.saveButton = NevButton(parent=self, label="Save changes")
        self.saveButton.Bind(wx.EVT_BUTTON, self.OnSaveButton)
        
        self.update = NevButton(parent=self, label="Update the backend server")
        self.update.Bind(wx.EVT_BUTTON, self.OnUpdate)
        
        # GRID
        paramNames = list(paramData.GetParametersMap().keys())
        self.grid = NevGrid(parent=self)
        self.grid.CreateGrid(len(paramNames), 4) # paramName, setUpName, + and -

        
        # Initialize of the grid
        self.InitFill(parametersData) # fill up the first column with parameter names
        self.FillGrid(parametersData) # fill the second column with the values of the parameter corresponding to the choosed setup

        

        # GRID INTERACTIONS
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellClick)
        self.grid.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChanged) 

        # SIZERS (version simplifiée et corrigée)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        labelSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondRowSizer = wx.BoxSizer(wx.HORIZONTAL)

        gridAndButtonSizer = wx.BoxSizer(wx.VERTICAL)



        # Upper part (label and checkboxes)
        labelSizer.Add(NevSimpleText(parent=self, label="Choose a set up"), flag=wx.ALL, border=5)
        firstRowSizer.Add(self.setUpComboBox, proportion=1, flag=wx.EXPAND)

        # Down part (grid and save button)
        gridAndButtonSizer.Add(self.grid, proportion=1,flag=wx.EXPAND|wx.ALL, border=5)
        gridAndButtonSizer.Add(self.saveButton, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        gridAndButtonSizer.Add(self.update, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        
        mainSizer.Add(labelSizer, proportion=0, flag=wx.EXPAND)
        mainSizer.Add(firstRowSizer, proportion=0, flag=wx.EXPAND)
        mainSizer.Add(secondRowSizer, proportion=0, flag=wx.EXPAND)
        mainSizer.Add(gridAndButtonSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)




        # END OF INIT
        self.ApplyTheme()
        self.grid.AutoSize()

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        

    
# ────────────────────────────────────────────────── Methods ─────────────────────────────────────────────────────       

    def InitFill(self, parametersData : ParametersData):
        """
        inputs : None
        outputs : None
        This method initializes the grid by filling the first column with parameter names and setting up the headers
        for the grid.
        """
        self.grid.SetColLabelValue(0, "Parameter name")
        self.grid.SetColLabelValue(2, "+")
        self.grid.SetColLabelValue(3, "-")
        paramData : ParametersData = parametersData
        paramNames = list(paramData.GetParametersMap().keys())
        for i, paramName in enumerate(paramNames):
            # Set the parameter name in the first column
            self.grid.SetCellValue(i, 0, paramName)
            # Fill up the + and -
            self.grid.SetCellValue(i, 2, "+")
            self.grid.SetCellValue(i, 3, "-")
            
            # So we can not edit the first column (parameter name) and the + and - columns
            self.grid.SetReadOnly(i, 0, True)
            self.grid.SetReadOnly(i, 2, True)
            self.grid.SetReadOnly(i, 3, True)
            
            # Center the text in the grid cells for the + and - columns
            self.grid.SetCellAlignment(i, 2, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            self.grid.SetCellAlignment(i, 3, wx.ALIGN_CENTER, wx.ALIGN_CENTER)

    def UpdateData(self, setUpName : str, paramName : str, newValueString : str):
        self.controller.UpdateAllCSVAndDAQMX(setUpName, paramName, newValueString)

    def GetSetupName(self):
        return self.trueCheckbox.GetLabel()

    def FillGrid(self, parametersData : ParametersData):
        """
        Fills the grid with the parameters for the   currently selected setup.

        Parameters
        ----------
        parametersData : ParametersData
            The parametersData instance.
        """
        man : ParametersData = parametersData
        setupName = man.GetCurSetup()
        self.grid.SetColLabelValue(1, setupName)

        paramMap : dict[str : CSVParameter] = man.GetParametersMap()
        for rowNum in range(self.grid.GetNumberRows()):
            paramName             = self.grid.GetCellValue(rowNum, 0)
            param : CSVParameter  = paramMap[paramName]
            value                 = param.GetSetupsValues()[setupName]

            # Update the view accordingly
            self.grid.SetCellValue(rowNum, 1, str(value))

        self.grid.AutoSize()
        self.grid.Refresh()
        self.grid.Layout()
        self.Refresh()
        self.Layout()


    def SetGridValue(self, row : int, col : int, value : str):
        self.grid.SetCellValue(row, col, value)
        
        self.grid.AutoSize()
        self.grid.Refresh()
        self.grid.Layout()
        self.Refresh()
        self.Layout()
    
    def GetGridValue(self, row : int, col : int) -> str:
        return self.grid.GetCellValue(row, col)


    def ApplyTheme(self):
        self.grid.HideRowLabels()
        super().ApplyTheme()

# ────────────────────────────────────────────────── Event  Handlers ───────────────────────────────────────────────────── 
   
    def OnChangingSetUp(self, event):
        comboBox  = event.GetEventObject()
        setUpName = comboBox.GetStringSelection()
        self.controller.OnParametersChangingSetUp(setUpName)

        event.Skip()

    def OnCellChanged(self, event):
        row, col = event.GetRow(), event.GetCol()
        self.controller.OnParametersCellChanged(row, col)
        

        # Refresh the grid to reflect the changes
        self.grid.Refresh()
        self.grid.Layout()
        self.Refresh()
        self.Update()
        self.Layout()


        event.Skip()



    def OnSaveButton(self, event):
        with wx.FileDialog(
            self,
            "Save CSV file",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dlg.GetPath()
            try:
                self.controller.OnParametersSave(pathname)
                wx.MessageBox(
                    f"Changes saved to {pathname}",
                    "Info",
                    wx.OK | wx.ICON_INFORMATION,
                )
            except Exception as e:
                wx.MessageBox(
                    f"Failed to save file: {str(e)}",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )

        self.Refresh()
        self.Update()
        self.Layout()
        event.Skip()



    def OnGridCellClick(self, event):
        """
        inputs (wx.Event) :  event
        outputs : None
        This method handles the click event on the grid cells for the "+" and "-" columns.
        It increments or decrements the value in the second column based on the clicked cell.
        It also ensures that the value remains within the precision of the original value.
        """
        row, col = event.GetRow(), event.GetCol()
        
        # Only works for the "+" and "-" columns (2 and 3)
        if col != 2 and col != 3:
            event.Skip()  # Let the event propagate if not in the "+" or "-" columns
            return
        
        paramName = self.grid.GetCellValue(row, 0)
        currentValueStr = self.grid.GetCellValue(row, 1)
        
        try:
            digitPrecision = self._count_decimal_places(currentValueStr)
            currentValue = float(currentValueStr) # now that we have the precision, we can convert it to float for the operation                

            if col == 2: # Clic on "+"
                newValue = currentValue + 10**-digitPrecision
                
            else: # Clic on  "-"
                newValue = currentValue - 10**-digitPrecision
            newValue = round(newValue, digitPrecision) # in case we do not break the ceiling of the digit precision
            
            # We need to ensure we stay within the digit precision
            if len(str(newValue).split('.')[1]) > digitPrecision:
                newValueString = str(newValue)[:len(str(newValue).split('.')[0]) + digitPrecision + 1] # shrink it
            elif len(str(newValue).split('.')[1]) < digitPrecision:
                newValueString = str(newValue) + '0' * (digitPrecision - len(str(newValue).split('.')[1])) # add zeros
            else:
                newValueString = str(newValue)


            # Update the grid cell with the new value
            self.grid.SetCellValue(row, 1, newValueString)
            
            
            # Update the data:
            self.controller.UpdateCSVDAQMXAndViewParam(paramLabel=paramName, value=newValueString)
                    
        except ValueError:
            # Handle the case where the current value is not a valid number
            wx.MessageBox(f"The current value '{currentValueStr}' for '{paramName}' is not a valid number.", 
                            "Conversion error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Unknown error : {str(e)}", 
                            "Error", wx.OK | wx.ICON_ERROR)
        
        # Refresh the grid to reflect the changes
        self.grid.Refresh()
        self.grid.Layout()
        self.Refresh()
        self.Update()
        self.Layout()

    def OnUpdate(self, e :wx.Event):
        self.controller.SendDAQMXUpdatesToBackEndServer()

        





    # ────────────────────────────────────────────────── UTILS METHODS ───────────────────────────────────────────────────── 

    def _count_decimal_places(self, stringNumber):
        """
        inputs (str) : stringNumber
        outputs (int) : number of decimal places
        This method counts the number of decimal places in a number.
        """
        if '.' in stringNumber:
            return len(stringNumber.split('.')[-1])
        return 0

    # ────────────────────────────────────────────────── OTHER METHODS ───────────────────────────────────────────────────── 
    
    


    # ────────────────────────────────────────────────── GETTERs ─────────────────────────────────────────────────────  
    def GetSetUpName(self):
        return self.trueCheckbox.GetLabel()  
    