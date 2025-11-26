# Trigger Code Setup

## Arduino -> OpenBCI Cyton:
- Sends 5-bit binary trigger codes (0-31) via serial communication.

| Arduino Pin | OpenBCI Cyton Pin | Description          |
|-------------|-------------------|----------------------|
| 12          | D11               | Trigger Bit 0 (LSB)  |
| 10          | D12               | Trigger Bit 1        |
| 8           | D13               | Trigger Bit 2        |
| 6           | D17               | Trigger Bit 3        |
| 4           | D18               | Trigger Bit 4 (MSB)  |

- Arduino GND is connected to the optocoupler Pin 2
- OpenBCI DVDD is connected to the optocoupler Pin 5
- OpenBCI GND is connected to the optocoupler Pin 6

Notes:
- Cyton digital read pins held at LOW -> go to HIGH when trigger bit is HIGH.