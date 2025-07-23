import wx.lib.plot as plot
import numpy as np


class NevPSAPlot(plot.plotcanvas.PlotCanvas):
    """
    The NevPSAPlot is a class used to display the PSA plotting data in the PSAPanel

    Attributes
    ----------
    XAxisName : str
    YAxisName : str
        The names of the axes
    X : list[float]
        The parameter sweeper value or other input
    as selected in the combo box for the X axis.
    Y : list[list[float]]
        Of shape (nbSteps, nbInputs)
    title : str
        The title of the plot
    colors : list[str]
        The list of string colors in which to plot
        every data of shape (nbInputs,)
    legends : list[str]
        Same idea but for legends.
    
    
    """
    def __init__(self, 
                 XAxisName,
                 YAxisName,
                 title,
                 colors,
                 legends,
                 X,
                 Y,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.XAxisName    = XAxisName
        self.YAxisName    = YAxisName
        self.title        = title
        self.colors       = colors
        self.legends      = legends
        self.X            = X
        self.Y            = Y
        
        self.PlotData(self.X, self.Y)

    def _plotDummy(self):
        xmax = 20
        ymax = 20
        resolution = 1000
        x = np.linspace(-1, xmax, resolution)
        y = np.zeros((resolution,))
        y[0:100] = ymax
        dummy = plot.PolyLine(
            list(zip(x, y)),
            colour=self.GetBackgroundColour(), 
            width=0
        )
        g = plot.PlotGraphics(
            [dummy],
            self.title,
            self.XAxisName,
            self.YAxisName
        )
        self.Draw(g)


    def PlotData(self, X, Y):
        # Dummy mode
        if not Y or not X:
            self._plotDummy()
            return
        
        colors = self.colors
        legends = self.legends
        nbInputs = len(Y)

        
        # --- Plot creation
        line_plots = [
            plot.PolyLine(
                list(zip(X, Y[i])), 
                colour=colors[i], 
                legend=legends[i] 
            ) 
            for i in range(nbInputs)
        ]
        graphics = plot.PlotGraphics(line_plots, self.title, self.XAxisName, self.YAxisName)

        # --- Min/Max computations (pure gui purpose)
        if X and Y:
            # So to find min/max global
            all_y_values = [val for y_list in Y for val in y_list]
            global_min_y = min(all_y_values)
            global_max_y = max(all_y_values)
            
            min_x = min(X)
            max_x = max(X)

            # 10 % of margin
            plotMinX = min_x * 1.1 if min_x < 0 else min_x * 0.9
            plotMaxX = max_x * 1.1 if max_x > 0 else max_x * 0.9
            
            plotMinY = global_min_y * 1.1 if global_min_y < 0 else global_min_y * 0.9
            plotMaxY = global_max_y * 1.1 if global_max_y > 0 else global_max_y * 0.9
            
            # Edge case
            if plotMinX == 0 and plotMaxX == 0: plotMaxX = 1
            if plotMinY == 0 and plotMaxY == 0: plotMaxY = 1

        else: # To be really sure
            plotMinX, plotMaxX, plotMinY, plotMaxY = (0, 1, 0, 1)


        # Finally drawing
        self.enableLegend = True
        self.Draw(graphics, xAxis=(plotMinX, plotMaxX), yAxis=(plotMinY, plotMaxY))
    
    def UpdateData(self, X : list[float], Y : list[list[float]], XAxisName : str, colors : list[str], legends : list[str]):
        self.X         = X
        self.Y         = Y
        self.XAxisName = XAxisName
        self.colors    = colors
        self.legends   = legends

    def UpdatePlot(self):
        self.PlotData(self.X, self.Y)
        self.Refresh()
        self.Update()

# ───────────────────────────────────────────────────────── GETTERs ──────────────────────────────────────────────────────────────

    def GetXAxisName(self) -> str:
        return self.XAxisName
    
# ───────────────────────────────────────────────────────── SETTERs ──────────────────────────────────────────────────────────────
    
    def SetXAxisName(self, newName : str):
        self.XAxisName = newName
    def SetX(self, newX : list[float]):
        self.X = newX
    def SetY(self, newY : list[list[float]]):
        self.Y = newY
    def SetLegends(self, newLegends : list[str]):
        self.legends = newLegends
    def SetColors(self, newColors   : list[str]):
        self.colors = newColors
    
# ───────────────────────────────────────────────────────── OTHERs ──────────────────────────────────────────────────────────────
    
    def ApplyTheme(self):
        pass