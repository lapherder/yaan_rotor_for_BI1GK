from threading import Thread, Event
import serial 
import time


from config import ACCEPTABLE_ERROR
from yaan_operator import yaan_operator

class controller:
    def __init__(self, port, yaan_logger):
        self.yaan_logger = yaan_logger
        self.operator = yaan_operator(port, yaan_logger)

        self.target_elevation = 0   # 天线的目标仰角  0<=target_elevation<90
        self.target_azimuth = 0     # 天线的目标方位角  0<=target_azimuth<360

        self.force_stop = Event()
        self.force_stop.clear()

        # self.terminate_event = Event()
        # self.angle_limit_thread = Thread(target=self.angle_limit)
        # self.angle_limit_thread.start()

    def tx_command(self,vertical,horizontal):
        self.operator.command=[vertical,horizontal]

    def get_angle(self):
        return self.operator.update_show_angle()

    def rotate_to_target(self):
        while not self.force_stop.set():
            if abs((self.cur_elevation%360) - self.target_elevation) <= ACCEPTABLE_ERROR:
                vertical=0
            elif self.cur_elevation < self.target_elevation:
                vertical=1
            else:
                vertical=-1
            
            if abs((self.cur_azimuth%360) - self.target_azimuth) <= ACCEPTABLE_ERROR:
                horizontal=0
            elif self.cur_azimuth < self.target_azimuth:
                horizontal=1
            else:
                horizontal=-1
            self.tx_command(vertical=vertical,horizontal=horizontal)
            if vertical==0 and horizontal==0:
                self.tx_command(0,0)
                return
    
    def terminate(self):
        self.operator.terminate()


# from logger import logger
# yaan_logger = logger()
# a=controller('COM3',yaan_logger)
# a.tx_command(cmd='RIGHT')
# time.sleep(2)
# a.tx_command()