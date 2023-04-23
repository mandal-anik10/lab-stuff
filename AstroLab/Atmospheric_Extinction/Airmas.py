# Calculation Code:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from LocalModule.Curve_Fit import Linear_Fit
from tabulate import tabulate

df = pd.read_excel('Arcturus.xlsx')
print(tabulate(df, headers= df.keys(), tablefmt="github"))



Exp_date = '26th Feb, 23'
star = 'Arcturus'
Dec = 19 + 3/60 + 28/3600
Lat = 18.559
t_expo = 1

HA = np.array([])

for i in df['Hour Angle']:
    if i.hour <= 12:
        h = i.hour + i.minute/60 + i.second/3600
    else:
        h = 24 - (i.hour + i.minute/60 + i.second/3600)
    HA = np.append(HA, h * 15)

# converting values to radian

Dec = Dec * np.pi/180
Lat = Lat * np.pi/180
HA = HA * np.pi/180

Z_angle = np.arccos(np.sin(Lat) * np.sin(Dec) + np.cos(Lat) * np.cos(Dec) * np.cos(HA))
Z_angle*180/np.pi



def Flux2Mag(flux):
    m = -2.5 * np.log10(flux)
    return m



fig = plt.figure(figsize=(18, 9))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

sec_th = 1/ np.cos(Z_angle)

M_b = Flux2Mag(df['B_net'])
M_v = Flux2Mag(df['V_net'])

mb, cb = Linear_Fit(sec_th, M_b)
mv, cv = Linear_Fit(sec_th, M_v)

xx = np.linspace(1, 2, 100)
fb = mb*xx + cb
fv = mv*xx + cv

plt.suptitle(': Determination of Extinction Coefficient :\n Date : {}, Start Time :{}, Star :{}, Declination : {:.2f}$^\\circ$, Latitute : {:.2f}$^\\circ$'.format(Exp_date, '00:53:00', star, np.degrees(Dec), np.degrees(Lat)))

ax1.plot(sec_th, M_b, '.')
ax1.plot(xx, fb)
ax1.set_title('B Band: slope or $A_\lambda$ = {:.4f}'.format(mb))
ax1.set_xlabel('sec(Zenith Angle) [Airmass]')
ax1.set_ylabel('Apperent magnitude($m_\lambda$)')
ax1.grid()

ax2.plot(sec_th, M_v, '.')
ax2.plot(xx, fv)
ax2.set_title('V Band: slope or $A_\lambda$ = {:.4f}'.format(mv))
ax2.set_xlabel('sec(Zenith Angle) [Airmass]')
ax2.set_ylabel('Apperent magnitude ($m_\lambda$)')
ax2.grid()

plt.savefig('Atmos_extinction_arcturus.png')



calc_df = {'Zenith Angle (Degrees)': Z_angle * 180/np.pi, 'Magnitude in B Band' : M_b.values, 'Magnitude in V Band': M_v.values}
calc_df = pd.DataFrame(calc_df)
print(tabulate(calc_df, headers= calc_df.keys(), tablefmt="github"))




