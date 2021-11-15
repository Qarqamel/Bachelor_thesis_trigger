TIMESTAMPS_NR = 10
#trigger = 0.1mm
FIRST_TIMESTAMP = 1000 #in triggers (1s dla T_trigg=1ms)
TIMESTAMPS_STEP  = 50   # in trigers (50ms)

GENERATOR_COM_NR = 19
SELECTOR_COM_NR = 3
METER_COM_NR = 11

from my_serial import my_serial,read,writeln
from tabulate import tabulate
import random, shutil, os
import pandas as pd

TimestampsToSend_ms = [FIRST_TIMESTAMP]
recent_timestamp = FIRST_TIMESTAMP
for i in range(TIMESTAMPS_NR-1):
    timestamp = recent_timestamp+(random.randrange(1,10,1)*TIMESTAMPS_STEP)
    TimestampsToSend_ms.append(timestamp)
    recent_timestamp = timestamp

with my_serial(METER_COM_NR) as sr_meter:
    with my_serial(SELECTOR_COM_NR) as sr_selector:
        with my_serial(GENERATOR_COM_NR) as sr_generator:
            read(sr_meter)
            read(sr_selector)
            read(sr_generator)
            
            writeln(sr_generator, '1');
            writeln(sr_meter, 'Start');
            
            for i in TimestampsToSend_ms:
                writeln(sr_selector, str(i))                    
                
            TimestampsReceived_ms = [int(read(sr_meter)) for i in range(TIMESTAMPS_NR)]

df = pd.DataFrame() 
df['Timestamps Sent [ms]'] = TimestampsToSend_ms
df['Timestamps Received [ms]'] = TimestampsReceived_ms           
df['Error[1ms]'] = df['Timestamps Received [ms]']-df['Timestamps Sent [ms]']           

result = tabulate(df, df.columns)
print(result)
shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)
