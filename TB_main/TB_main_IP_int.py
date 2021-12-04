import shutil, os, random, threading, sys, pickle
from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate
import pandas as pd
sys.path.append('../')
from my_serial import my_serial,read,read_byte,writeln

def Find_Edges(samples_list):
    edges_ind_list = []
    last_samp = 1
    for n, s in enumerate(samples_list):
        if(last_samp == 0 and s == 1):
            edges_ind_list.append(n)
        last_samp = s
    return edges_ind_list

Lock_IP_Ready = threading.Lock()
Lock_IP_Ready.acquire()

Lock_IP_Start = threading.Lock()
Lock_IP_Start.acquire()

IP_DELAY = 2000

def TB_main():
    CAMERA_CH0_BIT = 0
    CAMERA_CH1_BIT = 1
    
    PULSE_GEN_COM_NR = 19
    CAMERA_COM_NR = 23
    
    #[ms]
    # GENERATOR_PERIOD = 1
    SELECTOR_PULSE_WIDTH = 10
    
    PULSES_NR = 10
    
    #[ms]
    FIRST_PULSE = 10
    PULSE_MIN_WIDTH = 50
    PULSE_MAX_WIDTH = 70
    PULSE_MIN_PER = 100
    PULSE_MAX_PER = 150
    
    PULSES_LIST = []
    recent_pulse_end = FIRST_PULSE
    for i in range(PULSES_NR):
        pulse_start = recent_pulse_end + random.randrange(PULSE_MIN_PER, PULSE_MAX_PER, 1)
        pulse_width = random.randrange(PULSE_MIN_WIDTH, PULSE_MAX_WIDTH, 1)
        PULSES_LIST.append([pulse_start, pulse_width])
        recent_pulse_end = pulse_start+pulse_width
    SAMPLES_NR = recent_pulse_end + IP_DELAY
    PULSES_STRING = '\n'.join(np.array(PULSES_LIST).flatten().astype(str))
    
    with my_serial(CAMERA_COM_NR) as sr_camera:           
        with my_serial(PULSE_GEN_COM_NR) as sr_pulse_gen:
            
            Lock_IP_Ready.acquire()
            print("TB: IP ready")                          
            print("TB: sr_camera:"+read(sr_camera).lstrip('0123'))                          
            
            print("TB: sr_pulse_gen:"+read(sr_pulse_gen))
            writeln(sr_pulse_gen, PULSES_STRING)                         
            print("TB: sr_pulse_gen:"+read(sr_pulse_gen))
            
            Lock_IP_Start.release()
            
            samples_received=[]
            for i in range(SAMPLES_NR):
                byte_buff = int(read_byte(sr_camera))
                samples_received.append([(byte_buff>>CAMERA_CH0_BIT)&1, (byte_buff>>CAMERA_CH1_BIT)&1])
            print('TB: All samples received')
    
    samples_received = np.array(samples_received)
    samples_received = samples_received.astype(int) #konwertuje stringi na inty
    
    samples_expected_ch0 = np.zeros(SAMPLES_NR, dtype=bool)    
    samples_expected_ch1 = np.zeros(SAMPLES_NR, dtype=bool)
    for start, width in PULSES_LIST:
        samples_expected_ch0[start+IP_DELAY:start+IP_DELAY+SELECTOR_PULSE_WIDTH] = True
        samples_expected_ch1[start:start+width] = True    
    
    df = pd.DataFrame()
    df['Received samples ch0'] = samples_received[:,0]
    df['Received samples ch1'] = samples_received[:,1]
    df['Expected samples ch0'] = samples_expected_ch0
    df['Expected samples ch1'] = samples_expected_ch1
            
    ch0_edges_indx_lst = Find_Edges(df['Received samples ch0'])
    ch1_edges_indx_lst = Find_Edges(df['Received samples ch1'])
    
    Delays = [i-j for i, j in zip(ch0_edges_indx_lst, ch1_edges_indx_lst)]    
    df = pd.concat([df, pd.DataFrame({'Delays':Delays})], axis=1)
    result = tabulate(df,df.columns)
    # print(result)
    
    shutil.rmtree('Results', ignore_errors=True)
    os.mkdir('Results')
    
    fig, axs = plt.subplots(4)
    axs[0].plot(samples_received[:,0], label='Measured Samples ch0')
    axs[1].plot(samples_expected_ch0,'green', label='Computed Samples ch0')
    axs[2].plot(samples_received[:,1],'orange', label='Measured Samples ch1')
    axs[3].plot(samples_expected_ch1,'red', label='Computed Samples ch1')
    fig.legend()
    fig.savefig('Results/results', dpi = 250)
    
    with open("Results/results.txt", "w") as f:
        f.write(result)
    
    with open("Results/results", "wb") as f:
        pickle.dump(df, f)
        
def Image_processing():
    print("IP: Created")
    
    SAMPLE_CH_NR = 0
    STOP_CH_NR = 1
    
    INPUT_SAMPLES_COM_NR = 7
    OUTPUT_TIMESTAMPS_COM_NR = 11
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
                    curr_sample = rcvd_byte&(1<<SAMPLE_CH_NR)
                    stop_bit = rcvd_byte&(1<<STOP_CH_NR)
                    if(last_sample == 0 and curr_sample == 1):
                        writeln(sr_output, str(sample_ctr + IP_DELAY))
                    last_sample = curr_sample
                    sample_ctr += 1
                    if(stop_bit==(1<<STOP_CH_NR)):
                        break
                    
IP_Thread = threading.Thread(target = Image_processing)
TB_main_Thread = threading.Thread(target = TB_main)

IP_Thread.start()
TB_main_Thread.start()
IP_Thread.join()
TB_main_Thread.join()