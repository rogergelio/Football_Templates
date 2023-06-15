import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch, FontManager, Sbopen
bg_color='#33312b'


# get data
parser = Sbopen()
match_files = [19789, 19794, 19805]
df = pd.concat([parser.event(file)[0] for file in match_files])  # 0 index is the event file

# filter chelsea pressure and pass events
mask_chelsea_pressure = (df.team_name == 'Chelsea FCW') & (df.type_name == 'Pressure')
df_pressure = df.loc[mask_chelsea_pressure, ['x', 'y']]
mask_chelsea_pressure = (df.team_name == 'Chelsea FCW') & (df.type_name == 'Pass')
df_pass = df.loc[mask_chelsea_pressure, ['x', 'y', 'end_x', 'end_y']]
 
##############################################################################
# Load some fonts, path effects, and a custom colormap
# fontmanager for google font (robotto)
robotto_regular = FontManager()

# path effects
path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
            path_effects.Normal()]

# see the custom colormaps example for more ideas on setting colormaps
pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#15242e', '#4393c4'], N=10)

##############################################################################
pitch = Pitch(line_zorder=2)
fig, ax = pitch.draw()
bin_statistic = pitch.bin_statistic(df_pass.x, df_pass.y, bins=(6, 5))
bin_statistic_end = pitch.bin_statistic(df_pass.end_x, df_pass.end_y, bins=(6, 5))

# let's get a mask for all passes that started in one grid cell and ended in another
mask_start = np.logical_and(bin_statistic['binnumber'][0] == 5,  # xs 5th box from left (zero indexed)
                            bin_statistic['binnumber'][1] == 0)  # ys 2nd from bottom (zero indexed)
mask_end = np.logical_and(bin_statistic_end['binnumber'][0] == 5,  # xs 6th box from left (zero indexed)
                          bin_statistic_end['binnumber'][1] == 2)  # ys 3rd box from bottom (zero indexed)
mask = np.logical_and(mask_start, mask_end)

# plot the passes that started in one grid cell and ended in another
pitch.scatter(df_pass.x[mask], df_pass.y[mask], ax=ax, fc='green',
              marker='o', s=100, ec='darkslategrey', lw=3, alpha=0.6, zorder=4)
pitch.arrows(df_pass.x[mask], df_pass.y[mask], df_pass.end_x[mask], df_pass.end_y[mask],
             ax=ax, zorder=10, color='red')

# plot all of the starting locations as a heatmap
pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolor='#f9f9f9', alpha=0.5)

plt.show()  # If you are using a Jupyter notebook you do not need this line