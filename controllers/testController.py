import numpy as np
import pandas as pd

column_names = ['r', 'Ws', 'Hs', 'theta', 'phid', 'udz']
df = pd.read_table("data/outlet.txt", sep='\t', skiprows=9 , header=None,
                   names=column_names, dtype=float)

mdot = np.zeros(len(df['r']))

for i in range(2, len(df['r'])):
    mdot[i] = (2 * np.pi *
               ((df['r'].iloc[i])) / 100 *
               ((df['r'].iloc[i]) - (df['r'].iloc[i-1])) / 100 *
               (-1 * df['udz'].iloc[i]) *
               1200 *
               df['phid'].iloc[i] / 1E6)

total_flow_rate = sum(mdot)
print(total_flow_rate)