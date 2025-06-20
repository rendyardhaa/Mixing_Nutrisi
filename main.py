from threading import Thread
import time
import yaml
import csv
import os
from datetime import datetime
from core.sensor import read_sensor_wec, read_sensor_wmps, read_pressure
from controllers.pid_controller import PIDController
from controllers.uart import uart_send, send_pwm_zero

# Load config
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

setpoint = config['setpoint']
pid_conf = config['pid']

# PID
pid_ec = PIDController(**pid_conf['motor_a_b'], name="EC")
pid_ph = PIDController(**pid_conf['motor_ph'], name="pH")

# Logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = f"logs/pid_log_{timestamp}.csv"
os.makedirs("logs", exist_ok=True)

with open(log_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "EC", "Setpoint_EC", "pH", "Setpoint_pH", "Temp", "Pressure", "PWM_EC", "PWM_pH"])

def main():
    print("🟢 Sistem Mixing Nutrisi dimulai...")
    while True:
        try:
            ec = read_sensor_wec()
            ph, temp = read_sensor_wmps()
            volt, pressure = read_pressure()

            pwm_ec = pwm_ph = 0

            if ec is not None:
                print(f"[EC]      {ec:.2f} µS/cm")
            if ph is not None and temp is not None:
                print(f"[pH]      {ph:.2f} | Temp: {temp:.1f}°C")
            print(f"[Pressure] {pressure:.1f} kPa (V={volt:.2f} V)")

            if ec and ph and pressure >= setpoint['pressure_kpa']:
                pwm_ec = pid_ec.calculate(setpoint['ec'], ec)
                pwm_ph = pid_ph.calculate(setpoint['ph'], ph)
                uart_send(f"A:{pwm_ec},B:{pwm_ec},pH:{pwm_ph},nutrisi:0\n")
                print(f"📤 UART SENT → A:{pwm_ec}, B:{pwm_ec}, pH:{pwm_ph}, nutrisi:0")
            else:
                print("🕒 Menunggu tekanan mencukupi...")

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([now, ec, setpoint['ec'], ph, setpoint['ph'], temp, pressure, pwm_ec, pwm_ph])

            time.sleep(1)

        except KeyboardInterrupt:
            send_pwm_zero()
            print("🛑 Sistem dihentikan.")
            break

        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)
