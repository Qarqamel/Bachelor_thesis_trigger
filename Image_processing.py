from my_serial import my_serial,read_byte,writeln,read

TESTER_COM_NR = 14

sample_ctr = 0

with my_serial(TESTER_COM_NR) as sr_tester:
        # read(sr_tester)
        
        last_sample = 1
        
        while True:
            rcvd_byte = int(read_byte(sr_tester))&0b11
            curr_sample = rcvd_byte&0b01
            # stop_bit = rcvd_byte&0b10
            print(curr_sample)
            if(last_sample == 0 and curr_sample == 1):
                writeln(sr_tester, str(sample_ctr))
            last_sample = curr_sample
            sample_ctr += 1
