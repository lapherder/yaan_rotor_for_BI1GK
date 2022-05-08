def MERGE_COMMAND(vertical,horizontal):
    # 从(vertical,horizontal)->查找指令
    if (vertical,horizontal) == (1,1):
        return COMMAND['UP_RIGHT']
    elif (vertical,horizontal) == (1,0):
        return COMMAND['UP']
    elif (vertical,horizontal) == (1,-1):
        return COMMAND['UP_LEFT']
    elif (vertical,horizontal) == (0,1):
        return COMMAND['RIGHT']
    elif (vertical,horizontal) == (0,0):
        return COMMAND['STOP']
    elif (vertical,horizontal) == (0,-1):
        return COMMAND['LEFT']
    elif (vertical,horizontal) == (-1,1):
        return COMMAND['DOWN_RIGHT']
    elif (vertical,horizontal) == (-1,0):
        return COMMAND['DOWN']
    elif (vertical,horizontal) == (-1,-1):
        return COMMAND['DOWN_LEFT']

COMMAND = {
'UP_RIGHT' : [255, 1, 0, 10, 63, 63, 137],
'UP' : [255, 1, 0, 8, 63, 63, 135],
'UP_LEFT' : [255, 1, 0, 12, 63, 63, 139],
'RIGHT' : [255, 1, 0, 2, 63, 63, 129],
'STOP' : [255, 1, 0, 0, 63, 63, 127],
'LEFT' : [255, 1, 0, 4, 63, 63, 131],
'DOWN_RIGHT' : [255, 1, 0, 18, 63, 63, 145],
'DOWN' : [255, 1, 0, 16, 63, 63, 143],
'DOWN_LEFT' : [255, 1, 0, 20, 63, 63, 147],
}