from tkinter import *
from tkinter import ttk
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import h5py
import ast
import numpy as np
import re
from matplotlib.figure import Figure
import pandas as pd
import customtkinter
from PIL import Image, ImageTk
import os
import numpy as np

# Initialize global variables
global xmin
xmin = 1100 
global xmax 
xmax = 1300
global xia
global SelEnergy
SelEnergy = 0
global i0
global pintegral_array

def CreateNewPlot(figure, xlabel, ylabel):
	"""Creates an empty axis"""
	ax = figure.add_subplot()
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	figure.tight_layout()
	return ax


class DataFluo:
    def __init__(self, energy,channels,i0eh2, i0eh1, name, metadata, ixeh2, i1eh2):
        self.energy = energy
        self.name = name
        self.ixeh2 = ixeh2
        self.i1eh2 = i1eh2
        self.channels = channels
        self.i0eh2 = i0eh2
        self.i0eh1 = i0eh1
        self.spectra={}
        self.correction={}
        self.xias=[]
        self.metadata= metadata
    def add_xia(self,spectra_data,correction_data,xia_number):
        self.spectra[xia_number]=spectra_data
        self.correction[xia_number]=correction_data
        self.xias += [xia_number]
    
        
        
def get_groups_XIA(file):
    """Extract groups matching the pattern 'Fluo_' followed by a number"""
    entry_group = file.get('Entry', {})
    pattern = re.compile(r'Fluo_(?:[0-9]|[0-9][0-9])$')
    return [name for name in entry_group.keys() if pattern.match(name)]




def clear_interface():
    """Clear the interface elements"""
    root.XiaTab.delete(*root.XiaTab.get_children())
    root.energySlider.set(0)
    root.energyCorrected.set("n.a")
    root.figuresCanvas.axesplot.clear()
    root.figuresCanvas.axesxas.clear()
    root.figuresCanvas.plotcanvas.draw()
    root.figuresCanvas.xascanvas.draw()
    global SelXia
    SelXia = []
    global SelEnergy
    SelEnergy = 0



def open_file():
    """Open and process the selected file"""
    clear_interface()
    file = filedialog.askopenfilenames(filetypes=[("NX5 files", "*.nx5")]) 
    file_path_tuple = ast.literal_eval(str(file))
    file_path = file_path_tuple[0]
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    meta_data = {}
    global SelEnergy

    with h5py.File(file_path, 'r') as file:
        global data
        groupC = file['Entry/Instrument/Monochromator']
        groupT = file['Entry']
        crystall = groupC.attrs['miller']
        time = groupT.attrs['time']
        meta_data['Crystal'] = crystall
        meta_data['Time'] = time
        names = [name for name in get_groups_XIA(file)]
        xianumbers = [re.findall(r'\d+', name)[0] for name in names]
        
        energy= np.array(file['Entry/Instrument/Monochromator/energy_corretta']) #lista delle energie
        channels = np.array(file['Entry/Instrument/Fluorescence/channels'])
        i0eh2 = np.array(file['Entry/I0 EH2/counts'][:])
        i0eh1 = np.array(file['Entry/I0 EH1/counts'][:])
        ixeh2 = np.array(file['Entry/Instrument/IX_Eh2/riferimento'])
        i1eh1 = np.array(file['Entry/I1 EH2/counts'][:])
        data = DataFluo(energy, channels, i0eh2, i0eh1, file_name,meta_data,ixeh2,i1eh1)
        for xian in xianumbers:
            xia = np.array(file[f'Entry/Fluo_{xian}/counts'])
            ocr = file[f'Entry/Instrument/Fluorescence/Fluo_{xian}/ocr'][:]
            icr = file[f'Entry/Instrument/Fluorescence/Fluo_{xian}/icr'][:]
            corr = icr/ocr
            data.add_xia(xia,corr,int(xian))
            root.XiaTab.insert("", 'end', text=int(xian), iid=int(xian))
    root.energySlider.configure(to=len(energy)-1)
    xmax = len(channels) -1
    root.energyCorrected.set(str(np.round(data.energy[0],2)))
    
    


def plot_fluo():
    """Plot fluorescence data"""
    root.figuresCanvas.axesplot.clear()
    global SelXia
    global data
    global SelEnergy
    for xia in SelXia:
        plotdata = data.spectra[int(xia)][SelEnergy]
        x_data=data.channels
        root.figuresCanvas.axesplot.plot(x_data, plotdata, label=xia, markersize=0, linewidth=0.5)
        
    root.figuresCanvas.axesplot.set_xlabel('Channels')
    root.figuresCanvas.axesplot.set_ylabel('Counts') 
    root.figuresCanvas.axesplot.legend()  
    root.figuresCanvas.plotcanvas.draw()
    
    
 
def plot_xafs():
    """Plot XAFS data"""
    root.figuresCanvas.axesxas.clear()
    global SelXia
    global data
    global xmin
    global xmax
    global i0
    global pintegral_array
    if root.I0.get() == 1:
        i0 = data.i0eh2
    else:
        i0 = data.i0eh1
    if len(SelXia) == 1:
        
        if root.DTcorr.get()==1:
            cor = data.correction[SelXia[0]] 
            pintegral_array = np.sum(data.spectra[SelXia[0]][:, int(xmin):int(xmax)], axis=1)/i0*cor
        else:
            pintegral_array = np.sum(data.spectra[SelXia[0]][:, int(xmin):int(xmax)], axis=1)/i0
        
    elif len(SelXia) > 1:
        cor = data.correction[SelXia[0]] 
        pintegral_array = np.sum(data.spectra[SelXia[0]][:, int(xmin):int(xmax)], axis=1)/i0*cor
        for xia in SelXia[1:]:
            if root.DTcorr.get()==1:
                cor = data.correction[xia] 
                pintegral_array += np.sum(data.spectra[xia][:, int(xmin):int(xmax)], axis=1)/i0*cor
            else:
                pintegral_array += np.sum(data.spectra[xia][:, int(xmin):int(xmax)], axis=1)/i0*cor
                
    df = pd.DataFrame(pintegral_array)
    x_data = data.energy[df.index]
    y_data = df.iloc[:,0]
    root.figuresCanvas.axesxas.plot(x_data, y_data, markersize=0, linewidth=0.5) 
    root.figuresCanvas.axesxas.set_xlabel('Energy(eV)')
    root.figuresCanvas.axesxas.set_ylabel('μx') 
    root.figuresCanvas.xascanvas.draw()
    
     
     
def dead_time_correction():
    """Apply dead time correction and refresh plots"""
    plot_xafs()   
          
        
def RefreshPlots():
    """Refresh plots based on current selections"""
    global xmin
    global xmax
    global SelXia

    plot_xafs()
    plot_fluo()
  
        
def onselect(dmin, dmax):
    """Update the selected range and refresh plots"""
    global xmin
    global xmax
    xmin = int(np.floor(dmin))
    xmax = int(np.ceil(dmax))
    RefreshPlots()


def XiaClicked(a):
    """Handle the selection of XIA channels"""
    global SelXia
    if len(list(root.XiaTab.selection())) != 0:
        SelXia = list(root.XiaTab.selection())
        SelXia = [int(i) for i in SelXia]
        plot_fluo()
        plot_xafs()
    
     
     
def update_energy(value):
    """Update the energy value and refresh fluorescence plot"""
    global data
    global SelEnergy
    global SelXia
    SelEnergy = int(value)
    root.energyCorrected.set(str(np.round(data.energy[SelEnergy],2)))
    plot_fluo()
    
    
def save():
    """Save the data to a file"""
    global data
    global i0
    global xmin
    global xmax
    global pintegral_array
    
    # Convert pintegral_array to DataFrame
    df = pd.DataFrame(pintegral_array)
    
    # Create the column headers
    column = '#energy eV I0 Fluo I1 IR\n'
    
    # Initialize the data list
    data_list = []
    
    # Append energy values rounded to 2 decimal places
    data_list.append(round(i, 2) for i in data.energy)
    
    # Append i0 values
    data_list.append(i0)
    
    # Append pintegral values
    data_list.append(df.iloc[:, 0])
    
    # Append i1eh2 values
    data_list.append(data.i1eh2)
    
    # Append ixeh2 values
    data_list.append(data.ixeh2)
    
    # Determine i0 source based on checkbox selection
    i0 = ""
    if root.I0.get() == 1:
        i0 = "eh2"
    else:
        i0 = "eh1"
        
    # Open a new file with .xdi extension and write metadata and data
    with open(data.name + '.xdi', 'w') as xdifile:
        xdifile.write('# XDI/1.0 GSE/1.0\n')
        xdifile.write('# Scan-start_time: %s\n' % (data.metadata['Time']))
        xdifile.write('# Column.1: energy (eV)\n')
        
        # Write column headers
        for i, col in enumerate(column.split()[2:]):
            xdifile.write('# Column.%d: %s\n' % (i + 2, col))
        
        # Write metadata
        xdifile.write('# Mono.name: Si %s\n' % (data.metadata['Crystal']))
        xdifile.write('# Mono.d_spacing: 3.134692\n')
        xdifile.write('# Mono.notes: LNT cooled\n')
        xdifile.write('# Beamline.name: BM08-LISA\n')
        xdifile.write('# Facility.name: ESRF\n')
        xdifile.write('# Facility.xray_source: Bending magnet\n')
        xdifile.write('# DTC: %s\n' % root.DTcorr.get())
        xdifile.write('# Norm: %s\n' % i0)
        xdifile.write('#Xmin: %s\n' % xmin)
        xdifile.write('#Xmax: %s\n' % xmax)
        
        # Write column headers again
        xdifile.write(column)
        
        # Write the data rows
        for row in zip(*data_list):
            line = " ".join(map(str, row)) + "\n"
            xdifile.write(line)
    return

class FigureFrame(Frame):
    def __init__(self, parent):
        # Create a canvas for the figures
        self.figuresCanvas = Frame(parent, width=600, height=800, borderwidth=0, bg='white')
        self.figuresCanvas.pack(fill='y', side='left')
        
        # Create a frame for the XAS plot
        self.xasFrame = Frame(self.figuresCanvas, width=600, height=400)
        self.xasFrame.pack(side='top', expand=1)
        
        # Create the XAS figure and canvas
        self.figurexas = Figure(figsize=(6, 3), dpi=100)
        self.xascanvas = FigureCanvasTkAgg(self.figurexas, self.xasFrame)
        self.xascanvas.get_tk_widget().pack(side="top", fill='both', expand=True)
        
        # Create the XAS axis
        self.axesxas = CreateNewPlot(self.figurexas, 'Channel', 'Intensity')
        
        # Create a frame for the plot
        self.plotFrame = Frame(self.figuresCanvas, width=600, height=400, bg='black')
        self.plotFrame.pack(side='top', expand=1)
        
        # Create the plot figure and canvas
        self.figureplot = Figure(figsize=(6, 3), dpi=100)
        self.plotcanvas = FigureCanvasTkAgg(self.figureplot, self.plotFrame)
        self.plotcanvas.get_tk_widget().pack(expand=1)
        
        # Create the plot axis
        self.axesplot = CreateNewPlot(self.figureplot, 'Channel', 'Intensity')

class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize variables
        self.energyCorrected = StringVar()
        self.energyCorrected.set("n.a")
        self.DTcorr = BooleanVar()
        self.DTcorr.set(1)
        self.I0 = BooleanVar()
        self.I0.set(1)
        
        # Set window title and icon
        self.title("ROI Master: Streamlining XAFS")
        
        
        # Set window style and size
        self.style = ttk.Style(self)
        self.config(width=1026, height=850, bg='white')
        self.resizable(False, False)
        
        # Create the lateral bar
        self.LateralBar = Frame(self, bg="white")
        self.LateralBar.pack(side='left', fill='y')
        
        # Create the title frame
        self.Title = Frame(self.LateralBar, bg='white')
        self.Title.pack(side='top', fill='x')
        
        # Load and display the title image
        self.image = Image.open('programXas\\title_roimaster.png')
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.TitleTxt = Label(self.Title, image=self.tk_image, bg="white")
        self.TitleTxt.pack()
        
        # Create the top buttons frame
        self.TopButtons = Frame(self.LateralBar, bg='white')
        self.TopButtons.pack(side='top', fill='x', pady=(20, 0))
        
        # Create the "Open File" button
        self.OpenButton = Button(self.TopButtons, text='Open File', command=open_file, width=15)
        self.OpenButton.pack(side='left', padx=(10, 10))
        
        # Create the DTC switch
        self.switch_1 = customtkinter.CTkSwitch(master=self.TopButtons, text="DTC", variable=self.DTcorr, onvalue=True, offvalue=False, command=dead_time_correction)
        self.switch_1.pack(pady=(10, 10), padx=(10, 10), side='right', fill='x')
        
        # Create the I0 switch
        self.switch_norm = customtkinter.CTkSwitch(master=self.TopButtons, text="eh1/eh2", variable=self.I0, onvalue=True, offvalue=False, command=dead_time_correction)
        self.switch_norm.pack(pady=(10, 10), padx=(10, 0), side='right', fill='x')
        
        # Create the data frame
        self.DataFrame = Frame(self.LateralBar, width=300, height=600, bg='white')
        self.DataFrame.pack(expand=True, fill='x', pady=(0, 10))
        
        # Create the XIA treeview
        self.XiaTab = ttk.Treeview(self.DataFrame, height=10)
        self.XiaTab.column('#0', width=500, stretch=False)
        self.XiaTab.heading('#0', text='Xia', anchor='center')
        self.XiaTab.pack(expand=False, fill='none', padx=(0, 10))
        self.XiaTab.bind('<ButtonRelease-1>', XiaClicked)
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Create the energy frame
        self.FrameEnergy = Frame(self.LateralBar, width=500, height=100)
        self.FrameEnergy.pack(fill="x", padx=10, pady=10)
        
        # Create the energy slider
        self.energySlider = Scale(self.FrameEnergy, from_=0, to=100, orient=HORIZONTAL, command=update_energy, showvalue=0)
        self.energySlider.pack(side='bottom', fill='x')
        
        # Create the energy label
        self.Energy = Label(self.FrameEnergy, text="Energy(eV)   = ")
        self.Energy.pack(side='left', padx=(70, 0))
        
        # Create the energy value label
        self.labelEnergy = Label(self.FrameEnergy, textvariable=self.energyCorrected)
        self.labelEnergy.pack(side='left')
        
        # Create the "Save" button
        self.SaveMap = Button(self.LateralBar, text='Save', width=15, command=save)
        self.SaveMap.pack(pady=(10, 10), padx=(10, 10), side='left', fill='x')
        
        # Create the "Quit" button
        self.CloseButton = Button(self.LateralBar, text='Quit', command=quit, width=15)
        self.CloseButton.pack(side='right', padx=(10, 10))
        
        # Create the default fluo plot
        self.figuresCanvas = FigureFrame(self)
        
        # Create the SpanSelector for selecting the range
        self.xrfspan = SpanSelector(self.figuresCanvas.axesplot, onselect, "horizontal", useblit=True, props=dict(alpha=0.5, facecolor="tab:blue"), interactive=True, drag_from_anywhere=True, snap_values=None)
        self.figuresCanvas.plotcanvas.mpl_connect('key_press_event', self.xrfspan)
        self.figuresCanvas.figureplot.tight_layout()

root = MainWindow()

root.mainloop()
