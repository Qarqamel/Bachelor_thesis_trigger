from my_serial import my_serial,read_byte,writeln,read

SAMPLE_CH_NR = 0
STOP_CH_NR = 1

INPUT_SAMPLES_COM_NR = 7
OUTPUT_TIMESTAMPS_COM_NR = 11
GENERATOR_COM_NR = 3

sample_ctr = 0

with  my_serial(OUTPUT_TIMESTAMPS_COM_NR) as sr_output:
    with my_serial(INPUT_SAMPLES_COM_NR) as sr_input:        
        with my_serial(GENERATOR_COM_NR) as sr_generator:
            
            print("img_proc_input:"+read(sr_input))
            print("img_proc_output:"+read(sr_output))
            print("sr_generator:"+read(sr_generator))
                            
            last_sample = 1
            stop_bit = 0
            writeln(sr_generator, "1")
            print("sr_generator:"+read(sr_generator))
            
            while True:
                rcvd_byte = int(read_byte(sr_input))&((1<<SAMPLE_CH_NR)|(1<<STOP_CH_NR))
                curr_sample = rcvd_byte&(1<<SAMPLE_CH_NR)
                stop_bit = rcvd_byte&(1<<STOP_CH_NR)
                if(last_sample == 0 and curr_sample == 1):
                    writeln(sr_output, str(sample_ctr))
                last_sample = curr_sample
                sample_ctr += 1
                if(stop_bit==(1<<STOP_CH_NR)):
                    break