from my_serial import my_serial,read_byte,writeln,read

SAMPLE_CH_NR = 0
STOP_CH_NR = 1

INPUT_SAMPLES_COM_NR = 8
OUTPUT_TIMESTAMPS_COM_NR = 11
TB_MAIN_COM_NR = 6

sample_ctr = 0

with my_serial(TB_MAIN_COM_NR) as sr_tb:
    with my_serial(INPUT_SAMPLES_COM_NR) as sr_input:
        with  my_serial(OUTPUT_TIMESTAMPS_COM_NR) as sr_output:
            writeln(sr_tb, "Init")
            print("img_proc_input:"+read(sr_input))
            print("img_proc_output:"+read(sr_output))
            print("img_proc_input:"+read(sr_input))
            print("img_proc_output:"+read(sr_output))
            
            last_sample = 1
            stop_bit = 0
            writeln(sr_tb, "Started")
            
            while True:
                rcvd_byte = int(read_byte(sr_input))&((1<<SAMPLE_CH_NR)|(1<<STOP_CH_NR))
                curr_sample = rcvd_byte&(1<<SAMPLE_CH_NR)
                stop_bit = rcvd_byte&(1<<STOP_CH_NR)
                if(last_sample == 0 and curr_sample == 1):
                    writeln(sr_output, str(sample_ctr))
                last_sample = curr_sample
                sample_ctr += 1
                if(stop_bit==1):
                    break