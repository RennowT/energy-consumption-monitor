# Energy Consumption Monitor

Real-time energy consumption monitoring system using an **Arduino Nano** and an **ACS712 5A current sensor**.  
The project reads current values from the sensor, sends them via serial communication, and displays them in a **Python desktop application** that plots real-time graphs, optionally saves the data to CSV files, and allows saving the generated graph as an image file.

---

## Overview

This system allows you to measure and visualize the electrical current of a device over time, estimate energy consumption, and log data for further analysis.  
It’s divided into two main parts:

### 1. Hardware

- **Arduino Nano**  
- **ACS712 5A Current Sensor**
- The Arduino reads the analog signal from the ACS712 and sends timestamped readings via serial communication.

### 2. Software

- **Python Desktop Application (UI)**
- Reads serial data, plots current vs. time in real-time, and can save data to CSV or export the final plot as an image file.
- The user can:
  - Select which device is being measured.
  - Choose whether to save data to CSV.
  - Change the default output directory.
  - Start and stop data collection.
  - Save the plotted graph manually.

---

## Hardware Details

| Component | Description |
|------------|-------------|
| **Microcontroller** | Arduino Nano (ATmega328P) |
| **Sensor** | ACS712 5A Current Sensor |
| **Measurement Range** | 0 A – 5 A |
| **Output** | Analog voltage proportional to measured current |
| **Supply Voltage** | 5 V DC |
| **Sensitivity** | 185 mV/A |
| **Communication** | Serial (9600 baud) |

**Sensor formula (from datasheet):**

```cpp
I = (VOUT - 2.5) / 0.185
```

*(for 5 A version, VOUT centered at 2.5 V when current = 0 A)*

---

## Software Features

- **Real-time plotting** using Matplotlib and threading.
- **Serial communication** with configurable COM port and baud rate.
- **CSV logging** with corrected timestamps (relative to first sample).
- **Graph reset and stop button** for clean data sessions.
- **Option to save the generated graph as an image file.**
- **Simple and responsive UI** built with Tkinter.

---

## Requirements

### Firmware

- Developed using **PlatformIO**, but an `.ino` version is also available for Arduino IDE users.

### Python Application

- Python 3.11 or higher
- Required packages:

```bash
pip install pyserial matplotlib tkinter pandas
```

---

## How to Run

### Arduino Firmware

1. Connect the **ACS712 OUT pin** to **A0** on the Arduino Nano.
2. Upload the provided firmware using **PlatformIO** or the `.ino` file through the **Arduino IDE**.
3. Open the serial monitor to verify the current readings.

### Python UI

1. Connect the Arduino via USB.
2. Run the Python application:

   ```bash
   python app.py
   ```

3. Select the device name, toggle CSV logging if desired, and click **Start**.
4. Press **Stop** to end data collection and close the session.
5. Optionally, click **Save Graph** to export the plotted chart as an image.

---

## Future Improvements

- Add RMS and power calculations (P = V × I).
- Implement automatic sensor calibration.
- Add energy cost estimation feature.
- Include temperature compensation for sensor drift.

---

## License

This project is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.
You are free to use, modify, and share the project for **non-commercial purposes only**, with attribution to the author.
The full license text is available in [`LICENSE`](LICENSE).

---

## Author

**Matheus Renó Torres**
Engineering Student @ INATEL
