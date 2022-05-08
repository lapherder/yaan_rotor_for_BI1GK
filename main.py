import keyboard
from controller import controller
from logger import logger
import sys
import time
from threading import Thread, Event

yaan_logger = logger()
rotor = controller('COM3',yaan_logger)

def manual_control():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
            rotor.terminate()
            return
        
        elif event.event_type == keyboard.KEY_DOWN and event.name == 's':
            rotor.tx_command(0,0)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'q':
            rotor.tx_command(1,-1)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'w':
            rotor.tx_command(1,0)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'e':
            rotor.tx_command(1,1)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'a':
            rotor.tx_command(0,-1)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'd':
            rotor.tx_command(0,1)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'z':
            rotor.tx_command(-1,-1)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
            rotor.tx_command(-1,0)
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'c':
            rotor.tx_command(-1,1)
        elif event.event_type == keyboard.KEY_UP and event.name in {'q','w','e','a','d','z','x','c',}:
            rotor.tx_command(0,0)

# def set_target_and_rotate():
#     scan()


def prt_angle():
    timer=time.time()
    while True:
        if time.time()-timer>0.5:
            cur_angle = rotor.get_angle()
            print(cur_angle)
            # sys.stdout.write("\r                                                              ")
            # sys.stdout.write("\r%g\t%g\t%g" %(cur_angle[0], cur_angle[2],))
            # sys.stdout.flush() 
            timer=time.time()

# a=Thread(target=prt_angle)
# a.start()
# while True:   
#     event = keyboard.read_event()
#     if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
#         rotor.terminate()
#         break
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 's':
#             rotor.tx_command(0,0)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'q':
#             rotor.tx_command(1,-1)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'w':
#         rotor.tx_command(1,0)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'e':
#         rotor.tx_command(1,1)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'a':
#         rotor.tx_command(0,-1)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'd':
#         rotor.tx_command(0,1)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'z':
#         rotor.tx_command(-1,-1)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
#         rotor.tx_command(-1,0)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'c':
#         rotor.tx_command(-1,1)
#     elif event.event_type == keyboard.KEY_UP and event.name in {'q','w','e','a','d','z','x','c',}:
#         rotor.tx_command(0,0)
#     elif event.event_type == keyboard.KEY_DOWN and event.name == 'p':
#         rotor.target_elevation = 45
#         rotor.target_azimuth = 180
#         rotor.rotate_to_target()




manual_control()