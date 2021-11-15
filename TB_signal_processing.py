from my_serial import my_serial_9600,read,read_byte,writeln,write
import random, shutil, os
import pandas as pd
from tabulate import tabulate

SIG_PROC_COM_NR = 5

PULSES_NR = 10

FIRST_PULSE = 10
PULSE_WIDTH = 5
PULSE_MIN_PER = 5
PULSE_MAX_PER = 100

SAMPLES_NR = FIRST_PULSE + (PULSE_MAX_PER+PULSE_WIDTH)*PULSES_NR

SAMPLES_TO_SEND = [0]*SAMPLES_NR
EXPECTED_TIMESTAMPS = []
last_pulse_end = FIRST_PULSE
for i in range(PULSES_NR):
    start = last_pulse_end + random.randrange(PULSE_MIN_PER, PULSE_MAX_PER, 1)
    SAMPLES_TO_SEND[start:start+PULSE_WIDTH] = [1]*PULSE_WIDTH
    EXPECTED_TIMESTAMPS.append(start)
    last_pulse_end = start+PULSE_WIDTH

with my_serial_9600(SIG_PROC_COM_NR) as sr_sp:
    read(sr_sp)
    
    for i in SAMPLES_TO_SEND:
        write(sr_sp, str(i))
    
    rcvd_timestamps = []
    for i in range(PULSES_NR):
        rcvd_timestamps.append(int(read(sr_sp)))
        
    print(EXPECTED_TIMESTAMPS, rcvd_timestamps)
    
df = pd.DataFrame()
df['Expected Timestamps'] = EXPECTED_TIMESTAMPS
df['Received Timestamps'] = rcvd_timestamps
df['Error'] = df['Expected Timestamps'] - df['Received Timestamps']

result = tabulate(df, df.columns)
print(result)
shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)