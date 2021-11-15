from my_serial import my_serial_9600,read,write
import shutil, os, time
import pandas as pd
from tabulate import tabulate

SIG_PROC_COM_NR = 5

PULSES_NR = 10

PULSE_WIDTH = 5
PULSE_PER = 100

SAMPLES_NR = PULSE_PER + (PULSE_PER+PULSE_WIDTH)*PULSES_NR

SAMPLES_TO_SEND = [0]*SAMPLES_NR
end = PULSE_PER
for i in range(PULSES_NR):
    start = end + PULSE_PER
    end += PULSE_PER + PULSE_WIDTH
    SAMPLES_TO_SEND[start:end] = [1]*PULSE_WIDTH

with my_serial_9600(SIG_PROC_COM_NR) as sr_sp:
    read(sr_sp)
    
    timestamp_delays = []
    for i,j in zip(SAMPLES_TO_SEND, SAMPLES_TO_SEND[1:]):
        if(i==0 and j ==1):
            write(sr_sp, str(j))
            sent_time = time.time()
            read(sr_sp)
            rcvd_time = time.time()
            timestamp_delays.append(rcvd_time-sent_time)
        else:
            write(sr_sp, str(j))
        
df = pd.DataFrame()
df['Delays[s]'] = timestamp_delays
df['Delays[ms]'] = round(df['Delays[s]']*1000, 3)
df.drop(columns=['Delays[s]'], inplace = True)

result = tabulate(df, df.columns)
print(result)

# shutil.rmtree('Results', ignore_errors=True)
# os.mkdir('Results')
# with open('Results/results.txt', 'w') as file:
#     file.write(result)