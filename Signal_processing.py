from my_serial import my_serial,read_byte,writeln,read

CAMERA_COM_NR = 11
SELECTOR_COM_NR = 3
GENERATOR_COM_NR = 19

sample_ctr = 0

with my_serial(CAMERA_COM_NR) as sr_camera:
    with my_serial(SELECTOR_COM_NR) as sr_selector:
        with my_serial(GENERATOR_COM_NR) as sr_generator:
            read(sr_camera)
            read(sr_selector)
            read(sr_generator)
            
            writeln(sr_generator, "1")
            writeln(sr_camera, "Start")
    
            last_sample = 1
            
            while True:
                curr_sample = int(read_byte(sr_camera))&0b1
                if(last_sample == 0 and curr_sample == 1):
                    writeln(sr_selector, str(sample_ctr))
                last_sample = curr_sample
                sample_ctr += 1