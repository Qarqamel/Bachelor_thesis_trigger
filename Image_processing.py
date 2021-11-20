from my_serial import my_serial,read_byte,writeln,read
#import time

TESTER_COM_NR = 14

sample_ctr = 0

with my_serial(TESTER_COM_NR) as sr_tester:
        
    last_sample = 1
    stop_bit = 0
    
    while stop_bit==0:
        rcvd_byte = int(read_byte(sr_tester))&0b11
        curr_sample = rcvd_byte&0b01
        stop_bit = rcvd_byte&0b10
        print(rcvd_byte)
        if(last_sample == 0 and curr_sample == 1):
            #time.sleep(0.020)
            writeln(sr_tester, str(sample_ctr))
        last_sample = curr_sample
        sample_ctr += 1
