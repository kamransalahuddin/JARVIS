# Hardware

[Back to JARVIS](../README.md)

A webcam is enough for the vision demo. The following hardware enables physical tracking and light control.

## Servo-mounted camera

The original sketch was found at `~/Documents/Arduino/facetracker/facetracker.ino`; its iCloud contents became available during the audit. [The included copy](facetracker/facetracker.ino) is byte-for-byte identical to that file and matches the firmware supplied by the author.

1. Install [Arduino IDE](https://www.arduino.cc/en/software/) and the board package matching your controller.
2. Install the [Arduino Servo library](https://github.com/arduino-libraries/Servo) through Library Manager if it is not available.
3. Open `hardware/facetracker/facetracker.ino`, select the actual board and serial port, and upload it.
4. Connect horizontal servo signal to **pin 9** and vertical servo signal to **pin 7**. Use power appropriate for the servos, with a common ground to the controller. Exact servo ratings and the original board model were not established by the software audit.
5. Close Serial Monitor and set `ARDUINO_PORT` in `.env` to the actual port, such as `/dev/cu.usbserial-...` on macOS, `/dev/ttyUSB0` on Linux, or `COM3` on Windows.

The protocol is ASCII `x,y\r` at **115200 baud**. Python sends offsets from the frame center. The firmware adjusts the two angles by the corresponding offset divided by 60, constraining angles to 0–180 degrees. It starts its angle variables at 90 degrees.

The original Mac-specific port was `/dev/cu.usbserial-A5069RR4`. It was not connected during the audit. Depending on the board, you may need its USB-to-serial driver; identify the controller/USB chipset before selecting one. Linux may require serial-device group access. No driver package, board model, or physical wiring has been guessed.

Leave `ARDUINO_PORT` empty to disable serial output while retaining face tracking.

## Smart lights

The existing `python-kasa` integration uses `SmartPlug` without device credentials. Use devices compatible with that API on the same reachable LAN; newer authenticated devices may require an application change.

Fill `IP_Address_right`, `IP_Address_left`, `IP_Address_LED1`, and `IP_Address_LED2`, then set `ENABLE_SMART_LIGHTS=true`.

| Gesture | Action |
| --- | --- |
| Pointing up | Right lamp on |
| Victory | Left lamp on |
| Thumb up | LED 1 on |
| Thumb down | LED 2 on |
| Open palm | All four on |
| Closed fist after one of those gestures | Corresponding device/group off |

Set `ENABLE_SMART_LIGHTS=false` for recognition without device actions. Physical servos and smart plugs were not activated during validation.
