# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:18:03 2015

@author: ahaque
"""

from datetime import date, datetime
import time
import pandas as pd
import numpy as np
import google_analytics as ga

def isoDate():
    today = date.today()
    iso = date.isoformat(today)
    return iso
    
def human_datetime(z):
    z = z/1000
    g = time.localtime(z)
    
    year = str(g.tm_year)
    mon = "{:0>2d}".format(g.tm_mon)
    day = "{:0>2d}".format(g.tm_mday)

    return year+'-'+mon+'-'+day


df = pd.read_csv('posts_and_date.csv')
header = df.columns

df['human_datetime'] = df['n.dateAdded'].map(lambda x: human_datetime(x))

def freq_dict(phrases):
    words = [str(s) for s in phrases] 
    d = {w: 0 for w in words}
    for word in words:
        d[word] += 1
        
    return d
    
dateonly = np.array(df['human_datetime'])

freq_dates = freq_dict(dateonly)

filt_freq_dates ={i:freq_dates[i] for i in freq_dates if i>='2015-04-16'}

post_act = []
for f in filt_freq_dates:
    if(f>'2015-08-23'):
        countunique = ga.num_user_sessions(f, f)
        post_act.append([f, filt_freq_dates[f], countunique])
    else:
        countunique1 = ga.num_user_sessions2(f,f)
        post_act.append([f, filt_freq_dates[f], countunique])
    
df2 = pd.DataFrame(post_act, columns = ['Date', 'How many posts', 'Unique users'])

df2.to_csv('post_activity'+isoDate()+".csv")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    