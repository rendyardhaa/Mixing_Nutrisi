from pymodbus.client import ModbusSerialClient
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import yaml

with open('config/config.yaml') as f:
    cfg = yaml.safe_load(f)

# ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x49)
chan0 = AnalogIn(ads, ADS.P0)

V_ZERO = 0.5
V_MAX = 4.5
P_MAX = 12.0

# Modbus
client = ModbusSerialClient(
    method='rtu',
    port=cfg['modbus']['port'],
    baudrate=cfg['modbus']['baudrate'],
    timeout=cfg['modbus']['timeout']
)
client.connect()

def crc16(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            crc = (crc >> 1) ^ (0xA001 if crc & 1 else 0)
    return crc

def read_sensor_wec():
    try:
        req = bytearray([0x02, 0x03, 0x00, 0x00, 0x00, 0x04])
        crc = crc16(req)
        req += crc.to_bytes(2, byteorder='little')
        client.socket.write(req)
        time.sleep(0.3)
        resp = client.socket.read(13)
        if resp and len(resp) >= 13:
            ec_raw = (resp[3] << 8) | resp[4]
            decimal = (resp[9] << 8) | resp[10]
            ec = ec_raw / (10 ** decimal if decimal < 4 else 1)
            return ec
    except:
        pass
    return None

def read_sensor_wmps():
    try:
        req = bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x03])
        crc = crc16(req)
        req += crc.to_bytes(2, byteorder='little')
        client.socket.write(req)
        time.sleep(0.3)
        resp = client.socket.read(11)
        if resp and len(resp) >= 9:
            ph = ((resp[3] << 8) | resp[4]) * 0.01
            temp = ((resp[7] << 8) | resp[8]) * 0.1
            return ph, temp
    except:
        pass
    return None, None

def read_pressure():
    try:
        voltage = chan0.voltage
        pressure = (voltage - V_ZERO) * (P_MAX / (V_MAX - V_ZERO))
        return round(voltage, 2), round(pressure * 1000, 2)
    except:
        return 0.0, 0.0
