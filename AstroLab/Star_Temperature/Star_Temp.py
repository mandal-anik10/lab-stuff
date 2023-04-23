# Calculation Code:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate



# Reading Data File
df_new = pd.read_excel(r'/home/mandal-anik/Desktop/Sem-4/Astrolab/Star.xlsx')
print(tabulate(df_new, headers= df_new.keys(), tablefmt="github"))



def Color_Index(data):
    ci = np.array(-2.5 * np.log10((data["B_net"])/(data["V_net"])))
    ci_high = np.array(-2.5 * np.log10((data["B_net"]-data["B_error"])/(data["V_net"]+data["V_error"])))
    ci_low = np.array(-2.5 * np.log10((data["B_net"]+data["B_error"])/(data["V_net"]-data["V_error"])))
    return [ci, ci_high, ci_low]



ci, ci_high, ci_low = Color_Index(df_new)
ci_highError = ci_high - ci
ci_lowError = ci_low - ci



for i in range(len(df_new['Star'])):
    ist = "IST {}".format(df_new['Time(IST)'][i])
    a = "Color index of {:}\t\t".format(df_new['Star'][i])
    err = [float('{:.4f}'.format(ci_lowError[i])), float('{:.4f}'.format(ci_highError[i]))]
    print(ist, a, '{:.2f}'.format(ci[i]), err)

    
def ColIdx_to_temp(col_idx):
    # t = 4600*(1/(0.92*col_idx + 1.7) + 1/(0.92*col_idx + 0.62))    # Another relation that we can use
    t = 7000 * (1/(col_idx + 0.56))
    return t    
    
    

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111)

ci_i = np.linspace(-0.10, 1.5, 1000)
T_i = ColIdx_to_temp(ci_i)
    

T = ColIdx_to_temp(ci)
T_low = T - ColIdx_to_temp(ci + ci_highError)
T_high = ColIdx_to_temp(ci + ci_lowError) - T
ci_err = [-ci_lowError, ci_highError]
T_err = [T_low, T_high]
ax.errorbar(x=ci, y=T, xerr=ci_err, yerr= T_err, fmt='.', ecolor = 'red')


for i in range(len(ci)):
    Ti = ColIdx_to_temp(ci[i])
    ax.scatter(ci[i], Ti, label= str(df_new['Star'][i]))
               

ax.plot(ci_i, T_i)
ax.set_title("Temperature vs Color Index plot")
ax.set_ylabel("Temperature(K)")
ax.set_xlabel("Color Index (B-V)")
ax.grid()
ax.legend()

plt.savefig(r"/home/mandal-anik/Desktop/Sem-4/Astrolab/Star_Temp/ColIdvsTemp.png")
   
    
    
# print("Starting Date of Experiment:", Date, '\n')
for i in range(len(T)):
    ist = "IST {}".format(df_new['Time(IST)'][i])
    a = "Surface Tempurature of {:}\t\t".format(df_new['Star'][i])
    err = [float('{:.2f}'.format(-T_low[i])), float('{:.2f}'.format(T_high[i]))]
    print(ist, a, '{:.2f}'.format(T[i]), err, 'K')    
    
    
    
    
# Exact median values taken from Google
T_exact = [11668, 8500, 4470, 8296, 4500, 9355, 4290, 22400, 6100, 15540]

rel_err = abs(T- T_exact)*100/ T_exact 
rel_err    
    
