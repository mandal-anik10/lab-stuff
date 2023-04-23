# Calculation Code:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from tabulate import tabulate



df = pd.read_excel('Night_Sky.xlsx')
print(tabulate(df, headers= df.keys(), tablefmt="github"))


def SkyMeg(Sky_meg, Flux_star_sky, Flux_Sky):
    Sm = Sky_meg  + (-2.5 * np.log10(Flux_Sky/Flux_star_sky ))
    return Sm


# Given Parameters:
f = 2350 #mm
A = 1 #sq mm

Sm_v = SkyMeg(Sky_meg=df['Magnitude(V)'].values,
              Flux_star_sky=df['V_flux'].values,
              Flux_Sky=df['V_background'].values)
Sm_v_max = SkyMeg(Sky_meg=df['Magnitude(V)'].values,
                  Flux_star_sky=df['V_flux'].values + df['V_error'].values,
                  Flux_Sky=df['V_background'].values)
Sm_v_min = SkyMeg(Sky_meg=df['Magnitude(V)'].values,
                  Flux_star_sky=df['V_flux'].values - df['V_error'].values,
                  Flux_Sky=df['V_background'].values)

A1 = A * (206265/f)**2

Sm1_v = Sm_v + (-2.5 * np.log10(1/A1))
Sm1_v_max = Sm_v_max + (-2.5 * np.log10(1/A1))
Sm1_v_min = Sm_v_min + (-2.5 * np.log10(1/A1))


calc_df = {'Star': df['Star'], 'Sky Magnitude': Sm_v,
           'SkyMag_neg_err': Sm_v_min- Sm_v, 'SkyMag_pos_err': Sm_v_max- Sm_v,
           'Sky Magnitude per sq arc second' : Sm1_v,
           'SkyMag_psac_neg_err': Sm1_v_min- Sm1_v, 'SkyMag_psac_pos_err': Sm1_v_max- Sm1_v}
calc_df = pd.DataFrame(calc_df)
print(tabulate(calc_df, headers= calc_df.keys(), tablefmt="github"))


avg_sm = np.average(calc_df['Sky Magnitude'].values)
avg_sm_neg_err = np.average(calc_df['SkyMag_neg_err'].values)
avg_sm_pos_err = np.average(calc_df['SkyMag_pos_err'].values)
avg_sm1 = np.average(calc_df['Sky Magnitude per sq arc second'].values)
avg_sm1_neg_err = np.average(calc_df['SkyMag_psac_neg_err'].values)
avg_sm1_pos_err = np.average(calc_df['SkyMag_psac_pos_err'].values)

print('Average Sky Magnitude : {:.5f} [{:.2f},{:.2f}]'.format(avg_sm, avg_sm_neg_err, avg_sm_pos_err ))
print('Average Sky Magnitude per sq arc second : {:.5f} [{:.2f},{:.2f}] '.format(avg_sm1, avg_sm1_neg_err, avg_sm1_pos_err))
