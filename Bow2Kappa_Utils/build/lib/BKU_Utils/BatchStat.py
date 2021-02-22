''' Definition of useful functions for statistical analysis
 - Kappa_data
 - Kappa_flatten
 - Kappa_hist
 - Kappa_bbox'''
 
__all__ = [
    "Kappa_data",
    "Kappa_flatten",
    "Kappa_hist",
    "Kappa_bbox",
]

def Kappa_data(dk, val_min, val_max, sensors_nbr):

    '''
    Version 2021.02.13
    Define a dictionary containing the cutting efficiency data calculated from the bow in-situ measurements
    by bow2kappa function on a specific cut-progress range

    Inputs
    - data_file: name of the results file (output of bow2kappa function)
    - val_min, val_max : minimum and maximum values of the cut-progress range
      used for data selection
    - sensors_nbr: number of sensors used for the bow in-situ measurements (parameter of the cut)

    Outputs
    - Dictionary dkappa for plot and statistical analysis
    '''

    # Standard library imports
    import copy

    # Select cut-progress range
    dk.rename({"Cut progress (%)":"A"}, axis=1, inplace=True)
    dk_part = dk.query('A > @val_min and A < @val_max')
    dkappa = copy.deepcopy(dk_part)
    dkappa.rename({"A":"Cut progress (%)"}, axis=1, inplace=True)

    return dkappa


def Kappa_flatten(kappa_file, val_min, val_max, sensors_nbr, sensor_init, sensor, sheet_kappa):

    '''
    Version 2021.02.19
    Flattening of data for statistical analysis of the cutting efficiency calculated
    from the bow in-situ measurements by bow2kappa function

    Inputs
    - kappa_file: name of the results file (output of bow2kappa function)
    - val_min, val_max: minimum and maximum values of the cut-progress range
                        used for plot title label
    - sensors_nbr: number of sensors used for the bow in-situ measurements (parameter of the cut)
    - sensor_init: label of the first sensor of the sensors
    - sensor: index of the sensor of which the data are analyzed among the sensors used for the measurements

    Called functions
     - Kappa_data: build dkappa dictionary of the cutting efficiency data calculated from the bow in-situ measurements
              by bow2kappa function on the specified cut-progress range

    Outputs
    - dkappa_flatten: flattened dkappa dictionary

    '''
    # Local imports
    from .BatchPlot import Data_extract
    
    # Selection of data
    dk = Data_extract(kappa_file, sheet_kappa, sensors_nbr)
    dkappa = Kappa_data(dk, val_min, val_max, sensors_nbr)
    dkappa = dkappa.drop(["Cut progress (%)"],axis=1)

    if sensor != 0:
        sensors = []
        for s in range(sensors_nbr):
            sensors.append(s)
        for s in sensors:
            if s != sensor-1 :
                dkappa = dkappa.drop(["Kappa " + str(sensor_init + s) + " x10^7 (m/N)"],axis=1)

    # dkappa flattening
    dkappa_flatten = dkappa.values.flatten()

    return dkappa_flatten

def Kappa_hist(dkappa_flat, x_min, x_max):

    '''
    Version 2021.02.19
    Statistical analysis of the cutting efficiency calculated from the bow in-situ measurements
    by bow2kappa function

    Inputs
    - dkappa_flat: dictionary containing the cutting efficiency data to be analysed
    - x_min, x_max: minimum and maximum values of the cutting efficiency range
                    used for the histogram plot

    Outputs
    - Histogram plot of the cutting efficiency values
    '''

    # 3rd party imports
    import numpy as np
    import matplotlib.pyplot as plt

    # Histogram plot
    plt.hist(dkappa_flat,bins=25)
    plt.xlim(x_min,x_max)
    plt.xlabel('Cutting efficiency (10$^{-7}$ m.N$^{-1}$)',fontsize=12)

def Kappa_bbox(dkappa_flat, x_min, x_max):

    '''
    Version 2021.02.19
    Statistical analysis of the cutting efficiency calculated from the bow in-situ measurements
    by bow2kappa function

    Inputs
    - dkappa_flat: dictionary containing the cutting efficiency data to be analysed
    - x_min, x_max: minimum and maximum values of the cutting efficiency range
                    used for the boxplot plot

    Outputs
    - Histogram plot of the cutting efficiency values
    - Box plot of the cutting efficiency values
    '''

    # 3rd party imports
    import numpy as np
    import matplotlib.pyplot as plt

    # Boxplot plot
    plt.boxplot(dkappa_flat)

    plt.ylim(x_min,x_max)
