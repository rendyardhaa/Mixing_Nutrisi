import pigpio
import time
import yaml

with open('config/config.yaml') as file:
    config = yaml.safe_load(file)['uart']

TX_PIN = config['tx_pin']
RX_PIN = config['rx_pin']
BAUD_RATE = config['baudrate']

pi = pigpio.pi()
if not pi.connected:
    raise Exception("❌ Tidak bisa konek ke pigpio daemon")

try:
    pi.bb_serial_read_close(RX_PIN)
except pigpio.error:
    pass

pi.set_mode(TX_PIN, pigpio.OUTPUT)
pi.bb_serial_read_open(RX_PIN, BAUD_RATE, 8)

def uart_send(message):
    try:
        pi.wave_clear()
        if isinstance(message, str):
            message = message.encode()
        pi.wave_add_serial(TX_PIN, BAUD_RATE, message)
        wave_id = pi.wave_create()
        if wave_id >= 0:
            pi.wave_send_once(wave_id)
            while pi.wave_tx_busy():
                time.sleep(0.01)
            pi.wave_delete(wave_id)
    except Exception as e:
        print(f"[UART] Error: {e}")

def send_pwm_zero():
    uart_send("A:0,B:0,pH:0,nutrisi:0\n")
