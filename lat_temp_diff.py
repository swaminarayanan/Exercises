import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl

# Load the dataset (replace 'N:\\temp2m.nc' with your actual file path)
ds = xr.open_dataset(r'/home/lab/Desktop/Narayanswamy/ruff/temp2m.nc')
ds1 = ds['t2m'] - 273.16  # Convert temperature from Kelvin to Celsius

# Resample the data from daily to monthly, taking the mean
monthly_utci = ds1.resample(time='M').mean(dim='time')

# Calculate the mean along the longitude dimension
utci_monthly = monthly_utci.mean(dim='longitude')[::-1]

# Select latitude and process further
hh_monthly1 = utci_monthly.sel(latitude=6).values
hh_monthly2 = utci_monthly.sel(latitude=15).values
hh_monthly3 = utci_monthly.sel(latitude=-15).values
hh_monthly4 = utci_monthly.sel(latitude=35).values
hh_monthly5 = utci_monthly.sel(latitude=-35).values
hh_monthly6 = utci_monthly.sel(latitude=60).values
hh_monthly7 = utci_monthly.sel(latitude=-60).values

# Convert the time data to a normal datetime format
time = pd.to_datetime(monthly_utci.time.values)

# If time steps are shifted, apply a one-month shift back
time_adjusted = time - pd.DateOffset(months=1)

# Create x-axis ticks for 12 months in 2020
x_ticks = pd.date_range(start='2020-01-01', end='2020-12-31', freq='MS')

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(10, 6))
# Plotting line plot for different latitudes
ax1.plot(time_adjusted, hh_monthly1, marker='D', linestyle='-', color='red', label='close to Equator (6°)')
ax1.plot(time_adjusted, hh_monthly2, marker='*', linestyle='-', color='brown', label='Tropics (15°)')
ax1.plot(time_adjusted, hh_monthly3, marker='*', linestyle='-', color='y', label='Tropics (-15°)')
ax1.plot(time_adjusted, hh_monthly4, marker='o', linestyle='-', color='g', label='Subtropics (35°)')
ax1.plot(time_adjusted, hh_monthly5, marker='o', linestyle='-', color='k', label='Subtropics (-35°)')
ax1.plot(time_adjusted, hh_monthly6, marker='p', linestyle='-', color='orange', label='polar (60°)')
ax1.plot(time_adjusted, hh_monthly7, marker='H', linestyle='-', color='b', label='polar (-60°)')

# Set x-axis ticks and labels
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_ticks.strftime('%b-%Y'), rotation=45, fontsize=15, fontweight='bold')

# Customize primary y-axis labels and title
ax1.set_ylabel('T2M Temp (°C)', fontsize=12, fontweight='bold')
# Add y-ticks based on the data range
y_ticks = np.arange(np.floor(min(hh_monthly1.min(), hh_monthly2.min(), hh_monthly3.min(),
                                hh_monthly4.min(), hh_monthly5.min(), hh_monthly6.min(), 
                                hh_monthly7.min())),
                    np.ceil(max(hh_monthly1.max(), hh_monthly2.max(), hh_monthly3.max(),
                                hh_monthly4.max(), hh_monthly5.max(), hh_monthly6.max(), 
                                hh_monthly7.max())) + 1, 2)
ax1.set_yticks(y_ticks)
ax1.set_yticklabels(y_ticks, rotation=0, fontsize=15, fontweight='bold')
ax1.set_title('Latitudinal Temperature difference', fontsize=15, fontweight='bold')
ax1.grid(True)

# Add legends directly on plot lines
ax1.text(time_adjusted[6], hh_monthly1[3], 'close to Equator (6°)', color='red', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[0], hh_monthly2[7], 'Tropics (15°)', color='brown', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[7], hh_monthly3[-7], 'Tropics (-15°)', color='y', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[9], hh_monthly4[1], 'Subtropics (35°)', color='green', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[9], hh_monthly5[-4], 'Subtropics (-35°)', color='k', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[9], hh_monthly6[1], 'polar (60°)', color='orange', fontsize=13, verticalalignment='center', fontweight='bold')
ax1.text(time_adjusted[4], hh_monthly7[-5], 'polar (-60°)', color='b', fontsize=13, verticalalignment='center', fontweight='bold')

plt.tight_layout()
mpl.rcParams.update({
    "font.weight": "bold",
    "axes.labelweight": "bold",
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    "axes.linewidth": 2,
    "patch.linewidth": 2,
    'xtick.major.size': 16,
    'ytick.major.size': 16,
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    'axes.titlesize': 16,  # For axes titles
    'figure.titlesize': 25  # For overall figure title
})
plt.show()
