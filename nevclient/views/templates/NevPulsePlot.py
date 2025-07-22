import wx.lib.plot as plot
import numpy as np

class NevPulsePlot(plot.plotcanvas.PlotCanvas):
    """
    The NevPulsePlot is a class used to heelp visualizing the pulse impulsion.

    Attributes
    ----------
    nbPulses : int
        The number of impulsions to set.
    delays : list
        The delay parameter for each impulsion.
    widths : list
        The width parameter for each impulsion.
    amps : list
        The amp of every impulsion.
    colors : list
        The color to plot for every impulsion vizualisation.
    title : str
        The title of the plot... (really optionnal)
    """
    def __init__(self,
                 nbPulses = 0, 
                 delays = [], # ms 
                 widths = [],  # ms,
                 amps = [], # mV,
                 colors = [], 
                 title="Pulse imp vizualisation", 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)


        if len(widths) != len(delays) != len(amps) != len(colors) != nbPulses:
            raise Exception("ERROR : Not same length for every parameters passed")
        

        
        self.nbPulses = nbPulses
        self.delays = delays
        self.widths = widths
        self.amps = amps
        self.xAxisName = "Time (ms)"
        self.yAxisName = "Amplitude (mv)"
        self.title = title
        self.colors = colors
        
        
        self.PlotData()

        
    

    def PlotData(self):
        if not self.nbPulses:
            xmax = 20
            ymax =  200
            resolution = 1000
            x = np.linspace(-1, xmax, resolution)
            y = np.zeros((resolution,))
            y[0:100] = ymax

            # invisible line
            dummy = plot.PolyLine(
                list(zip(x, y)),
                colour=self.GetBackgroundColour(), 
                width=0
            )

            g = plot.PlotGraphics(
                [dummy],                      
                self.title,                   
                self.xAxisName,               
                self.yAxisName              
            )
            self.Draw(g)
            return




        maxXValue = (max(self.delays)+max(self.widths))+10
        maxYValue = max(self.amps) + 10


        resolution = 1000
        x = np.linspace(0, maxXValue, resolution)
        ys = [np.zeros((resolution,)) for _ in range(self.nbPulses)]
        
        # Create the pulse signal
        for i in range(self.nbPulses):
            start_idx = int((self.delays[i]/maxXValue) * resolution)
            end_idx = int(((self.delays[i] + self.widths[i])/maxXValue) * resolution)

            ys[i][start_idx:end_idx] = self.amps[i]

        # Create plot graphics
        line_plots = [plot.PolyLine(list(zip(x, ys[i])), colour=self.colors[i], legend=f"Pulse {i+1}") for i in range(self.nbPulses)]
        graphics = plot.PlotGraphics(line_plots, self.title, self.xAxisName, self.yAxisName)

        # Draw the plot
        self.enableLegend = True
        self.Draw(graphics, xAxis=(-maxXValue*0.2, maxXValue), yAxis=(-maxYValue*0.2, maxYValue))
        

    def UpdateData(self, nbPulses, delays, widths, amps, colors):
        self.nbPulses = nbPulses
        self.delays = delays
        self.widths = widths
        self.amps = amps
        self.colors = colors

        self.PlotData()


    def ApplyTheme(self):
        pass