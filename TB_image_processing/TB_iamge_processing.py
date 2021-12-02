import shutil, os, time, random, threading, sys, pickle
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
from subprocess import Popen
sys.path.append('../')
from my_serial import my_serial,read,writeln

TESTER_COM_NR = 6

SAMPLE_CH_NR = 0
STOP_CH_NR = 1

PULSES_NR = 100

Img_proc_ready = threading.Event()
def Signal_processing_task():
    sig_proc_task = Popen(['python', '..\Image_processing.py'])
    sig_proc_task.wait()

Signal_processing_thread = threading.Thread(target=Signal_processing_task)
Signal_processing_thread.start()

time.sleep(10)

with my_serial(TESTER_COM_NR) as sr_tester:
    delays_recieved = []        
    for i in tqdm(range(PULSES_NR)):
        writeln(sr_tester, str(1<<SAMPLE_CH_NR))
        delays_recieved.append(int(read(sr_tester)))
        # time.sleep(0.1)
        time.sleep(random.randrange(1,5,1))
    writeln(sr_tester, str(1<<STOP_CH_NR))
Signal_processing_thread.join()

df = pd.DataFrame()
df['Delays [ms]'] = delays_recieved
result = tabulate(df, df.columns)
print(result)

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')
with open('Results/results.txt', 'w') as file:
    file.write(result)    
with open("Results/results", "wb") as f:
    pickle.dump(df, f)
