# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 16:29:59 2023

@author: rogel
"""
from statsbombpy import sb
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)
from Metodos_Generales import plot_shotmap, plot_shots, joint_shotmap, plot_passes
import matplotlib.pyplot as plt
import seaborn as sns


fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
                       'rubikmonoone/RubikMonoOne-Regular.ttf')

comps=sb.competitions()
matches=sb.matches(competition_id=43, season_id=106)

Mex_Arg=matches.iloc[13]
match_id=Mex_Arg.match_id
events=sb.events(match_id)
home_team=Mex_Arg.home_team
away_team=Mex_Arg.away_team
home_color="#00DDFF"
away_color="#11CC00"

lineup_home=events.iloc[0].tactics["lineup"]
lineup_away=events.iloc[1].tactics["lineup"]


parser = Sbopen()
df_event, df_related, df_freeze, df_tactics = parser.event(match_id)
lineup = parser.lineup(match_id)


#Sacar el lineup
df_lineup = parser.lineup(Mex_Arg.match_id)
df_lineup = df_lineup[['player_id', 'jersey_number', 'team_name']].copy()

# %% Shots
shots=events.query("type == 'Shot'")
shots=shots.dropna(axis=1, how="all")
shots['x'] = shots['location'].apply(lambda loc: loc[0])
shots['y'] = shots['location'].apply(lambda loc: loc[1])
shots['end_x'] = shots['shot_end_location'].apply(lambda loc: loc[0])
shots['end_y'] = shots['shot_end_location'].apply(lambda loc: loc[1])

shots_home=shots.query(f"team == '{home_team}'")
shots_away=shots.query(f"team == '{away_team}'")

# filter goals / non-shot goals
goals_home = shots_home.query("shot_outcome=='Goal'")
non_goal_shots_home = shots_home.query("shot_outcome!='Goal'")
goals_away = shots_away.query("shot_outcome=='Goal'")
non_goal_shots_away = shots_away.query("shot_outcome!='Goal'")

events, related, freeze, tactics = parser.event(match_id)
lineup = parser.lineup(match_id)

#Shotmaps por equipo
plot_shotmap(home_team, away_team, non_goal_shots_home, goals_home, home_color, away_color)
plot_shotmap(away_team ,home_team, non_goal_shots_away, goals_away, away_color, home_color)

#Shotmap conjunto
joint_shotmap(shots, home_team, away_team, shots_home, shots_away, home_color, away_color)

#Shotmaps generales
plot_shots(shots, df_freeze, home_team, away_team,df_lineup, home_color, away_color)

#Grid de pases
plot_passes(events, lineup, tactics, home_team, away_team)
plot_passes(events, lineup, tactics, away_team, home_team)


