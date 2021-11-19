from my_serial import my_serial,read_byte,writeln,read

TESTER_COM_NR = 11

sample_ctr = 0

with my_serial(TESTER_COM_NR) as sr_tester:
        read(sr_tester)
        
        last_sample = 0
        
        while True:
            curr_sample = int(read_byte(sr_tester))&0b1
            if(last_sample == 0 and curr_sample == 1):
                writeln(sr_tester, str(sample_ctr))
            last_sample = curr_sample
            sample_ctr += 1