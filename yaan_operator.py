import serial 
from threading import Thread, Event
import time
import numpy as np
from copy import deepcopy

from command import COMMAND,MERGE_COMMAND
from config import MIN_ELEVATION,MAX_ELEVATION,MIN_AZIMUTH,MAX_AZIMUTH,ACCEPTABLE_ERROR,VERTICAL_SPEED,HORIZONTAL_SPEED

class yaan_operator():
    def __init__(self, port, yaan_logger):
        self.yaan_logger = yaan_logger
        self.last_angle = [0.0]*3    # 从传感器读来的上一个数据(方位角已反转)，-180<方位角<180，-180<仰角<180
        self.acc_angle = [0.0]*3    # 计算出来的累加数据，方位角无限制（读取数据帧50Hz时，角速度超过25round/s会计数错误）,由main_thread写，update_show_angle()调用
        self.acc_round = 0          # 计数累加的圈数，当acc_round = 0时，0<方位角<360
        self.ser_available = False       # 记录串口是否因电磁波干扰掉了
        self.show_angle = [0.0]*3   # 上层读取接口，如果ser_available则等于acc_angle，否则根据上次读数估算一个值
        self.predict_timmer = time.time()   # 记录更新show_angle的时间，用来预测show_angle

        self.command = [0,0]        # controller控制接口,(vertical,horizontal)
        self.cur_command = [0,0]    # 记录当前正在执行的指令，如果发送指令与之一样则不用重复发送

        self.terminate_event = Event()  # 终止信号量，用来结束控制线程
        self.terminate_event.clear()
        self.changing_command = Event() # 发送指令锁，发送指令需要0.2s间隔，防止期间再次发送
        self.changing_command.clear()
        self.main_thread = Thread(target=self.start_operate)

        try:
            self.port = port
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=100, bytesize=8, stopbits=1)
            self.ser_available = True
            self.main_thread.start()
        except Exception as e:
            self.yaan_logger.prt_info(e)
            self.yaan_logger.prt_info('控制器初始化失败')
    
    def start_operate(self):
        self.yaan_logger.prt_info('开始获取姿态传感器读数&控制云台')
        AngleData=[0.0]*8
        Bytenum = 0               #读取到这一段的第几位
        captured = 0
        CheckSum = 0              #求和校验位
        while not self.terminate_event.is_set():
            # 读传感器数据
            datahex = self.unfail_read()            
            for data in datahex:  #在输入的数据进行遍历
                if data==0x55 and Bytenum==0: #0x55位于第一位时候，开始读取数据，增大bytenum
                    CheckSum=data
                    Bytenum=1
                    captured=1
                elif data==0x53 and Bytenum==1:
                    CheckSum+=data
                    Bytenum=2
                    captured=1
                elif captured==1:
                    if Bytenum<10:
                        AngleData[Bytenum-2]=data
                        CheckSum+=data
                        Bytenum+=1
                    else:
                        if data == (CheckSum&0xff):
                            angle = self.decode_angle_data(AngleData)
                            self.update_acc_angle(angle)
                        CheckSum=0
                        Bytenum=0
                        captured=0
                else:
                    Bytenum==0
            
            # 软件限位器
            # if self.show_angle[0] >= MAX_ELEVATION and self.cur_command[0] == 1:
            #     self.yaan_logger.prt_info("已到达软件限位MAX_ELEVATION")
            #     self.command = [0,0]
            # if self.show_angle[0] <= MIN_ELEVATION and self.cur_command[0] == -1:
            #     self.yaan_logger.prt_info("已到达软件限位MIN_ELEVATION")
            #     self.command = [0,0]
            # if self.show_angle[2] >= MAX_AZIMUTH and self.cur_command[1] == 1:
            #     self.yaan_logger.prt_info("已到达软件限位MAX_AZIMUTH")
            #     self.command = [0,0]
            # if self.show_angle[2] <= MIN_AZIMUTH and self.cur_command[1] == -1:
            #     self.yaan_logger.prt_info("已到达软件限位MIN_AZIMUTH")
            #     self.command = [0,0]

            # 控制部分
            if self.command != self.cur_command:
                if not self.changing_command.is_set():
                    self.changing_command.set()
                    Thread(target=self.tx_command()).start()
            
    def decode_angle_data(self,datahex):                                 
        rxl = datahex[0]                                        
        rxh = datahex[1]
        ryl = datahex[2]                                        
        ryh = datahex[3]
        rzl = datahex[4]                                        
        rzh = datahex[5]
        k_angle = 180.0
    
        angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
        angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
        angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
        if angle_x >= k_angle:
            angle_x -= 2 * k_angle
        if angle_y >= k_angle:
            angle_y -= 2 * k_angle
        if angle_z >=k_angle:
            angle_z-= 2 * k_angle
    
        return angle_x,angle_y,angle_z

    def update_acc_angle(self,raw_angle):
        angle = [raw_angle[0],raw_angle[1],-raw_angle[2]]
        # 更新raw_angle和acc_angle
        # 因为为了配合云台，方位角模到0°~360°，所以判断acc_round是根据在0°处的方位角跳变
        # 增加+-90°的约束是为了防止读数在+-180°之间跳变时影响acc_round
        if angle[2] > 0 and angle[2] < 90 and self.last_angle[2] <= 0 and self.last_angle[2] > -90:
            self.acc_round += 1
        elif self.last_angle[2] > 0 and self.last_angle[2] < 90 and angle[2] <= 0 and angle[2] > -90:
            self.acc_round -= 1
        self.acc_angle[0] = angle[0]
        self.acc_angle[1] = angle[1]
        self.acc_angle[2] = angle[2] % 360 + self.acc_round * 360
        self.last_angle = angle

    def tx_command(self):
        self.unfail_write(COMMAND['STOP'])
        # self.ser.read_all()
        time.sleep(0.2)
        vertical,horizontal = self.command[0],self.command[1]
        self.unfail_write(MERGE_COMMAND(vertical,horizontal))
        # self.ser.read_all()
        self.update_show_angle()    # 必须，防止串口掉了，更新一下预测数值。
        self.cur_command = [vertical,horizontal]
        self.changing_command.clear()

    def unfail_read(self):
        while True:
            try:
                datahex = self.ser.read(33)
                self.ser_available = True
                return datahex
            except:
                self.ser_available = False
                self.ser = serial.Serial(port=self.port, baudrate=9600, timeout=100, bytesize=8, stopbits=1)
    
    def unfail_write(self,cmd):
        while True:
            try:
                self.ser.write(cmd)
                self.ser_available = True
                return
            except:
                self.ser_available = False
                self.ser = serial.Serial(port=self.port, baudrate=9600, timeout=100, bytesize=8, stopbits=1)

    def reset_angle(self, round = 0):
        self.acc_round = round
        self.yaan_logger.prt_info('相位角已重置')

    def update_show_angle(self):
        # 如果串口没掉，show_angle=acc_angle否则根据角速度预测角度
        # 每次改变天线指令时需要调用该函数
        if self.ser_available:
            self.show_angle = self.acc_angle
            self.predict_timmer = time.time()
        else:
            interval = time.time()-self.predict_timmer
            self.show_angle[0] = self.acc_angle[0] + self.cur_command[0]*interval*VERTICAL_SPEED
            self.show_angle[2] = self.acc_angle[2] + self.cur_command[1]*interval*HORIZONTAL_SPEED
            self.predict_timmer = time.time()
        return self.show_angle

    def terminate(self):
        self.terminate_event.set()
        self.main_thread.join()



# a = attitude_transducer(ser,breaker)
# a.t1.start()
# time.sleep(0.5)
# a.reset_angle()
# print('start')

# for _ in range(60):
#     (cur_angle_x, cur_angle_y, cur_angle_z)=a.get_angle()
#     sys.stdout.write("\r                                                              ")
#     sys.stdout.write("\r%g\t%g\t%g" %(cur_angle_x, cur_angle_y, cur_angle_z,))
#     sys.stdout.flush() 
#     # print(a.last_angle)
#     time.sleep(0.5)
# breaker.set()
# a.t1.join()
