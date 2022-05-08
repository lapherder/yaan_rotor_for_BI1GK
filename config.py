# 软件限位器设置
MIN_ELEVATION = 0   # 仰角下限<=0
MAX_ELEVATION = 90  # 仰角上限>=90
MIN_AZIMUTH = 0   # 仰角下限<=0
MAX_AZIMUTH = 540  # 仰角上限>=360
# MAX_AZIMUTH = MIN_AZIMUTH + 540 # 考虑到最大连贯旋转需求为180°，故建议保证540°的自由旋转空间

ACCEPTABLE_ERROR = 3

VERTICAL_SPEED = 10     # 垂直方向转速，单位°/s
HORIZONTAL_SPEED = 10   # 水平方向转速，单位°/s
