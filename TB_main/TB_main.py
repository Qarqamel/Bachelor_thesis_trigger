from my_serial import my_serial,read,read_byte,writeln
import shutil, os, random, threading
from subprocess import call
from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate
from tqdm import tqdm

def Signal_processing_task():
    call(['python', 'Image_processing.py'])

PERIOD_GEN_COM_NR = 3
PULSE_GEN_COM_NR = 7
CAMERA_COM_NR = 19
SIG_PROC_COM_NR = 5

#[ms]
GENERATOR_PERIOD = 1

PULSES_NR = 10

#[ms]
FIRST_PULSE = 10
PULSE_WIDTH = 10
PULSE_MIN_PER = 10
PULSE_MAX_PER = 100

PULSES_LIST = []
recent_pulse_end = FIRST_PULSE
for i in range(PULSES_NR):
    pulse_start = recent_pulse_end + random.randrange(PULSE_MIN_PER, PULSE_MAX_PER, 1)
    pulse_width = PULSE_WIDTH
    PULSES_LIST.append([pulse_start, pulse_width])
    recent_pulse_end = pulse_start+pulse_width
SAMPLES_NR = sum(PULSES_LIST[-1])

PULSES_STRING = '\n'.join(np.array(PULSES_LIST).flatten().astype(str))

print(PULSES_LIST)
print(PULSES_STRING)
with my_serial(SIG_PROC_COM_NR) as sr_sig_proc:
    with my_serial(PERIOD_GEN_COM_NR) as sr_period_gen:
        with my_serial(CAMERA_COM_NR) as sr_camera:           
            with my_serial(PULSE_GEN_COM_NR) as sr_pulse_gen:
                Signal_processing_thread =threading.Thread(target=Signal_processing_task)
                Signal_processing_thread.start()
                print("sr_period_gen:"+read(sr_period_gen))           
                print("sr_camera:"+read(sr_camera)) 
                print("sr_pulse_gen:"+read(sr_pulse_gen))
                print("sr_sig_proc:"+read(sr_sig_proc))                
                
                writeln(sr_pulse_gen, PULSES_STRING)
                
                print("sr_camera:"+read(sr_camera)) 
                print("sr_pulse_gen:"+read(sr_pulse_gen))
                print("sr_sig_proc:"+read(sr_sig_proc))
                writeln(sr_period_gen, str(GENERATOR_PERIOD))
                print("sr_period_gen:"+read(sr_period_gen))
                
                samples_received=[]
                for i in tqdm(range(SAMPLES_NR)):
                    byte_buff = int(read_byte(sr_camera))
                    samples_received.append([byte_buff&0b1, byte_buff>>1&0b1])
                             
Signal_processing_thread.join()

samples_received = np.array(samples_received)
samples_received = samples_received.astype(int) #konwertuje stringi na inty

samples_expected = np.zeros(SAMPLES_NR, dtype=bool)
for start, width in PULSES_LIST:
    samples_expected[start:start+width] = True

print(tabulate(zip(samples_received, samples_expected), headers=['samples_received', 'samples_expected']))

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')

fig, axs = plt.subplots(3)
axs[0].plot(samples_received[:,0], label='Measured Samples ch1')
axs[1].plot(samples_received[:,1], label='Measured Samples ch2')
axs[2].plot(samples_expected,'orange', label='Computed Samples')
# axs[2].plot(Error, 'r', label = 'Error')
fig.legend()
fig.savefig('Results/results', dpi = 250)