from my_serial import my_serial,read,writeln
import shutil, os
import pandas as pd
from tabulate import tabulate

TESTER_COM_NR = 13
GENERATOR_COM_NR = 7

PULSES_NR = 100

with my_serial(GENERATOR_COM_NR) as sr_generator:    
    with my_serial(TESTER_COM_NR) as sr_tester:        
        read(sr_tester)     
        read(sr_generator)
        
        writeln(sr_generator, '1')
        writeln(sr_tester, 'Start')
        
        writeln(sr_tester, 'Start_acquisition')
        
        delays = [int(read(sr_tester)) for i in range(PULSES_NR)]
                
df = pd.DataFrame()
df['Delays [ms]'] = delays

result = tabulate(df, df.columns)
print(result)
shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)
