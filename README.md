# Energy Consumption Monitor

Real-time energy consumption monitoring system using an **Arduino Nano** and an **ACS712 5A current sensor**.  
The project reads current values from the sensor, sends them via serial communication, and displays them in a **Python desktop application** built with **PyQt5** that plots real-time graphs, saves the data to CSV files, and allows exporting the plotted graph as an image.

---

## Overview

This system allows measuring and visualizing the electrical current of a device over time, estimating energy consumption, and logging data for further analysis.  
It’s divided into two main parts:

### 1. Hardware

- **Arduino Nano**
- **ACS712 5A Current Sensor**
- The Arduino reads the analog signal from the ACS712, converts it to current in milliamperes (mA), and sends timestamped readings via serial communication in **CSV format**.

### 2. Software

- **Python Desktop Application (UI)**
- Built with **PyQt5** and **Matplotlib**.
- Reads serial data, plots current vs. time in real-time, and can save data to CSV or export the final plot as an image file.
- Main functions:
  - Configure serial port and baud rate.
  - Start and stop data collection.
  - Display real-time current graph.
  - Show average, RMS, and estimated energy (Wh).
  - Automatically save or export data.

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

---

## Firmware

The firmware is written entirely in **C using ATmega328P registers (bare-metal)**, without the Arduino framework.
It performs the following tasks:

* Initializes **UART (9600 bps)** for serial output.
* Uses **Timer0 in CTC mode** to maintain a 1 ms timestamp counter.
* Reads **analog data from A0 (ADC0)** connected to the ACS712.
* Converts the raw ADC value into **current in milliamperes (mA)**.
* Sends results in **CSV format**:

```
<timestamp_ms>,<current_mA>
```

Example:

```
1245,-56
1261,-48
1277,15
1293,102
```

---

## Python Application

* Developed using **PyQt5** and **Matplotlib**.
* Modules:

  * `drivers/` → handles serial communication and sensor calibration.
  * `core/` → manages logging, data analysis, and coordination.
  * `ui/` → main interface with real-time plotting and user controls.
* CSV data is logged automatically with timestamps and current values.
* Graphs can be exported as images.

---

## Requirements

### Firmware

* Developed using **PlatformIO** (AVR environment).
* Compatible with **Arduino Nano @ 16 MHz**.

### Python Application

* **Python 3.9+**
* Dependencies:

```bash
pip install pyserial matplotlib pandas PyQt5
```

---

## How to Run

### Arduino Firmware

1. Connect the **ACS712 OUT pin** to **A0** on the Arduino Nano.
2. Upload the firmware using **PlatformIO** (located in `firmware/src/main.c`).
3. Open the serial monitor at **9600 baud** to verify readings.

### Python UI

1. Connect the Arduino Nano to your PC via USB.

2. Run the application:

   ```bash
   cd app
   python -m src.main
   ```

3. In the window:

   * Click **Settings** to select the correct COM port and baud rate.
   * Click **Start** to begin data collection.
   * Click **Stop** to end the capture and view statistics.
   * Optionally, export the graph or open the saved CSV.

---

## License

This project is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.
You are free to use, modify, and share it for **non-commercial purposes**, with attribution to the author.
The full license text is available in [`LICENSE`](LICENSE).

---

## Author

**Matheus Renó Torres**
Engineering Student @ INATEL
