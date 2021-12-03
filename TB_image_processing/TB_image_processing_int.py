import shutil, os, time, random, threading, sys, pickle
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
sys.path.append('../')
from my_serial import my_serial,read,writeln,read_byte

Lock_IP_Ready = threading.Lock()
Lock_IP_Ready.acquire()

Lock_IP_Start = threading.Lock()
Lock_IP_Start.acquire()

def TB_image_processing():
    TESTER_COM_NR = 6

    SAMPLE_CH_NR = 0
    STOP_CH_NR = 1
    
    PULSES_NR = 100
    
    Lock_IP_Ready.acquire()
    print("TB: IP Ready")
            
    with my_serial(TESTER_COM_NR) as sr_tester:
        Lock_IP_Start.release()
        time.sleep(1)
        
        delays_recieved = []   
        for i in tqdm(range(PULSES_NR)):
            writeln(sr_tester, str(1<<SAMPLE_CH_NR))
            delays_recieved.append(int(read(sr_tester)))
            time.sleep(0.1)
            # time.sleep(random.randrange(1,5,1))
        writeln(sr_tester, str(1<<STOP_CH_NR))
    
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
        
def Image_processing():
    print("IP: Created")
    
    SAMPLE_CH_NR = 0
    STOP_CH_NR = 1
    
    INPUT_SAMPLES_COM_NR = 25
    OUTPUT_TIMESTAMPS_COM_NR = 8
    GENERATOR_COM_NR = 3
    
    sample_ctr = 0
    
    with  my_serial(OUTPUT_TIMESTAMPS_COM_NR) as sr_output:
        with my_serial(INPUT_SAMPLES_COM_NR) as sr_input:        
            with my_serial(GENERATOR_COM_NR) as sr_generator:                
                print("IP: sr_input:"+read(sr_input).lstrip('0123'))
                print("IP: sr_output:"+read(sr_output))
                print("IP: sr_generator:"+read(sr_generator))
                
                Lock_IP_Ready.release()
                Lock_IP_Start.acquire()
                print("IP: Started")
                                
                last_sample = 1
                stop_bit = 0
                writeln(sr_generator, "1")
                print("IP: sr_generator:"+read(sr_generator))
                
                while True:
                    rcvd_byte = int(read_byte(sr_input))&((1<<SAMPLE_CH_NR)|(1<<STOP_CH_NR))
                    # print(rcvd_byte)
                    curr_sample = rcvd_byte&(1<<SAMPLE_CH_NR)
                    stop_bit = rcvd_byte&(1<<STOP_CH_NR)
                    if(last_sample == 0 and curr_sample == 1):
                        writeln(sr_output, str(sample_ctr))
                    last_sample = curr_sample
                    sample_ctr += 1
                    if(stop_bit==(1<<STOP_CH_NR)):
                        break

IP_Thread = threading.Thread(target = Image_processing)
TB_IP_Thread = threading.Thread(target = TB_image_processing)

IP_Thread.start()
TB_IP_Thread.start()
IP_Thread.join()
TB_IP_Thread.join()