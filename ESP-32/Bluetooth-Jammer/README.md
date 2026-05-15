# ESP32 NRF24L01 2.4GHz Jammer

A personal research project for studying 2.4GHz RF interference using an ESP32 microcontroller and NRF24L01+PA+LNA module. Built and tested on a personal Bluetooth speaker as a controlled RF interference experiment.

> ⚠️ **Legal Notice** — Jamming radio frequencies is illegal in most countries including India (Indian Wireless Telegraphy Act, 1933). This project is strictly for **educational and personal research purposes only**, tested exclusively on your own hardware in an isolated environment. Do not use this on devices you do not own.

---

## How It Works

The ESP32 configures the NRF24L01 module to transmit a **constant carrier wave** across the 2.4GHz band (channels 2–79), hopping in 2MHz steps. This raises the noise floor across the band, causing interference with Bluetooth Classic, BLE, and 2.4GHz WiFi devices in close proximity.

Key behaviours:
- Channel hops from 2 → 79 → 2 continuously (bounce pattern)
- PA level set to maximum for strongest possible output
- Data rate set to 2Mbps, CRC disabled, AutoAck off
- Watchdog timer auto-resets the ESP32 if it freezes
- Radio re-initializes every 30 seconds to prevent silent failure states

---

## Hardware Required

| Component | Details |
|---|---|
| ESP32 Dev Board | Any standard 30-pin or 38-pin variant |
| NRF24L01+PA+LNA | Version with external antenna for best range |
| Jumper wires | 7x female-to-female dupont |
| Capacitor (recommended) | 100µF electrolytic across NRF24 VCC/GND |

---

## Wiring

| Wire Color | ESP32 Pin | NRF24L01 Pin |
|---|---|---|
| Red | 3V3 | VCC |
| Black | GND | GND |
| Orange | D5 | CE |
| Brown | D13 | CSN |
| Yellow | D18 | SCK |
| Blue | D19 | MISO |
| Green | D23 | MOSI |

> ⚠️ Power the NRF24L01 from **3.3V only**. 5V will permanently damage the module.

**Recommended:** Solder a 100µF electrolytic capacitor directly between VCC and GND pins on the NRF24L01 module to stabilize the power rail and prevent initialization failures.

---

## Dependencies

Install via Arduino IDE Library Manager:

- [RF24](https://github.com/nRF24/RF24) by TMRh20

---

## Setup

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Add ESP32 board support:
   - Go to **File → Preferences**
   - Add to Additional Board Manager URLs:
