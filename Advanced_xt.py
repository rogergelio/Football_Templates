# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:30:59 2023

@author: rogel
"""
#Imports
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer import Sbopen, Pitch

#Sacar datos
parser = Sbopen()
df_match = parser.match(competition_id=43, season_id=106)

# first let's get the match file which lists all the match identifiers for
# the 87 games from the FA WSL 2019/20
def xt_per_game(df_match):
	pitch = Pitch(line_zorder=2)
	bins = (pitch.dim.positional_x[[0, 3, 4, 5, 6]], pitch.dim.positional_y)
	#filtered_match_df = df_match[(df_match['home_team_group'] == "E")]
	match_ids = df_match.match_id.unique()
	# next we create a dataframe of all the events
	all_events_df = []
	set_pieces = ['Throw-in', 'Free Kick', 'Goal Kick', 'Corner', 'Kick Off', 'Penalty']
	cols = ['match_id', 'id', 'type_name', 'sub_type_name', 'player_name',
	        'x', 'y', 'end_x', 'end_y', 'outcome_name', 'shot_statsbomb_xg']
	for match_id in match_ids:
	    # get carries/ passes/ shots
	    event = parser.event(match_id)[0]  # get the first dataframe (events) which has index = 0
	    event = event.loc[((event.type_name.isin(['Carry', 'Shot', 'Pass'])) &
	                       (~event['sub_type_name'].isin(set_pieces))),  # remove set-piece events
	                      cols].copy()
	
	    # boolean columns for working out probabilities
	    event['goal'] = event['outcome_name'] == 'Goal'
	    event['shoot'] = event['type_name'] == 'Shot'
	    event['move'] = event['type_name'] != 'Shot'
	    all_events_df.append(event)
	event = pd.concat(all_events_df)
	
	shot_probability = pitch.bin_statistic(event['x'], event['y'], values=event['shoot'],
	                                       statistic='mean', bins=bins)
	move_probability = pitch.bin_statistic(event['x'], event['y'], values=event['move'],
	                                       statistic='mean', bins=bins)
	goal_probability = pitch.bin_statistic(event.loc[event['shoot'], 'x'],
	                                       event.loc[event['shoot'], 'y'],
	                                       event.loc[event['shoot'], 'shot_statsbomb_xg'],
	                                       statistic='mean',
	                                       bins=bins)
	
	fig, ax = pitch.draw()
	shot_heatmap = pitch.heatmap(shot_probability, ax=ax)
	
	fig, ax = pitch.draw()
	move_heatmap = pitch.heatmap(move_probability, ax=ax)
	
	fig, ax = pitch.draw()
	goal_heatmap = pitch.heatmap(goal_probability, ax=ax)
	
	# get a dataframe of move events and filter it
	# so the dataframe only contains actions inside the pitch.
	move = event[event['move']].copy()
	bin_start_locations = pitch.bin_statistic(move['x'], move['y'], bins=bins)
	move = move[bin_start_locations['inside']].copy()
	
	# get the successful moves, which filters out the events that ended outside the pitch
	# or where not successful (null)
	bin_end_locations = pitch.bin_statistic(move['end_x'], move['end_y'], bins=bins)
	move_success = move[(bin_end_locations['inside']) & (move['outcome_name'].isnull())].copy()
	
	# get a dataframe of the successful moves
	# and the grid cells they started and ended in
	bin_success_start = pitch.bin_statistic(move_success['x'], move_success['y'], bins=bins)
	bin_success_end = pitch.bin_statistic(move_success['end_x'], move_success['end_y'], bins=bins)
	df_bin = pd.DataFrame({'x': bin_success_start['binnumber'][0],
	                       'y': bin_success_start['binnumber'][1],
	                       'end_x': bin_success_end['binnumber'][0],
	                       'end_y': bin_success_end['binnumber'][1]})
	
	# calculate the bin counts for the successful moves, i.e. the number of moves between grid cells
	bin_counts = df_bin.value_counts().reset_index(name='bin_counts')
	
	# create the move_transition_matrix of shape (num_y_bins, num_x_bins, num_y_bins, num_x_bins)
	# this is the number of successful moves between grid cells.
	num_y, num_x = shot_probability['statistic'].shape
	move_transition_matrix = np.zeros((num_y, num_x, num_y, num_x))
	move_transition_matrix[bin_counts['y'], bin_counts['x'],
	                       bin_counts['end_y'], bin_counts['end_x']] = bin_counts.bin_counts.values
	
	# and divide by the starting locations for all moves (including unsuccessful)
	# to get the probability of moving the ball successfully between grid cells
	bin_start_locations = pitch.bin_statistic(move['x'], move['y'], bins=bins)
	bin_start_locations = np.expand_dims(bin_start_locations['statistic'], (2, 3))
	move_transition_matrix = np.divide(move_transition_matrix,
	                                   bin_start_locations,
	                                   out=np.zeros_like(move_transition_matrix),
	                                   where=bin_start_locations != 0,
	                                   )
	
	move_transition_matrix = np.nan_to_num(move_transition_matrix)
	shot_probability_matrix = np.nan_to_num(shot_probability['statistic'])
	move_probability_matrix = np.nan_to_num(move_probability['statistic'])
	goal_probability_matrix = np.nan_to_num(goal_probability['statistic'])
	
	xt = np.multiply(shot_probability_matrix, goal_probability_matrix)
	diff = 1
	iteration = 0
	while np.any(diff > 0.00001):  # iterate until the differences between the old and new xT is small
	    xt_copy = xt.copy()  # keep a copy for comparing the differences
	    # calculate the new expected threat
	    xt = (np.multiply(shot_probability_matrix, goal_probability_matrix) +
	          np.multiply(move_probability_matrix,
	                      np.multiply(move_transition_matrix, np.expand_dims(xt, axis=(0, 1))).sum(
	                          axis=(2, 3)))
	          )
	    diff = (xt - xt_copy)
	    iteration += 1
	print('Number of iterations:', iteration)
	
	path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
	            path_effects.Normal()]
	# new bin statistic for plotting xt only
	for_plotting = pitch.bin_statistic(event['x'], event['y'], bins=bins)
	for_plotting['statistic'] = xt
	fig, ax = pitch.draw(figsize=(14, 9.625))
	_ = pitch.heatmap(for_plotting, ax=ax)
	_ = pitch.label_heatmap(for_plotting, ax=ax, str_format='{:.2%}',
	                        color='white', fontsize=14, va='center', ha='center',
	                        path_effects=path_eff)
	# sphinx_gallery_thumbnail_path = 'gallery/tutorials/images/sphx_glr_plot_xt_improvements_004'
	fig.patch.set_facecolor('#111111')
	# first get grid start and end cells
	grid_start = pitch.bin_statistic(move_success.x, move_success.y, bins=bins)
	grid_end = pitch.bin_statistic(move_success.end_x, move_success.end_y, bins=bins)
	
	# then get the xT values from the start and end grid cell
	start_xt = xt[grid_start['binnumber'][1], grid_start['binnumber'][0]]
	end_xt = xt[grid_end['binnumber'][1], grid_end['binnumber'][0]]
	
	# then calculate the added xT
	added_xt = end_xt - start_xt
	move_success['xt'] = added_xt
	
	Xt_final=move_success.groupby('player_name')['xt'].sum().sort_values(ascending=False)
	return Xt_final

res_model=xt_per_game(df_match)

