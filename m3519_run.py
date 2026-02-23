import serial
import time
from DM_CAN import Motor, MotorControl, DM_Motor_Type, Control_Type

# ===================== 固定配置 =====================
COM_PORT    = "COM5"
BAUD_RATE   = 921600
MOTOR_TYPE  = DM_Motor_Type.DM3507
MASTER_ID   = 0x11
# ====================================================

# 全局初始化（只执行一次）
ser = serial.Serial(COM_PORT, BAUD_RATE, 8, 'N', 1, 0.01)
ctrl = MotorControl(ser)

# 你要的【唯一驱动函数】：只传 电机ID + RPM
def motor_run(motor_id, rpm):
    rad = rpm * 0.1047197551  # RPM → rad/s
    ctrl.control_Vel(ctrl.motors_map[motor_id], rad)

# 初始化电机（只做一次）
motor = Motor(MOTOR_TYPE, 1, MASTER_ID)
ctrl.addMotor(motor)
ctrl.switchControlMode(motor, Control_Type.VEL)
time.sleep(0.1)
ctrl.enable(motor)
time.sleep(0.5)

# ===================== 你的极简循环 =====================
try:
    while True:
        motor_run(1, 50)   # 1. 电机ID=1，正转50RPM
        time.sleep(1)      # 2. 停1秒
        motor_run(1, -50)  # 3. 电机ID=1，反转50RPM
        time.sleep(1)      # 4. 停1秒
except KeyboardInterrupt:
    ctrl.disable(motor)
    ser.close()
