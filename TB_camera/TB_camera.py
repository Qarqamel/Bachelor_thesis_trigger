from my_serial import my_serial,read,read_byte,writeln
import shutil, os, random
from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate

PERIOD_GEN_COM_NR = 19
PULSE_GEN_COM_NR = 3
CAMERA_COM_NR = 11

#[ms]
GENERATOR_PERIOD = 1

PULSES_NR = 10

#[ms]
FIRST_PULSE = 10
PULSE_WIDTH = 5
PULSE_MIN_PER = 5
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

with my_serial(PERIOD_GEN_COM_NR) as sr_period_gen:
    with my_serial(CAMERA_COM_NR) as sr_camera:           
        with my_serial(PULSE_GEN_COM_NR) as sr_pulse_gen:
            read(sr_period_gen)            
            read(sr_camera) 
            read(sr_pulse_gen)
            
            writeln(sr_period_gen, str(GENERATOR_PERIOD))
            writeln(sr_pulse_gen, PULSES_STRING)
            writeln(sr_camera, "Start")
                
            # samples_received = np.array([read_byte(sr_camera) for i in range(SAMPLES_NR)])
            samples_received=[]
            for i in range(SAMPLES_NR):
                byte_buff = int(read_byte(sr_camera))
                samples_received.append([byte_buff&0b1, byte_buff>>1&0b1])
            samples_received = np.array(samples_received)

samples_received = samples_received.astype(int) #konwertuje stringi na inty

samples_expected = np.zeros(SAMPLES_NR, dtype=bool)
for start, width in PULSES_LIST:
    samples_expected[start:start+width] = True

Error = samples_received[:,0] - samples_expected

print(tabulate(zip(samples_received, samples_expected, Error), headers=['samples_received', 'samples_expected', 'Error']))

shutil.rmtree('Results', ignore_errors=True)
os.mkdir('Results')

fig, axs = plt.subplots(3)
axs[0].plot(samples_received[:,0], label='Measured Samples')
axs[1].plot(samples_expected,'orange', label='Computed Samples')
axs[2].plot(Error, 'r', label = 'Error')
fig.legend()
fig.savefig('Results/results', dpi = 250)
