# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 16:29:59 2023

@author: rogel
"""
from statsbombpy import sb
import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)
from Metodos_Generales import plot_shotmap, plot_shots, joint_shotmap, plot_passes, draw_passgrid, xt_per_game, plot_xt, plot_green
import seaborn as sns
from matplotlib.colors import to_rgba
import gc
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
                       'rubikmonoone/RubikMonoOne-Regular.ttf')
print("imports done")

comps=sb.competitions()
matches=sb.matches(competition_id=43, season_id=106)

Mex_Arg=matches.iloc[13]
match_id=Mex_Arg.match_id
aaa=match_id
events=sb.events(match_id)
home_team=Mex_Arg.home_team
away_team=Mex_Arg.away_team
home_color="#00DDFF"
away_color="#11CC00"
home_goals=Mex_Arg.home_score
away_goals=Mex_Arg.away_score


lineup_home=events.iloc[0].tactics["lineup"]
lineup_away=events.iloc[1].tactics["lineup"]

home_formation=events.iloc[0].tactics["formation"]
away_formation=events.iloc[1].tactics["formation"]
print("lineup done")
parser = Sbopen()
df_event, df_related, df_freeze, df_tactics = parser.event(match_id)
lineup = parser.lineup(match_id)


#Sacar el lineup
df_lineup = parser.lineup(Mex_Arg.match_id)
df_lineup = df_lineup[['player_id', 'jersey_number', 'team_name']].copy()
distinct_values = events['type'].unique()
passes=events.query("type == 'Pass'")
passes=passes.dropna(axis=1, how="all")
passes_under_pressure=passes.query("under_pressure==True")
# %% Shots
shots=events.query("type == 'Shot'")
#shots=pd.read_csv('wc_shots.csv')
shots=shots.dropna(axis=1, how="all")
shots['x'] = shots['location'].apply(lambda loc: loc[0])
shots['y'] = shots['location'].apply(lambda loc: loc[1])
shots['end_x'] = shots['shot_end_location'].apply(lambda loc: loc[0])
shots['end_y'] = shots['shot_end_location'].apply(lambda loc: loc[1])

shots_home=shots.query(f"team == '{home_team}'")
shots_away=shots.query(f"team == '{away_team}'")

home_xg=sum(shots_home.shot_statsbomb_xg)
away_xg=sum(shots_home.shot_statsbomb_xg)

player_xg_count=shots.groupby("player")["shot_statsbomb_xg"].count()
player_xg_sum=shots.groupby("player")["shot_statsbomb_xg"].sum()

home_xg_per_shot=home_xg/len(shots_home)
away_xg_per_shot=away_xg/len(shots_away)

# filter goals / non-shot goals
goals_home = shots_home.query("shot_outcome=='Goal'")
non_goal_shots_home = shots_home.query("shot_outcome!='Goal'")
goals_away = shots_away.query("shot_outcome=='Goal'")
non_goal_shots_away = shots_away.query("shot_outcome!='Goal'")

events, related, freeze, tactics = parser.event(match_id)
lineup = parser.lineup(match_id)

df_match = parser.match(competition_id=43, season_id=106)


#Shotmaps por equipo
plot_shotmap(home_team, away_team, non_goal_shots_home, goals_home, home_color, away_color)
plot_shotmap(away_team ,home_team, non_goal_shots_away, goals_away, away_color, home_color)
'''
#Shotmap conjunto
joint_shotmap(shots, home_team, away_team, shots_home, shots_away, home_color, away_color)

#Shotmaps generales
plot_shots(shots, df_freeze, home_team, away_team,df_lineup, home_color, away_color)

#Grid de pases
plot_passes(events, lineup, tactics, home_team, away_team)
plot_passes(events, lineup, tactics, away_team, home_team)

#Passgrid
events, related, freeze, players = parser.event(match_id)
draw_passgrid(events, related, freeze, players, away_team, away_formation, home_team, away_color)
events, related, freeze, players = parser.event(match_id)
draw_passgrid(events, related, freeze, players, home_team, home_formation, away_team, home_color)


#Expected Threat
expected_threat_games=xt_per_game(df_match.iloc[13:14])

# Select the first 10 objects
data = expected_threat_games[:10]
data2=player_xg_sum[:10]
	
plot_xt(data, home_team, away_team)
plot_green(data2, f"Expected Goals {home_team} vs {away_team}")
'''