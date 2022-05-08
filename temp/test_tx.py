import serial  
import time

def calc_command(vertical=0, horizontal=0, horizontal_speed=0x3f, vertical_speed=0x3f):
    address_code=0x01
    command_1=0x00
    command_2=0x00
    data_1=horizontal_speed%0x100
    data_2=vertical_speed%0x100

    if vertical>0:
        command_2 |= 0x08
    if vertical<0:
        command_2 |= 0x10
    if horizontal>0:
        command_2 |= 0x02
    if horizontal<0:
        command_2 |= 0x04
    
    print(hex(command_2))

    checksum=(address_code+command_1+command_2+data_1+data_2)%0x100

    return [0xff,address_code,command_1,command_2,data_1,data_2,checksum]

# print("first command")

ser = serial.Serial(port='COM4', baudrate=2400, timeout=100, bytesize=8, stopbits=1)

tx_command=calc_command(0,0,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()
time.sleep(0.2)
tx_command=calc_command(1,1,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()

time.sleep(1)

tx_command=calc_command(0,0,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()
time.sleep(0.2)
tx_command=calc_command(-1,-1,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()

time.sleep(2)

tx_command=calc_command(0,0,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()
time.sleep(0.2)
tx_command=calc_command(1,1,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()

time.sleep(1)

tx_command=calc_command(0,0,0x3f,0x3f)
ser.write(tx_command)  
readdata=ser.read_all()
time.sleep(0.2)
ser.write(tx_command)  
readdata=ser.read_all()



ser.close()