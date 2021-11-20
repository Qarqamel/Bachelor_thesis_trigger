from my_serial import my_serial,read,writeln,write
import shutil, os
import pandas as pd
from tabulate import tabulate

TESTER_COM_NR = 13
GENERATOR_COM_NR = 7

PULSES_NR = 100

with my_serial(TESTER_COM_NR) as sr_tester: 
    read(sr_tester)
    writeln(sr_tester, 'Start')

with my_serial(GENERATOR_COM_NR) as sr_generator:    
    with my_serial(TESTER_COM_NR) as sr_tester:        
        read(sr_tester)     
        read(sr_generator)
        
        writeln(sr_generator, '1')
        writeln(sr_tester, 'Start')
        
        delays = []
        timestamps = []
        for i in range(PULSES_NR):
            writeln(sr_tester, str(0b1))
            timestamps.append(int(read(sr_tester)))
            delays.append(int(read(sr_tester)))
        writeln(sr_tester, str(0b10))
                
df = pd.DataFrame()
df['Timestamps'] = timestamps
df['Delays [ms]'] = delays

result = tabulate(df, df.columns)
print(result)
shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)
