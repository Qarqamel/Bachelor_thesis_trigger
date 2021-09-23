import serial

with serial.Serial(port="COM26", baudrate=115200,bytesize = 8,
                    timeout = None, stopbits=serial.STOPBITS_ONE) as serialPort:

    serialPort.write('start\n'.encode('utf-8'))
    
    output_list = [serialPort.readline().decode('utf-8').strip() for i in range(400)]
    
    for i, j in zip(output_list, output_list[1:]):
        print(int(i), int(j)-int(i))
    
    #print(output_list)
