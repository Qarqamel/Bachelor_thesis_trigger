SAMPLE_NR = 2900
METER_UNIT_IN_US = 0.0625

METER_COM_NR = 47
REGENERATOR_COM_NR = 36
GENERATOR_COM_NR = 6

GENERATOR_PERIODS_LIST = [4,10,40]


from tabulate import tabulate
import shutil, os, sys, pickle
import pandas as pd
sys.path.append('../')
from my_serial import my_serial,read,writeln

with my_serial(METER_COM_NR) as sr_meter:
    with my_serial(REGENERATOR_COM_NR) as sr_regenerator:
        with my_serial(GENERATOR_COM_NR) as sr_generator:
            print("sr_generator:"+read(sr_generator))
                
            print("sr_meter:"+read(sr_meter))
            print("sr_regenerator:"+read(sr_regenerator))
            for i in GENERATOR_PERIODS_LIST:
                writeln(sr_generator, str(i))
            print("sr_generator:"+read(sr_generator))
    
            writeln(sr_meter, 'start')
    
            df = pd.DataFrame()
            df['Measured Period'] = [int(read(sr_meter))for i in range(SAMPLE_NR)]
    
# df['Measured Period [us]'] = round(df['Measured period']*METER_UNIT_IN_US, 3)
df['Measured Period [us]'] = df['Measured Period']*METER_UNIT_IN_US
df.drop(columns=['Measured Period'], inplace=True)

result = tabulate(df, df.columns)
print(result)

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')

with open("Results/results.txt", 'w') as f:
    f.write(result)
with open("Results/results", "wb") as f:
    pickle.dump(result, f)