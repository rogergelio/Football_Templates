# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:25:00 2023

@author: rogel
"""
#Utilerías 
from statsbombpy import sb
import pandas as pd
import numpy as np

matches=sb.matches(competition_id=43, season_id=106)

def event_start11(events):
	event_type=events.query("type == 'Starting XI'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_half_start(events):
	event_type=events.query("type == 'Half Start'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_passes(events):
	event_type=events.query("type == 'Pass'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_ball_receipt(events):
	event_type=events.query("type == 'Ball Receipt'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_carries(events):
	event_type=events.query("type == 'Carry'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_clearances(events):
	event_type=events.query("type == 'Clearance'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_pressures(events):
	event_type=events.query("type == 'Pressure'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_disposessed(events):
	event_type=events.query("type == 'Dispossessed'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_duel(events):
	event_type=events.query("type == 'Duel'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_error(events):
	event_type=events.query("type == 'Error'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_fouls(events):
	event_type=events.query("type == 'Foul Comitted'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_fouls_won(events):
	event_type=events.query("type == 'Foul Won'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_dribbled_past(events):
	event_type=events.query("type == 'Dribbled Past'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_dribble(events):
	event_type=events.query("type == 'Dribble'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_block(events):
	event_type=events.query("type == 'Block'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_miscontrol(events):
	event_type=events.query("type == 'Miscontrol'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_bad_behaviour(events):
	event_type=events.query("type == 'Bad Behaviour'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_ball_recovery(events):
	event_type=events.query("type == 'Ball Recovery'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type
	
def event_injury_stoppage(events):
	event_type=events.query("type == 'Injury Stoppage'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_player_off(events):
	event_type=events.query("type == 'Player Off'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_player_on(events):
	event_type=events.query("type == 'Player On'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_5050(events):
	event_type=events.query("type == '50/50'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_interception(events):
	event_type=events.query("type == 'Interception'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_shot(events):
	event_type=events.query("type == 'Shot'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_goalkeeper(events):
	event_type=events.query("type == 'Goal Keeper'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_referee_ball_drop(events):
	event_type=events.query("type == 'Referee Ball-Drop'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_substitution(events):
	event_type=events.query("type == 'Substitution'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_shield(events):
	event_type=events.query("type == 'Shield'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_own_goal_for(events):
	event_type=events.query("type == 'Own Goal For'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_own_goal_against(events):
	event_type=events.query("type == 'Own Goal Against'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_offside(events):
	event_type=events.query("type == 'Offside'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_half_end(events):
	event_type=events.query("type == 'Half End'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

def event_tactical_shift(events):
	event_type=events.query("type == 'Tactical Shift'")
	event_type=event_type.dropna(axis=1, how="all")
	return event_type

res=sb.events(matches.iloc[0].match_id)
# Create an empty list to store DataFrames
df_list = []

for i in range(0,len(matches)):
	data=sb.events(matches.iloc[i].match_id)
	df_list.append(data)
	print(i)
	
# Concatenate the DataFrames in the list into a single DataFrame
df = pd.concat(df_list, ignore_index=True)

shots=event_passes(df)
shots.to_csv('wc_passes.csv')
examplple=df.iloc[27]
distinct_values = df['type'].unique()
print(str(shots.iloc[0]))
aa=shots.groupby('player').agg(lambda x: x.count() if pd.api.types.is_numeric_dtype(x) else x.value_counts())






