SAMPLE_NR = 2900
METER_UNIT_IN_US = 0.0625
PERIOD_INPUT_US = 25

METER_COM_NR = 48

from my_serial import my_serial,read,writeln
from tabulate import tabulate
import shutil, os
import pandas as pd
from collections import Counter
import pickle

with my_serial(METER_COM_NR) as sr_meter:
    read(sr_meter)    
    
    writeln(sr_meter, 'start')
    
    df = pd.DataFrame()
    df['Measured Period'] = [int(read(sr_meter)) for i in range(SAMPLE_NR)]
    
df['Measured Period [us]'] = df['Measured Period']#*METER_UNIT_IN_US
df['Set Period [us]'] = PERIOD_INPUT_US
df['Error [%]'] = ((df['Set Period [us]'] - df['Measured Period [us]'])/df['Set Period [us]'])*100
df.drop(columns=['Measured Period'], inplace = True)              

result = tabulate(df, df.columns)
cnt_val = Counter(df['Measured Period [us]'])
cnt_val = list(map(list, cnt_val.items()))
cnt_val = tabulate(cnt_val, headers = ['period', 'nr'])             
print(result)
print(cnt_val)

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')                
with open("Results/results.txt", 'w') as f:
    f.write(result)
with open("Results/summary.txt", 'w') as f:
    f.write(cnt_val)
with open("Results/results", "wb") as f:
    pickle.dump(result, f)
        

