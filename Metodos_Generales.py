# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:33:54 2023

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

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
                       'rubikmonoone/RubikMonoOne-Regular.ttf')


def plot_shotmap(home_team, away_team, non_goal_shots_home, goals_home, home_color, away_color):
	pitch = VerticalPitch(pad_bottom=0.5,  # pitch extends slightly below halfway line
	                      half=True,  # half of a pitch
	                      goal_type='box',
						  pitch_color="#111111",
	                      goal_alpha=0.9)  # control the goal transparency

	fig, axs = pitch.grid(figheight=10, title_height=0.12, endnote_space=0,
	                      # Turn off the endnote/title axis. I usually do this after
	                      # I am happy with the chart layout and text placement
	                      axis=False,
	                      title_space=0, grid_height=0.82, endnote_height=0.05)

	# Set the background color of the figure
	fig.patch.set_facecolor('#111111')

	# plot non-goal shots with hatch
	sc1 = pitch.scatter(non_goal_shots_home.x, non_goal_shots_home.y,
	                    # size varies between 100 and 1900 (points squared)
	                    s=(non_goal_shots_home.shot_statsbomb_xg * 2900) + 100,
	                    edgecolors=home_color,  # give the markers a charcoal border
	                    c='None',  # no facecolor for the markers
	                    hatch='///',  # the all important hatch (triple diagonal lines)
	                    # for other markers types see: https://matplotlib.org/api/markers_api.html
	                    marker='s',
	                    ax=axs['pitch'])

	# plot goal shots with a color
	sc2 = pitch.scatter(goals_home.x, goals_home.y,
	                    # size varies between 100 and 1900 (points squared)
	                    s=(goals_home.shot_statsbomb_xg * 2900) + 100,
	                    edgecolors='#606060',  # give the markers a charcoal border
	                    c=home_color,  # color for scatter in hex format
	                    # for other markers types see: https://matplotlib.org/api/markers_api.html
	                    marker='o',
	                    ax=axs['pitch'])

	# endnote text
	axs['endnote'].text(1, 0.5, '@rogergelioo', color=pitch.line_color,
	                    va='center', ha='right', fontsize=15,
	                    fontproperties=fm_rubik.prop)

	# title text
	title1 = axs['title'].text(0.5, 0.8, f"{home_team}", color=home_color,
	                           va='center', ha='center', fontproperties=fm_rubik.prop, fontsize=30)
	title2 = axs['title'].text(0.5, 0.45, "shots versus", color=pitch.line_color,
	                           va='center', ha='center', fontproperties=fm_rubik.prop, fontsize=20)
	title3 = axs['title'].text(0.5, 0.2, f"{away_team}", color=away_color,
	                           va='center', ha='center', fontproperties=fm_rubik.prop, fontsize=20)
	plt.savefig(f'{title1}.jpg', format='jpeg')
def joint_shotmap(shots, home_team, away_team, shots_home, shots_away, home_color, away_color):
	home_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
	                                                       ['#002C33', home_color], N=10)
	away_cmap = LinearSegmentedColormap.from_list("El Greco Violet - 10 colors",
	                                                         ['#043300', away_color], N=10)

	pitch = Pitch(pad_top=0.05, pad_right=0.05, pad_bottom=0.20, pad_left=0.05, line_zorder=2, pitch_color="#111111",)
	vertical_pitch = VerticalPitch(half=True, pad_top=0.05, pad_right=0.05, pad_bottom=0.05,
	                               pad_left=0.05, line_zorder=2, pitch_color="#111111",)
	
	# setup a mplsoccer FontManager to download google fonts (Roboto-Regular / SigmarOne-Regular)
	fm = FontManager()
	fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
	                       'RubikMonoOne-Regular.ttf')
	
	# subset the shots
	df_shots = shots.copy()
	
	# subset the shots for each team
	team1, team2 = home_team,away_team
	df_team1 = shots_home
	df_team2 = shots_away
	
	# Usually in football, the data is collected so the attacking direction is left to right.
	# We can shift the coordinates via: new_x_coordinate = right_side - old_x_coordinate
	# This is helpful for having one team shots on the left of the pitch and the other on the right
	df_team1['x'] = pitch.dim.right - df_team1.x
	
	
	fig, axs = pitch.jointgrid(figheight=10,  # the figure is 10 inches high
	                           left=None,  # joint grid center-aligned
	                           bottom=0.075,  # grid starts 7.5% in from the bottom of the figure
	                           marginal=0.1,  # marginal axes heights are 10% of grid height
	                           space=0,  # 0% of the grid height reserved for space between axes
	                           grid_width=0.9,  # the grid width takes up 90% of the figure width
	                           title_height=0,  # plot without a title axes
	                           axis=False,  # turn off title/ endnote/ marginal axes
	                           endnote_height=0,  # plot without an endnote axes
	                           grid_height=0.8)  # grid takes up 80% of the figure height
	# we plot a usual scatter plot but the scatter size is based on expected goals
	# note that the size is the expected goals * 700
	fig.patch.set_facecolor('#111111')
	
	# so any shots with an expected goals = 1 would take a size of 700 (points**2)
	sc_team1 = pitch.scatter(df_team1.x, df_team1.y, s=df_team1.shot_statsbomb_xg * 2100,
	                         ec='black', color=home_color, ax=axs['pitch'])
	sc_team2 = pitch.scatter(df_team2.x, df_team2.y, s=df_team2.shot_statsbomb_xg * 2100,
	                         ec='black', color=away_color, ax=axs['pitch'])
	# (step) histograms on each of the left, top, and right marginal axes
	team1_hist_y = sns.histplot(y=df_team1.y, ax=axs['left'], element='step', color=home_color)
	team1_hist_x = sns.histplot(x=df_team1.x, ax=axs['top'], element='step', color=home_color)
	team2_hist_x = sns.histplot(x=df_team2.x, ax=axs['top'], element='step', color=away_color)
	team2_hist_y = sns.histplot(y=df_team2.y, ax=axs['right'], element='step', color=away_color)
	txt1 = axs['pitch'].text(x=15, y=70, s=team1, fontproperties=fm.prop, color=home_color,
	                         ha='center', va='center', fontsize=45)
	txt2 = axs['pitch'].text(x=105, y=70, s=team2, fontproperties=fm.prop, color=away_color,
	                         ha='center', va='center', fontsize=45)
	plt.savefig(f'{txt1}.jpg', format='jpeg')
	
	
	###############################################################
	
	
	
	fig, axs = pitch.jointgrid(figheight=10, left=None, bottom=0.075, grid_height=0.8,
                           # plot without endnote/ title axes
                           title_height=0, endnote_height=0,
                           axis=False)
	bs1 = pitch.bin_statistic(df_team1.x, df_team1.y, bins=(18, 12))
	bs2 = pitch.bin_statistic(df_team2.x, df_team2.y, bins=(18, 12))
	# get the min/ max values for normalizing across both teams
	vmax = max(bs2['statistic'].max(), bs1['statistic'].max())
	vmin = max(bs2['statistic'].min(), bs1['statistic'].min())
	# set values where zero shots to nan values so it does not show up in the heatmap
	# i.e. zero values take the background color
	bs1['statistic'][bs1['statistic'] == 0] = np.nan
	bs2['statistic'][bs2['statistic'] == 0] = np.nan
	# set the vmin/ vmax so the colors depend on the minimum/maximum value for both teams
	hm1 = pitch.heatmap(bs1, ax=axs['pitch'], cmap=home_cmap, vmin=vmin, vmax=vmax, edgecolor='#808080')
	hm2 = pitch.heatmap(bs2, ax=axs['pitch'], cmap=away_cmap, vmin=vmin, vmax=vmax, edgecolor='#808080')
	# histograms with kdeplot
	fig.patch.set_facecolor('#111111')
	
	team1_hist_y = sns.histplot(y=df_team1.y, ax=axs['left'], color=home_color, linewidth=1, kde=True)
	team1_hist_x = sns.histplot(x=df_team1.x, ax=axs['top'], color=home_color, linewidth=1, kde=True)
	team2_hist_x = sns.histplot(x=df_team2.x, ax=axs['top'], color=away_color, linewidth=1, kde=True)
	team2_hist_y = sns.histplot(y=df_team2.y, ax=axs['right'], color=away_color, linewidth=1, kde=True)
	txt1 = axs['pitch'].text(x=25, y=70, s=team1, fontproperties=fm.prop, color=home_color,
	                         ha='center', va='center', fontsize=45)
	txt2 = axs['pitch'].text(x=95, y=70, s=team2, fontproperties=fm.prop, color=away_color,
	                         ha='center', va='center', fontsize=45)
	plt.savefig(f'{txt1}.jpg', format='jpeg')

def plot_shots(shots, df_freeze, home_team, away_team,df_lineup, home_color, away_color):
		
	for i in range(0,len(shots)):
		plt.style.use('ggplot')
		
		# lineup data
		
		SHOT_ID = shots.iloc[i].id
		df_freeze_frame = df_freeze[df_freeze.id == SHOT_ID].copy()
		df_shot_event = shots.iloc[i]
		# add the jersey number
		df_freeze_frame = df_freeze_frame.merge(df_lineup, how='left', on='player_id')
		# strings for team names
		team1 = home_team
		team2 = away_team
		
		# subset the team shooting, and the opposition (goalkeeper/ other)
		df_team1 = df_freeze_frame[df_freeze_frame.team_name == team1]
		df_team2_goal = df_freeze_frame[(df_freeze_frame.team_name == team2) &
		                                (df_freeze_frame.position_name == 'Goalkeeper')]
		df_team2_other = df_freeze_frame[(df_freeze_frame.team_name == team2) &
		                                 (df_freeze_frame.position_name != 'Goalkeeper')]
		# Setup the pitch
		pitch = VerticalPitch(half=True, goal_type='box', pad_bottom=-20, pitch_color="#111111")
		
		# We will use mplsoccer's grid function to plot a pitch with a title axis.
		fig, axs = pitch.grid(figheight=8, endnote_height=0,  # no endnote
		                      title_height=0.1, title_space=0.02, 
		                      # Turn off the endnote/title axis. I usually do this after
		                      # I am happy with the chart layout and text placement
		                      axis=False,
		                      grid_height=0.83)
		fig.patch.set_facecolor('#111111')
		# Plot the players
		sc1 = pitch.scatter(df_team1.x, df_team1.y, s=700, c=home_color, label='Attacker', ax=axs['pitch'])
		sc2 = pitch.scatter(df_team2_other.x, df_team2_other.y, s=700,
		                    c=away_color, label='Defender', ax=axs['pitch'])
		sc4 = pitch.scatter(df_team2_goal.x, df_team2_goal.y, s=700,
		                    ax=axs['pitch'], c='#c15ca5', label='Goalkeeper')
		
		# plot the shot
		if(df_shot_event.shot_outcome=="Goal"):
			sc3 = pitch.scatter(df_shot_event.x, df_shot_event.y, marker='football',
		                    s=700, ax=axs['pitch'], label='Shooter', zorder=1.2)
		else:
			sc3 = pitch.scatter(df_shot_event.x, df_shot_event.y, marker='o',
		                    s=700, ax=axs['pitch'], label='Shooter', zorder=1.2)
		
		line = pitch.lines(df_shot_event.x, df_shot_event.y,
		                   df_shot_event.end_x, df_shot_event.end_y, comet=True,
		                   label='shot', color='#cb5a4c', ax=axs['pitch'])
		
		# plot the angle to the goal
		pitch.goal_angle(df_shot_event.x, df_shot_event.y, ax=axs['pitch'], alpha=0.2, zorder=1.1,
		                 color='#cb5a4c', goal='right')
		
		# fontmanager for google font (robotto)
		robotto_regular = FontManager()
		
		# plot the jersey numbers
		for i, label in enumerate(df_freeze_frame.jersey_number):
		    pitch.annotate(label, (df_freeze_frame.x[i], df_freeze_frame.y[i]),
		                   va='center', ha='center', color='black',
		                   fontproperties=robotto_regular.prop, fontsize=18, ax=axs['pitch'])
		
		# add a legend and title
		legend = axs['pitch'].legend(loc='center left', labelspacing=1.5)
		for text in legend.get_texts():
		    text.set_fontproperties(robotto_regular.prop)
		    text.set_fontsize(20)
		    text.set_va('center')
		title=str(df_shot_event.player)
		# title
		axs['title'].text(0.5, 0.5, f'{df_shot_event.player} ({df_shot_event.team})\n{team1} vs. {team2}',
		                  va='center', ha='center', color='white',
		                  fontproperties=robotto_regular.prop, fontsize=35)
		plt.savefig(f'{title}.jpg', format='jpeg')
		plt.show()  # If you are using a Jupyter notebook you do not need this line

def plot_passes(events, lineup, tactics, team1, team2):
	##############################################################################
	# Add on the subbed on/ off times to the lineup dataframe

	# dataframe with player_id and when they were subbed off
	time_off = events.loc[(events.type_name == 'Substitution'),
	                      ['player_id', 'minute']]
	time_off.rename({'minute': 'off'}, axis='columns', inplace=True)
	# dataframe with player_id and when they were subbed on
	time_on = events.loc[(events.type_name == 'Substitution'),
	                     ['substitution_replacement_id', 'minute']]
	time_on.rename({'substitution_replacement_id': 'player_id',
	                'minute': 'on'}, axis='columns', inplace=True)
	players_on = time_on.player_id
	# merge on times subbed on/off
	lineup = lineup.merge(time_on, on='player_id', how='left')
	lineup = lineup.merge(time_off, on='player_id', how='left')

	##############################################################################
	# Filter the lineup to include players who played and add on the first position they played

	# filter the tactics lineup for the starting xi
	starting_ids = events[events.type_name == 'Starting XI'].id
	starting_xi = tactics[tactics.id.isin(starting_ids)]
	starting_players = starting_xi.player_id

	# filter the lineup for players that actually played
	mask_played = ((lineup.on.notnull()) | (lineup.off.notnull()) |
	               (lineup.player_id.isin(starting_players)))
	lineup = lineup[mask_played].copy()

	# get the first position for each player and add this to the lineup dataframe
	player_positions = (events[['player_id', 'position_id']]
	                    .dropna(how='any', axis='rows')
	                    .drop_duplicates('player_id', keep='first'))
	lineup = lineup.merge(player_positions, how='left', on='player_id')

	# add on the position abbreviation
	formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
	                  8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
	                  14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
	                  20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}
	lineup['position_abbreviation'] = lineup.position_id.map(formation_dict)

	# sort the dataframe so the players are
	# in the order of their position (if started), otherwise in the order they came on
	lineup['start'] = lineup.player_id.isin(starting_players)
	lineup.sort_values(['team_name', 'start', 'on', 'position_id'],
	                   ascending=[True, False, True, True], inplace=True)

	##############################################################################
	# Filter the lineup/ events to one team and exclude some set pieces

	# filter the lineup for Barcelona players
	# if you want the other team set team = team2
	# Barcelona (team1), Deportivo AlavÃ©s (team2)
	team = team1
	other_team=team2
	lineup_team = lineup[lineup.team_name == team].copy()

	# filter the events to exclude some set pieces
	set_pieces = ['Throw-in', 'Free Kick', 'Corner', 'Kick Off', 'Goal Kick']
	# for the team pass map
	pass_receipts = events[(events.team_name == team) & (
	    events.type_name == 'Ball Receipt')].copy()
	# for the player pass maps
	passes_excl_throw = events[(events.team_name == team) & (events.type_name == 'Pass') &
	                           (events.sub_type_name != 'Throw-in')].copy()

	# identify how many players played and how many subs were used
	# we will use this in the loop for only plotting pass maps for as
	# many players who played
	num_players = len(lineup_team)
	num_sub = num_players - 11

	##############################################################################
	# Setup the pitch, arrows, and get some images

	# add padding to the top so we can plot the titles, and raise the pitch lines
	pitch = Pitch(pad_top=10, line_zorder=2, pitch_color="#111111",)

	# arrow properties for the sub on/off
	green_arrow = dict(arrowstyle='simple, head_width=0.7',
	                   connectionstyle="arc3,rad=-0.8", fc="green", ec="green")
	red_arrow = dict(arrowstyle='simple, head_width=0.7',
	                 connectionstyle="arc3,rad=-0.8", fc="red", ec="red")

	# a fontmanager object for using a google font
	fm_scada = FontManager('https://raw.githubusercontent.com/googlefonts/scada/main/fonts/ttf/'
	                       'Scada-Regular.ttf')

	# Load the Club/ Statsbomb logos
	# these are the property of the respective clubs/ StatsBomb.

	SB_LOGO_URL = ('https://raw.githubusercontent.com/statsbomb/open-data/'
	               'master/img/SB%20-%20Icon%20Lockup%20-%20Colour%20positive.png')
	barca_logo = Image.open("D:/Github Repos/Football_Templates/mex_logo.png")
	deportivo_logo = Image.open("D:/Github Repos/Football_Templates/arg_logo.png")
	sb_logo = Image.open(urlopen(SB_LOGO_URL))

	##############################################################################
	# Plotting the Pass Maps

	# filtering out some highlight_text warnings - the warnings aren't correct as the
	# text fits inside the axes.
	warnings.simplefilter("ignore", UserWarning)

	# plot the 5 * 3 grid
	fig, axs = pitch.grid(nrows=5, ncols=4, figheight=30,
	                      endnote_height=0.03, endnote_space=0,
	                      # Turn off the endnote/title axis. I usually do this after
	                      # I am happy with the chart layout and text placement
	                      axis=False,
	                      title_height=0.08, grid_height=0.84)
	fig.patch.set_facecolor('#000000')
	# cycle through the grid axes and plot the player pass maps
	for idx, ax in enumerate(axs['pitch'].flat):
	    # only plot the pass maps up to the total number of players
	    if idx < num_players:
	        # filter the complete/incomplete passes for each player (excudes throw-ins)
	        lineup_player = lineup_team.iloc[idx]
	        player_id = lineup_player.player_id
	        player_pass = passes_excl_throw[passes_excl_throw.player_id == player_id]
	        complete_pass = player_pass[player_pass.outcome_name.isnull()]
	        incomplete_pass = player_pass[player_pass.outcome_name.notnull()]

	        # plot the arrows
	        pitch.arrows(complete_pass.x, complete_pass.y,
	                     complete_pass.end_x, complete_pass.end_y,
	                     color='#56ae6c', width=2, headwidth=4, headlength=6, ax=ax)
	        pitch.arrows(incomplete_pass.x, incomplete_pass.y,
	                     incomplete_pass.end_x, incomplete_pass.end_y,
	                     color='#7065bb', width=2, headwidth=4, headlength=6, ax=ax)

	        # plot the title for each player axis
	        # here we use f-strings to combine the variables from the dataframe and text
	        # we plot the title at x=0, y=-5
	        # this is the left hand-side of the pitch (x=0) and between
	        # top of the y-axis (y=0) and the top of the padding (y=-10, remember pad_top = 10)
	        # note that the StatsBomb y-axis is inverted, so you may need
	        # to change this if you use another pitch_type (e.g. 'uefa').
	        # We also use the highlight-text package to highlight complete_pass green
	        # so put <> around the number of completed passes.
	        total_pass = len(complete_pass) + len(incomplete_pass)
	        annotation_string = (f'{lineup_player.position_abbreviation} | '
	                             f'{lineup_player.player_name} | '
	                             f'<{len(complete_pass)}>/{total_pass} | '
	                             f'{round(100 * len(complete_pass) / total_pass, 1) if total_pass != 0 else 0}%')
	        ax_text(0, -5, annotation_string, ha='left', va='center', fontsize=13,color="#ffffff",
	                fontproperties=fm_scada.prop,  # using the fontmanager for the google font
	                highlight_textprops=[{"color": '#ffffff'}], ax=ax)

	        # add information for subsitutions on/off and arrows
	        if not np.isnan(lineup_team.iloc[idx].off):
	            ax.text(116, -10, str(lineup_team.iloc[idx].off.astype(int)), fontsize=20,
	                    fontproperties=fm_scada.prop,
	                    ha='center', va='center')
	            ax.annotate('', (120, -2), (112, -2), arrowprops=red_arrow)
	        if not np.isnan(lineup_team.iloc[idx].on):
	            ax.text(104, -10, str(lineup_team.iloc[idx].on.astype(int)), fontsize=20,
	                    fontproperties=fm_scada.prop,
	                    ha='center', va='center')
	            ax.annotate('', (108, -2), (100, -2), arrowprops=green_arrow)

	# plot on the last Pass Map
	# (note ax=ax as we have cycled through to the last axes in the loop)
	pitch.kdeplot(x=pass_receipts.x, y=pass_receipts.y, ax=ax,
	              cmap=cmr.lavender,
	              levels=100,
	              thresh=0, fill=True)
	ax.text(0, -5, f'{team}: Pass Receipt Heatmap', ha='left', va='center', color="#ffffff",
	        fontsize=20, fontproperties=fm_scada.prop)

	# remove unused axes (if any)
	for ax in axs['pitch'].flat[11 + num_sub:-1]:
	    ax.remove()

	# endnote text
	axs['endnote'].text(0, 0.5, ' @rogergelioo',color="#ffffff",
	                    fontsize=20, fontproperties=fm_scada.prop, va='center', ha='left')
	# to get the left position to align with the pitches I plotted it once with a random
	# left position (e.g. 0.5) and then used the following code
	# bbox_sb = ax_sb_logo.get_position()
	# bbox_endnote = axs['endnote'].get_position()
	# left = bbox_endnote.x1 - bbox_sb.width
	ax_sb_logo = add_image(sb_logo, fig, left=0.701126,
	                       # set the bottom and height to align with the endnote
	                       bottom=axs['endnote'].get_position().y0,
	                       height=axs['endnote'].get_position().height)

	# title text
	axs['title'].text(0.5, 0.65, f'{team} Pass Maps vs {other_team}', fontsize=40,color="#ffffff",
	                  fontproperties=fm_scada.prop, va='center', ha='center')
	SUB_TEXT = ('Player Pass Maps: exclude throw-ins only/n'
	            'Team heatmap: includes all attempted pass receipts')
	axs['title'].text(0.5, 0.35, SUB_TEXT, fontsize=20, color="#ffffff",
	                  fontproperties=fm_scada.prop, va='center', ha='center')
	# plot logos (same height as the title_ax)
	# set the barca logo to align with the left/bottom of the title axes
	ax_barca_logo = add_image(barca_logo, fig,
	                          left=axs['title'].get_position().x0,
	                          bottom=axs['title'].get_position().y0,
	                          height=axs['title'].get_position().height)
	# set the deportivo logo to align with the right/bottom of the title axes
	# to get the left position to align with the pitches I plotted it once with a random
	# left position (e.g. 0.5) and then used the following code
	# bbox_logo = ax_deportivo_logo.get_position()
	# bbox_title = axs['title'].get_position()
	# left = bbox_title.x1 - bbox_logo.width
	ax_deportivo_logo = add_image(deportivo_logo, fig, left=0.8521,
	                              bottom=axs['title'].get_position().y0,
	                              height=axs['title'].get_position().height)
	# setting this example to the gallery thumbnail
	# sphinx_gallery_thumbnail_path = 'gallery/pitch_plots/images/sphx_glr_plot_grid_005'
	plt.savefig(f'{team1} - {axs["title"]}.jpg', format='jpeg')
	plt.show()  # If you are using a Jupyter notebook you do not need this line

def draw_passgrid(events, related, freeze, players, TEAM, FORMATION, OPPONENT, home_color):
	events.loc[events.tactics_formation.notnull(), 'tactics_id'] = events.loc[
	    events.tactics_formation.notnull(), 'id']
	events[['tactics_id', 'tactics_formation']] = events.groupby('team_name')[[
	    'tactics_id', 'tactics_formation']].ffill()

	formation_dict = {1: 'GK', 2: 'RB', 3: 'RCB', 4: 'CB', 5: 'LCB', 6: 'LB', 7: 'RWB',
	                  8: 'LWB', 9: 'RDM', 10: 'CDM', 11: 'LDM', 12: 'RM', 13: 'RCM',
	                  14: 'CM', 15: 'LCM', 16: 'LM', 17: 'RW', 18: 'RAM', 19: 'CAM',
	                  20: 'LAM', 21: 'LW', 22: 'RCF', 23: 'ST', 24: 'LCF', 25: 'SS'}
	players['position_abbreviation'] = players.position_id.map(formation_dict)

	sub = events.loc[events.type_name == 'Substitution',
	                 ['tactics_id', 'player_id', 'substitution_replacement_id',
	                  'substitution_replacement_name']]
	players_sub = players.merge(sub.rename({'tactics_id': 'id'}, axis='columns'),
	                            on=['id', 'player_id'], how='inner', validate='1:1')
	players_sub = (players_sub[['id', 'substitution_replacement_id', 'position_abbreviation']]
	               .rename({'substitution_replacement_id': 'player_id'}, axis='columns'))
	players = pd.concat([players, players_sub])
	players.rename({'id': 'tactics_id'}, axis='columns', inplace=True)
	players = players[['tactics_id', 'player_id', 'position_abbreviation']]

	# add on the position the player was playing in the formation to the events dataframe
	events = events.merge(players, on=['tactics_id', 'player_id'], how='left', validate='m:1')
	# add on the position the receipient was playing in the formation to the events dataframe
	events = events.merge(players.rename({'player_id': 'pass_recipient_id'},
	                                     axis='columns'), on=['tactics_id', 'pass_recipient_id'],
	                      how='left', validate='m:1', suffixes=['', '_receipt'])

	events.groupby('team_name').tactics_formation.unique()

	pass_cols = ['id', 'position_abbreviation', 'position_abbreviation_receipt']
	passes_formation = events.loc[(events.team_name == TEAM) & (events.type_name == 'Pass') &
	                              (events.tactics_formation == FORMATION) &
	                              (events.position_abbreviation_receipt.notnull()), pass_cols].copy()
	location_cols = ['position_abbreviation', 'x', 'y']
	location_formation = events.loc[(events.team_name == TEAM) &
	                                (events.type_name.isin(['Pass', 'Ball Receipt'])) &
	                                (events.tactics_formation == FORMATION), location_cols].copy()

	# average locations
	average_locs_and_count = (location_formation.groupby('position_abbreviation')
	                          .agg({'x': ['mean'], 'y': ['mean', 'count']}))
	average_locs_and_count.columns = ['x', 'y', 'count']

	# calculate the number of passes between each position (using min/ max so we get passes both ways)
	passes_formation['pos_max'] = (passes_formation[['position_abbreviation',
	                                                'position_abbreviation_receipt']]
	                               .max(axis='columns'))
	passes_formation['pos_min'] = (passes_formation[['position_abbreviation',
	                                                'position_abbreviation_receipt']]
	                               .min(axis='columns'))
	passes_between = passes_formation.groupby(['pos_min', 'pos_max']).id.count().reset_index()
	passes_between.rename({'id': 'pass_count'}, axis='columns', inplace=True)

	# add on the location of each player so we have the start and end positions of the lines
	passes_between = passes_between.merge(average_locs_and_count, left_on='pos_min', right_index=True)
	passes_between = passes_between.merge(average_locs_and_count, left_on='pos_max', right_index=True,
	                                      suffixes=['', '_end'])

	MAX_LINE_WIDTH = 18
	MAX_MARKER_SIZE = 3000
	passes_between['width'] = (passes_between.pass_count / passes_between.pass_count.max() *
	                           MAX_LINE_WIDTH)
	average_locs_and_count['marker_size'] = (average_locs_and_count['count']
	                                         / average_locs_and_count['count'].max() * MAX_MARKER_SIZE)

	MIN_TRANSPARENCY = 0.3
	color = np.array(to_rgba('white'))
	color = np.tile(color, (len(passes_between), 1))
	c_transparency = passes_between.pass_count / passes_between.pass_count.max()
	c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
	color[:, 3] = c_transparency

	pitch = Pitch(pitch_type='statsbomb', pitch_color='#111111', line_color='#c7d5cc')
	fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0,
	                      # Turn off the endnote/title axis. I usually do this after
	                      # I am happy with the chart layout and text placement
	                      axis=False,
	                      title_space=0, grid_height=0.82, endnote_height=0.05)
	fig.set_facecolor("#111111")
	pass_lines = pitch.lines(passes_between.x, passes_between.y,
	                         passes_between.x_end, passes_between.y_end, lw=passes_between.width,
	                         color=color, zorder=1, ax=axs['pitch'])
	pass_nodes = pitch.scatter(average_locs_and_count.x, average_locs_and_count.y,
	                           s=average_locs_and_count.marker_size,
	                           color=home_color, edgecolors='black', linewidth=1, alpha=1, ax=axs['pitch'])
	for index, row in average_locs_and_count.iterrows():
	    pitch.annotate(row.name, xy=(row.x, row.y), c='#111111', va='center',
	                   ha='center', size=16,  ax=axs['pitch'])

	# Load a custom font.
	URL = 'https://raw.githubusercontent.com/google/fonts/main/apache/roboto/Roboto%5Bwdth,wght%5D.ttf'
	robotto_regular = FontManager(URL)

	# endnote /title
	axs['endnote'].text(1, 0.5, '@rogergelioo', color='white',
	                    va='center', ha='right', fontsize=15,
	                    fontproperties=robotto_regular.prop)
	TITLE_TEXT = f'{TEAM}, {FORMATION} formation'
	axs['title'].text(0.5, 0.7, TITLE_TEXT, color='white',
	                  va='center', ha='center', fontproperties=robotto_regular.prop, fontsize=30)
	axs['title'].text(0.5, 0.25, f'vs {OPPONENT}', color='white',
	                  va='center', ha='center', fontproperties=robotto_regular.prop, fontsize=18)
	plt.savefig(f'{TEAM} passgrid.jpg', format='jpeg')
	plt.show()  # If you are using a Jupyter notebook you do not need this line

