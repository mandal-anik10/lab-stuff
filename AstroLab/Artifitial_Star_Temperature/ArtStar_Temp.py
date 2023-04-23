# Calculation Code:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

# Write Data file:
df = pd.read_excel('ArtStar_Data.xlsx', )
print(tabulate(df, headers= df.keys(), tablefmt="github"))



def Color_Index(data):
    ci = np.array(-2.5 * np.log10(data["B_flux"]/data["V_flux"]))
    ci_high = np.array(-2.5 * np.log10((data["B_flux"]-data["B_error"])/(data["V_flux"]+data["V_error"])))
    ci_low = np.array(-2.5 * np.log10((data["B_flux"]+data["B_error"])/(data["V_flux"]-data["V_error"])))
    return [ci, ci_high, ci_low]



ci, ci_high, ci_low = Color_Index(df)
x = np.array([i for i in range(len(df['B_flux']))])



fig = plt.figure(figsize = (16, 6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.errorbar(df['V_flux'], df['B_flux'], xerr = df['V_error'], yerr = df['B_error'], fmt='.-', ecolor = 'red')
ax1.set_xlabel("V_flux")
ax1.set_ylabel("B_flux")
ax1.set_title("B_flux vs V_flux")
ax1.grid()

ax2.plot(x, ci, '-o', x,ci_low, '+--', x, ci_high, '^--')
ax2.set_title("Plt of color index per reading")
ax2.set_xlabel("Reading number")
ax2.set_ylabel("Color Index (B-V)")
ax2.legend(['Median values', 'Lower limit of error', 'Upper limit of error'])
plt.grid()



def ColIdx_to_temp(col_idx):
    # t = 4600*(1/(0.92*col_idx + 1.7) + 1/(0.92*col_idx + 0.62))    # Another relation that we can use
    t = 7000 * (1/(col_idx + 0.56))
    return t



T = ColIdx_to_temp(ci)
T_low = T - ColIdx_to_temp(ci_high)
T_high = ColIdx_to_temp(ci_low) - T

df_new = {'Color Index(CI)': ci, 'CI_neg_error': ci_low-ci, 'CI_pos_error': ci_high-ci,
         'Temperature(T) [K]': T, 'T_neg_error [K]': -T_low, 'T_pos_error [K]': T_high}
df_new = pd.DataFrame(df_new)
df_new.to_excel('Calculated_data.xlsx')
print(tabulate(df_new, headers= df_new.keys(), tablefmt="github"))



avg_ci =np.average(ci)
avg_ci_low = np.average(ci_low)
avg_ci_high = np.average(ci_high)

print("Avg. value of color index : \t", avg_ci)
print("Avg. lower err value of color index(-err) : \t", avg_ci_low- avg_ci)
print("Avg. upper err value of color index(+err) : \t", avg_ci_high-avg_ci)


fig = plt.figure(figsize=(16,9))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ci_i = np.linspace(0, 2.5, 1000)
T_i = ColIdx_to_temp(ci_i)

ci_err = [ci-ci_low, ci_high-ci]
T_err = [T_low, T_high]



ax1.errorbar(x=ci, y=T, xerr=ci_err, yerr=T_err, fmt='.', ecolor = 'red')
ax1.plot(ci_i, T_i)
ax1.set_title("Temperature vs Color Index plot")
ax1.set_ylabel("Temperature(K)")
ax1.set_xlabel("Color Index (B-V)")
ax1.grid()

ax2.errorbar(x=ci, y=T, xerr=ci_err, yerr= T_err, fmt='.', ecolor = 'red')
ax2.plot(ci_i, T_i)
ax2.set_title("Zoomed-In plot")
ax2.set_ylabel("Temperature(K)")
ax2.set_xlabel("Color Index (B-V)")
ax2.grid()
ax2.set_xlim([1.35, 1.6])
ax2.set_ylim([3200, 3650])
plt.savefig(r"/home/mandal-anik/Desktop/Sem-4/Astrolab/ArtStar_Temp/ColIdvsTemp.png")



Temp = ColIdx_to_temp(avg_ci)
Temp_low = ColIdx_to_temp(avg_ci_high) - Temp
Temp_high = ColIdx_to_temp(avg_ci_low ) - Temp

print("Avg. value of Temperature : \t", Temp)
print("Avg. lower err value of Temperature(-err) : \t", Temp_low)
print("Avg. upper err value of Temperature(+err) : \t", Temp_high)

