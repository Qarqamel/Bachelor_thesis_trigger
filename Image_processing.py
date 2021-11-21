from my_serial import my_serial,read_byte,writeln,read
#import time

SAMPLE_CH_NR = 0
STOP_CH_NR = 1

TESTER_COM_NR = 14

sample_ctr = 0

with my_serial(TESTER_COM_NR) as sr_tester:
        
    last_sample = 1
    stop_bit = 0
    
    while True:
        rcvd_byte = int(read_byte(sr_tester))&((1<<SAMPLE_CH_NR)|(1<<STOP_CH_NR))
        curr_sample = rcvd_byte&(1<<SAMPLE_CH_NR)
        stop_bit = rcvd_byte&(1<<STOP_CH_NR)
        if(last_sample == 0 and curr_sample == 1):
            #time.sleep(0.020)
            writeln(sr_tester, str(sample_ctr))
        last_sample = curr_sample
        sample_ctr += 1
        if(stop_bit==1):
            break