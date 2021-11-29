import shutil, os, random, threading, sys
from subprocess import call
from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate
from tqdm import tqdm
sys.path.append('../')
from my_serial import my_serial,read,read_byte,writeln

def Signal_processing_task():
    call(['python', '..\Image_processing.py'])

CAMERA_CH1_BIT = 0
CAMERA_CH2_BIT = 1

PERIOD_GEN_COM_NR = 3
PULSE_GEN_COM_NR = 7
CAMERA_COM_NR = 19
SIG_PROC_COM_NR = 5

#[ms]
GENERATOR_PERIOD = 1
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
SAMPLES_NR = recent_pulse_end

PULSES_STRING = '\n'.join(np.array(PULSES_LIST).flatten().astype(str))

# print(PULSES_LIST)
# print(PULSES_STRING)

with my_serial(SIG_PROC_COM_NR) as sr_sig_proc:
    with my_serial(PERIOD_GEN_COM_NR) as sr_period_gen:
        with my_serial(CAMERA_COM_NR) as sr_camera:           
            with my_serial(PULSE_GEN_COM_NR) as sr_pulse_gen:
                Signal_processing_thread =threading.Thread(target=Signal_processing_task)
                Signal_processing_thread.start()
                print("sr_period_gen:"+read(sr_period_gen))
                print("sr_pulse_gen:"+read(sr_pulse_gen))                
                
                writeln(sr_pulse_gen, PULSES_STRING)
                
                print("sr_camera:"+read(sr_camera).lstrip('0')) 
                print("sr_pulse_gen:"+read(sr_pulse_gen))
                print("sr_sig_proc:"+read(sr_sig_proc))
                writeln(sr_period_gen, str(GENERATOR_PERIOD))
                print("sr_period_gen:"+read(sr_period_gen))
                
                samples_received=[]
                for i in range(SAMPLES_NR):
                    byte_buff = int(read_byte(sr_camera))
                    samples_received.append([(byte_buff>>CAMERA_CH1_BIT)&1, (byte_buff>>CAMERA_CH2_BIT)&1])
                print('All samples received')
                             
Signal_processing_thread.join()

samples_received = np.array(samples_received)
samples_received = samples_received.astype(int) #konwertuje stringi na inty

samples_expected_ch1 = np.zeros(SAMPLES_NR, dtype=bool)    
samples_expected_ch2 = np.zeros(SAMPLES_NR, dtype=bool)
for start, width in PULSES_LIST:
    samples_expected_ch1[start:start+SELECTOR_PULSE_WIDTH] = True
    samples_expected_ch2[start:start+width] = True    

#print(tabulate(zip(samples_received, samples_expected_ch2), headers=['samples_received', 'samples_expected']))

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')

fig, axs = plt.subplots(4)
axs[0].plot(samples_received[:,0], label='Measured Samples ch1')
axs[1].plot(samples_expected_ch1,'green', label='Computed Samples ch1')
axs[2].plot(samples_received[:,1],'orange', label='Measured Samples ch2')
axs[3].plot(samples_expected_ch2,'red', label='Computed Samples ch2')
fig.legend()
fig.savefig('Results/results', dpi = 250)