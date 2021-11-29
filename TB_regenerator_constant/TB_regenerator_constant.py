SAMPLE_NR = 2900
METER_UNIT_IN_US = 0.0625
SetPeriodIn_ms_l = [1, 2, 5, 10]
SetPeriodOut_us_l = [40, 1000, 100, 200]

GENERATOR_COM_NR = 6
REGENERATOR_COM_NR = 36
METER_COM_NR = 47


from tabulate import tabulate
import shutil, os, sys, pickle
import pandas as pd
sys.path.append('../')
from my_serial import my_serial,read,writeln

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')

with my_serial(GENERATOR_COM_NR) as sr_generator:
    with my_serial(REGENERATOR_COM_NR) as sr_regenerator:
        with my_serial(METER_COM_NR) as sr_meter:
            print("sr_generator:"+read(sr_generator))
                        
            print("sr_regenerator:"+read(sr_regenerator))
            print("sr_meter:"+read(sr_meter))

            for period_In, period_Out in zip(SetPeriodIn_ms_l, SetPeriodOut_us_l):
            
                writeln(sr_generator, str(period_In))
                print("sr_generator:"+read(sr_generator))
                writeln(sr_regenerator, str(period_Out))
                print("sr_regenerator:"+read(sr_regenerator))
                writeln(sr_meter, 'start')
                
                df = pd.DataFrame()
                df['Measured Period'] = [int(read(sr_meter)) for i in range(SAMPLE_NR)]
                
                #df['Measured Period [us]'] = round(df['Measured period']*METER_UNIT_IN_US, 3)
                df['Measured Period [us]'] = df['Measured Period']*METER_UNIT_IN_US
                df['Set Period [us]'] = period_Out
                df['Error [%]'] = ((df['Set Period [us]'] - df['Measured Period [us]'])/df['Set Period [us]'])*100
                df.drop(columns=['Measured Period'], inplace = True)              
                
                result = tabulate(df, df.columns)                
                print(result)                
                with open(f"Results/in={period_In}ms;out={period_Out}us.txt", 'w') as f:
                    f.write(result)
                with open(f"Results/in={period_In}ms;out={period_Out}us", "wb") as f:
                    pickle.dump(df, f)