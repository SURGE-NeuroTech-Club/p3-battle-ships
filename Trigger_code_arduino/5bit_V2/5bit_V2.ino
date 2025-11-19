// 5-bit trigger box for EEG/OpenBCI
// Uses pins 4, 6, 8, 10, 12 as outputs.
// Receives 3 bytes over serial:
//   [0] code (0–31, mapped to 5 LSBs)
//   [1] duration low byte (ms)
//   [2] duration high byte (ms)

const uint8_t NUM_TRIGGER_PINS = 5;
const uint8_t TRIGGER_PINS[NUM_TRIGGER_PINS] = {12, 10, 8, 6, 4};

void setup()
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        pinMode(TRIGGER_PINS[i], OUTPUT);
        digitalWrite(TRIGGER_PINS[i], HIGH); // idle HIGH
    }

    Serial.begin(115200);
}

void loop()
{
    // Wait until we have a full 3-byte packet
    if (Serial.available() >= 3)
    {
        int rawCode = Serial.read();          // 0–255
        int durLow  = Serial.read();          // 0–255
        int durHigh = Serial.read();          // 0–255

        if (rawCode < 0 || durLow < 0 || durHigh < 0)
        {
            // Shouldn't happen if Serial.available() >= 3, but safety check
            return;
        }

        uint8_t code = static_cast<uint8_t>(rawCode) & 0x1F; // 5 bits
        uint16_t pulseMs = static_cast<uint16_t>(durLow) |
                           (static_cast<uint16_t>(durHigh) << 8);

        // Optional guard: avoid 0-length pulses
        if (pulseMs == 0)
        {
            pulseMs = 1;
        }

        // Fire the trigger
        setTriggerPattern(code);
        delay(pulseMs);
        clearTriggers();
    }
}

void setTriggerPattern(uint8_t code)
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        bool bitHigh = (code >> i) & 0x01;
        // Active LOW: LOW = "1", HIGH = "0"
        digitalWrite(TRIGGER_PINS[i], bitHigh ? LOW : HIGH);
    }
}

void clearTriggers()
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        digitalWrite(TRIGGER_PINS[i], HIGH); // back to idle
    }
}
