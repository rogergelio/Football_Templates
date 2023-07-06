# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:43:51 2023

@author: rogel
"""

from statsbombpy import sb
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from urllib.request import urlopen
import warnings
import cmasher as cmr
from PIL import Image
from highlight_text import ax_text
from mplsoccer import Pitch, VerticalPitch, add_image, FontManager, Sbopen
from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
from matplotlib.colors import to_rgba
import matplotlib.patheffects as path_effects

matches=sb.matches(competition_id=43, season_id=106)


events=sb.events(3857256)

shots=pd.read_csv('wc_shots.csv')
related_events=shots.iloc[1].related_events
all_related_events=[]
for i in range (0,len(shots)):
	related_events=events.query(f"id=={shots.iloc[i].related_events}")
	all_related_events.append(related_events)
	
related_events_df = pd.concat(all_related_events, ignore_index=True)


	