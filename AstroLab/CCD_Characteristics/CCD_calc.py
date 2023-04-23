# Calculation Code:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

#=====|Data File for CCD Experiment|====================================================
#CCD temperature : 16.95℃,	Focus peak count = 54963,	Time : 150s	
#Pixel Coordinate : x = 400, y = 270
#6	566	596	555	548	559

df = pd.read_excel('Datafile.xlsx')
print(tabulate(df, headers= df.keys(), tablefmt="github"))



avg_count = []
sd_count = []
conversion_factor = []
q_eff = 0.6
actual_count = []
sum_f = 0

for key in ['Center(O)', 'Up(U)', 'Down(D)', 'Left(L)', 'Right(R)']:
    avg = np.average(df[key])
    sd = np.std(df[key])
    f = avg/sd**2
    f_actual = f/q_eff
    
    sum_f = sum_f + f_actual
    
    avg_count.append(avg)
    sd_count.append(sd)
    conversion_factor.append(f)
    actual_count.append(int(f_actual))

net_f = sum_f/5

calc_df = {'Pixel': ['Center(O)', 'Up(U)', 'Down(D)', 'Left(L)', 'Right(R)'],
           'Pixel Location': [(400,270), (400, 269), (400, 271), (399, 270), (301, 270)],
           'Average Count': avg_count, 'SD' : sd_count, 'Conversion Factor': conversion_factor, 
           'Quantum Efficiency': q_eff * np.ones(5), 'Actual conversion factor(Photon Count/ADU)': actual_count}

calc_df = pd.DataFrame(calc_df)
print('Average conversion factor (Photon counts per ADU) : ', int(net_f))
print(tabulate(calc_df, headers= calc_df.keys(), tablefmt="github"))

calc_df.to_excel('Calculated data.xlsx')
