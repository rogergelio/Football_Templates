# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 13:52:43 2023

@author: rogel
"""
import numpy as np
#[num of shots, tot xg]
mci=[21,2.31]
tot=[21,2.00]


def game_sim(a,b):
	#Calc xg per shot
	a_xgps=a[1]/a[0]
	b_xgps=tot[1]/tot[0]
	a_xg=np.random.binomial(a[0],a_xgps)
	b_xg=np.random.binomial(b[0],b_xgps)
	if a_xg>b_xg:
		a_pts=3
		b_pts=0
	elif a_xg<b_xg:
		a_pts=0
		b_pts=3
	else:
		a_pts=1
		b_pts=1
	return [a_pts, b_pts]

def x_pts(a,b,sims):
	a_results=[]
	b_results=[]
	for i in np.arange(sims):
		sim_results=game_sim(a, b)
		a_results.append(sim_results[0])
		b_results.append(sim_results[1])
	a_xpoints=np.mean(a_results)
	b_xpoints=np.mean(b_results)
	return([a_xpoints, b_xpoints])

res=x_pts(mci,tot,20000)
	