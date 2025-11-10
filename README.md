# Energy Consumption Monitor

Real-time energy consumption monitoring system using an **Arduino Nano** and an **ACS712 5A current sensor**.
The project reads current values from the sensor, sends them via serial communication, and displays them in a **Python desktop application** that plots real-time graphs, optionally saves the data to CSV files, and allows saving the generated graph as an image file.

---

## Overview

This system allows you to measure and visualize the electrical current of a device over time, estimate energy consumption, and log data for further analysis.
It’s divided into two main parts:

### 1. Hardware

* **Arduino Nano**
* **ACS712 5A Current Sensor**
* The Arduino reads the analog signal from the ACS712, converts it to current in milliamperes (mA), and sends timestamped readings via serial communication in **CSV format**.

### 2. Software

* **Python Desktop Application (UI)**
* Reads serial data, plots current vs. time in real-time, and can save data to CSV or export the final plot as an image file.
* The user can:

  * Select which device is being measured.
  * Choose whether to save data to CSV.
  * Change the default output directory.
  * Start and stop data collection.
  * Save the plotted graph manually.

---

## Hardware Details

| Component             | Description                                     |
| --------------------- | ----------------------------------------------- |
| **Microcontroller**   | Arduino Nano (ATmega328P)                       |
| **Sensor**            | ACS712 5A Current Sensor                        |
| **Measurement Range** | 0 A – 5 A                                       |
| **Output**            | Analog voltage proportional to measured current |
| **Supply Voltage**    | 5 V DC                                          |
| **Sensitivity**       | 185 mV/A                                        |
| **Communication**     | Serial (9600 baud)                              |
| **Sampling Rate**     | ~62 samples/second (default)                    |

**Sensor formula (from datasheet):**

```cpp
I = (VOUT - 2.5) / 0.185
```

*(for the 5 A version, VOUT is centered at 2.5 V when current = 0 A)*

---

## Firmware

The firmware is written entirely in **C using ATmega328P registers (bare-metal)**, without the Arduino framework.
It performs the following tasks:

* Initializes **UART (9600 bps)** for serial output.
* Uses **Timer0 in CTC mode** to maintain a 1 ms timestamp counter.
* Reads **analog data from A0 (ADC0)** connected to the ACS712.
* Converts the raw ADC value into **current in milliamperes (mA)**.
* Sends the result in **CSV format**:

```
<timestamp_ms>,<current_mA>
```

Example output:

```
1245,-56
1261,-48
1277,15
1293,102
```

### Sampling rate

* Default: ~62.5 samples per second (`SAMPLE_PERIOD_MS = 16`).
* Can be increased or reduced by changing this constant in the firmware.
* Higher rates require a higher UART baud rate.

---

## Python Application

* **Real-time plotting** using Matplotlib and threading.
* **Serial communication** with configurable COM port and baud rate.
* **CSV logging** with corrected timestamps (relative to first sample).
* **Graph reset and stop button** for clean data sessions.
* **Option to save the generated graph as an image file.**
* **Simple and responsive UI** built with Tkinter.

---

## Requirements

### Firmware

* Developed using **PlatformIO** (AVR environment).
* Compatible with **Arduino Nano** @ 16 MHz.

### Python Application

* Python 3.11 or higher
* Required packages:

```bash
pip install pyserial matplotlib tkinter pandas
```

---

## How to Run

### Arduino Firmware

1. Connect the **ACS712 OUT pin** to **A0** on the Arduino Nano.
2. Upload the firmware using **PlatformIO** (the code is in `firmware/energy-monitor-nano/src/main.c`).
3. Open the serial monitor at **9600 baud** to verify the readings.
   Each line corresponds to a timestamp and current in milliamperes.

### Python UI

1. Connect the Arduino via USB
2. Run the Python application:

   ```bash
   python app.py
   ```

3. Select the correct COM port and press **Start** to begin data collection.
4. Press **Stop** to end data capture.
5. Optionally, click **Save Graph** to export the plotted chart as an image.

---

## Future Improvements

* Add RMS and power calculations (P = V × I).
* Implement automatic offset calibration.
* Add energy and cost estimation.
* Optional binary protocol for higher sampling rates.

---

## License

This project is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.
You are free to use, modify, and share the project for **non-commercial purposes only**, with attribution to the author.
The full license text is available in [`LICENSE`](LICENSE).

---

## Author

**Matheus Renó Torres**
Engineering Student @ INATEL
