import serial
from tabulate import tabulate 

with serial.Serial(port="COM14", baudrate=115200,bytesize = 8,
                    timeout = None, stopbits=serial.STOPBITS_ONE) as serialPort:

    serialPort.write('start\n'.encode('utf-8'))
    
    output_list = [serialPort.readline().decode('utf-8').strip() for i in range(400)]
    
    output_diff_list = [int(j)-int(i) for i, j in zip(output_list, output_list[1:])]
    output_diff2_list = [int(j)-int(i) for i, j in zip(output_diff_list, output_diff_list[1:])]
    
print(tabulate(zip(output_list, output_diff_list, output_diff2_list),
      headers = ["Timer_ctr","diff1","diff2"]))

with open('outputs.txt', 'w') as f:
    f.write(tabulate(zip(output_list, output_diff_list, output_diff2_list),
      headers = ["Timer_ctr","diff1","diff2"]))
    
