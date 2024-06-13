ROI Master: Streamlining XAFS
================================


Overview
--------
This project, "ROI Master," is a graphical user interface (GUI) application designed to facilitate the analysis of X-ray Absorption Fine Structure (XAFS) data. It allows users to open NX5 files, visualize fluorescence data, apply deadtime corrections, and save processed data in XDI format. The application is built using Python, Tkinter for the GUI, and Matplotlib for plotting.

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
- Matplotlib
- h5py
- numpy
- pandas
- customtkinter
- PIL (Python Imaging Library)

Installation
------------
1. Install the required Python packages using pip:
 - pip install tk
 - pip install numpy
 - pip install --upgrade --user pyglet
 - pip install pillow
 - pip3 install customtkinter
 - pip install h5py


Files
-----
- main.py: The main application script.
- IMG-LOGO.ico: The icon file for the application.
- title_roimaster.png: The title image displayed in the application.

Contact
-------
For any inquiries or issues, please contact the project maintainer at gabriele.donati11@studio.unibo.it.

## Author

- Gabriele Donati

