from my_serial import my_serial_9600,read_byte,writeln

TB_COM_NR = 6

sample_ctr = 0

with my_serial_9600(TB_COM_NR) as sr_tb:
    writeln(sr_tb, "Start")
    
    last_sample = 1
    
    while True:
        curr_sample = int(read_byte(sr_tb))&0b1
        if(last_sample == 0 and curr_sample == 1):
            writeln(sr_tb, str(sample_ctr))
        last_sample = curr_sample
        sample_ctr += 1
    

