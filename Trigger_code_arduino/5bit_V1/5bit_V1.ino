// 5-bit trigger box for EEG/OpenBCI
// Uses pins 4, 6, 8, 10, 12 as outputs.
// Each code (0–31) received over serial is mapped to the 5 LSBs and pulsed.

const uint8_t NUM_TRIGGER_PINS = 5;
const uint8_t TRIGGER_PINS[NUM_TRIGGER_PINS] = {12, 10, 8, 6, 4};

// Pulse duration in milliseconds
const uint16_t PULSE_MS = 25;

void setup()
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        pinMode(TRIGGER_PINS[i], OUTPUT);
        digitalWrite(TRIGGER_PINS[i], HIGH);
    }

    Serial.begin(115200);
}

void loop()
{
    if (Serial.available() > 0)
    {
        int incoming = Serial.read();   // 0–255
        Serial.print(incoming);

        if (incoming >= 0)
        {
            uint8_t code = static_cast<uint8_t>(incoming) & 0x1F; // 5 bits

            setTriggerPattern(code);
            delay(PULSE_MS);
            clearTriggers();
        }
    }
}

void setTriggerPattern(uint8_t code)
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        bool bitHigh = (code >> i) & 0x01;
        digitalWrite(TRIGGER_PINS[i], bitHigh ? HIGH : LOW);

    }
}

void clearTriggers()
{
    for (uint8_t i = 0; i < NUM_TRIGGER_PINS; ++i)
    {
        digitalWrite(TRIGGER_PINS[i], LOW);
    }
}
