# 🧪 Mixing Nutrisi Otomatis (Smart Nutrient Mixing System)

Sistem ini dirancang untuk mengontrol pencampuran nutrisi secara otomatis menggunakan **sensor pH, EC, dan tekanan**, serta **kontrol PID** yang mengatur aktuator melalui **UART**. Sistem bekerja secara **real-time**, mencatat semua pembacaan dan hasil kontrol ke dalam file log CSV.

---

## 📦 Struktur Folder

mixing_nutrisi_system/
├── config/
│ └── config.yaml # Konfigurasi semua parameter sistem
├── controllers/
│ ├── pid_controller.py # Modul PIDController
│ └── uart.py # Modul pengiriman PWM via UART pigpio
├── core/
│ └── sensor.py # Pembacaan semua sensor (WEC, WMPS, Pressure)
├── logs/
│ └── pid_log_YYYYMMDD_HHMMSS.csv # Log otomatis
└── main.py # Entry point utama sistem

---

## ⚙️ Requirements

- Python ≥ 3.7
- Raspberry Pi dengan pigpio aktif
- Library eksternal:
  - `pymodbus`
  - `adafruit-circuitpython-ads1x15`
  - `pigpio`
  - `PyYAML`

### 💻 Install dengan pip:

```bash
pip install pymodbus adafruit-circuitpython-ads1x15 pigpio PyYAML
```

🔧 Jalankan pigpio daemon:

```bash
sudo pigpiod
```

---

## 🛠️ Konfigurasi

Edit `config/config.yaml` untuk menyesuaikan:

```yaml
setpoint:
  ec: 1800 # Target EC (µS/cm)
  ph: 6.3 # Target pH
  pressure_kpa: 2500 # Tekanan minimum agar PID aktif (dalam kPa)

pid:
  motor_a_b:
    Kp: 10.0
    Ki: 0.0
    Kd: 0.0
  motor_ph:
    Kp: 1.08
    Ki: 1.54
    Kd: 0.189
```

---

## 🚀 Cara Menjalankan

```bash
python3 main.py
```

Sistem akan mencetak pembacaan sensor secara real-time ke terminal.

Saat tekanan mencukupi, PID akan dijalankan dan PWM dikirim ke aktuator.

Semua data disimpan ke dalam file `logs/pid_log_<timestamp>.csv`.

---

## 🔍 Data Logging (CSV)

Setiap loop, sistem akan menyimpan:

| Kolom CSV   | Keterangan                |
| ----------- | ------------------------- |
| timestamp   | Waktu pembacaan           |
| EC          | Nilai EC dari sensor WEC  |
| Setpoint_EC | Target EC dari config     |
| pH          | Nilai pH dari sensor WMPS |
| Setpoint_pH | Target pH dari config     |
| Temp        | Suhu air (°C)             |
| Pressure    | Tekanan air dalam kPa     |
| PWM_EC      | Hasil PID untuk EC        |
| PWM_pH      | Hasil PID untuk pH        |

---

## 📌 Catatan Teknis

- PWM motor A dan B mengikuti nilai yang sama dari PID EC
- Sensor WEC dan WMPS menggunakan protokol Modbus RTU
- Sensor tekanan dibaca dari ADS1115 analog ke I2C
- Semua pembacaan sensor dan kendali dijalankan real-time (interval 1 detik)

---

## 💡 Pengembangan Selanjutnya

- ⏱️ Logging otomatis tiap jam (rolling log)
- 🧠 Auto-tuning PID via antarmuka (opsional)
- 🛑 Watchdog untuk antisipasi freeze sensor
- 📤 Integrasi ke cloud/IoT dashboard

---

## 👨‍💻 Kontributor

Founder & Developer: [Nama Kamu]

Sistem ini dibangun untuk keperluan pertanian pintar dan automatisasi industri nutrisi hidroponik.

---

## 📜 License

MIT License – Silakan gunakan, kembangkan, dan kredit sesuai semangat open-source.
