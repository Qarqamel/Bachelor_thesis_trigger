import shutil, os, time, random, threading, sys
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
from subprocess import call
sys.path.append('../')
from my_serial import my_serial,read,writeln

TESTER_COM_NR = 13
GENERATOR_COM_NR = 7

SAMPLE_CH_NR = 0
STOP_CH_NR = 1

PULSES_NR = 100

def Signal_processing_task():
    call(['python', 'Image_processing.py'])
    
Signal_processing_thread =threading.Thread(target=Signal_processing_task)
Signal_processing_thread.start()

with my_serial(TESTER_COM_NR) as sr_tester: 
    read(sr_tester)
    writeln(sr_tester, 'Start')

df = pd.DataFrame(columns=['Timestamps', 'Delays [ms]'])

with my_serial(GENERATOR_COM_NR) as sr_generator:    
    with my_serial(TESTER_COM_NR) as sr_tester:        
        print("sr_tester:"+read(sr_tester))     
        print("sr_generator"+read(sr_generator))
        
        print("sr_tester:"+read(sr_tester))        
        writeln(sr_generator, '1')
        print("sr_generator"+read(sr_generator))
        
        for i in tqdm(range(PULSES_NR)):
            writeln(sr_tester, str(1<<SAMPLE_CH_NR))
            new_row = {'Timestamps':int(read(sr_tester)), 'Delays [ms]':int(read(sr_tester))}
            df = df.append(new_row, ignore_index=True)
            time.sleep(random.randrange(0,5,1))
        writeln(sr_tester, str(1<<STOP_CH_NR))

Signal_processing_thread.join()
result = tabulate(df, df.columns)
print(result)
shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)
