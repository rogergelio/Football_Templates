import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from mplsoccer import Pitch, VerticalPitch, FontManager, Sbopen
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
pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color=bg_color)
fig, ax = pitch.draw(figsize=(4.125, 6))
fig.set_facecolor(bg_color)
bin_statistic = pitch.bin_statistic(df_pressure.x, df_pressure.y, statistic='count', bins=(6, 6), normalize=True)
pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolor=bg_color)
labels = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=18,
                             ax=ax, ha='center', va='center',
                             str_format='{:.0%}', path_effects=path_eff)