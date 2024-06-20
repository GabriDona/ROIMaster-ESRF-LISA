ROI Master: Streamlining XAFS
================================


Overview
--------
This project, "ROI Master," is a graphical user interface (GUI) application designed to facilitate the analysis of X-ray Absorption Fine Structure (XAFS) data. It allows users to open NX5 files (saved with [DataNexusConverter](https://github.com/GabriDona/DataNexusConverter-ESRF-LISA)), visualize fluorescence data, apply deadtime corrections, and save processed data in XDI format. The application is built using Python, Tkinter for the GUI, and Matplotlib for plotting.

Features
--------
- Open NX5 Files: Load NX5 files containing XAFS data.
- Plot Fluorescence Data: Visualize fluorescence spectra and XAFS data.
- Energy Slider: Select and display specific energy values.
- XIA Channel Selection: Choose XIA channels for analysis.
- Dead Time Correction (DTC): Apply DTC to the data.
- Save Data: Save the processed data in XDI format.

Usage
-----
Make sure that the Nexus file you are about to analyze has been created through the DataNexusConverter application.
You can download the code at [link](https://github.com/GabriDona/DataNexusConverter-ESRF-LISA/blob/main/LICENSE)
1. **Open File**: Click on the 'Open File' button to load an NX5 file.
2. **Select XIA Channels**: Choose XIA channels from the treeview for analysis (you can also choose more than one channel).
3. **Adjust Energy**: Use the energy slider to select a specific energy value.
4. **Plot Fluorescence Data**: The fluorescence data will be plotted automatically based on the selected XIA channels and energy value. 
5. **Plot EXAFS signal**: The EXAFS signal will be plotted automatically within a default domain, but it is allowed to change with your cursor the range
6. **Apply Dead Time Correction**: Use the DTC switch to apply or remove dead time correction.
7. **Save Data**: Click the 'Save' button to save the processed data in XDI format.
8. **Quit**: Click the 'Quit' button to close the application.

Dependencies
------------
- Python 3.x
- Tkinter
- Matplotlib (3.3.4 or above)
- h5py (3.1.0 or above)
- numpy (1.19.5 or above)
- pandas (1.2.1 or above)
- customtkinter (4.6.3 or above)
- PIL (Python Imaging Library) (8.1.0 or above)

Files
-----
- main.py: The main application script.
- title_roimaster.png: The title image displayed in the application.

Contact
-------
For any inquiries or issues, please contact the project maintainer at gabriele.donati11@studio.unibo.it.

## Author

- Gabriele Donati

