/*
   Modified from ROM Reader by Oddbloke (16th Feb 2014) and adapted for 27C256
http://danceswithferrets.org/geekblog/wp-content/uploads/2014/02/RomReader.txt

name:         27C256
function:     32k x 8 paged parallel EPROM.
pinout:
+------()------+
VPP |1           28| VCC
A12 |2           27| A14
A7 |3           26| A13
A6 |4           25| A8
A5 |5           24| A9
A4 |6           23| A11
A3 |7    27256  22| OE
A2 |8           21| A10
A1 |9           20| CE
A0 |10          19| D7
D0 |11          18| D6
D1 |12          17| D5
D2 |13          16| D4
GND |14          15| D3
+--------------+

Tested with a M27C256B, but same pinout
 */

#define FW_END 0x7fffL

static const int kPin_A0  = 53;
static const int kPin_A1  = 51;
static const int kPin_A2  = 49;
static const int kPin_A3  = 47;
static const int kPin_A4  = 45;
static const int kPin_A5  = 43;
static const int kPin_A6  = 41;
static const int kPin_A7  = 39;

static const int kPin_A8  = 46;
static const int kPin_A9  = 48;
static const int kPin_A11 = 50;
static const int kPin_A10 = 52;

static const int kPin_A12 = 40;
static const int kPin_A13 = 42;
static const int kPin_A14 = 44;

static const int kPin_D0 = 32;
static const int kPin_D1 = 34;
static const int kPin_D2 = 36;

static const int kPin_D3 = 30;
static const int kPin_D4 = 28;
static const int kPin_D5 = 26;
static const int kPin_D6 = 24;
static const int kPin_D7 = 22;


// GND/CE/OE should be wired to ground.
// Vpp/Vcc/Vss should be wired to +5 volts.

const char hex[] = {'0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

void setup()
{
        pinMode(kPin_A0, OUTPUT);
        pinMode(kPin_A1, OUTPUT);
        pinMode(kPin_A2, OUTPUT);
        pinMode(kPin_A3, OUTPUT);
        pinMode(kPin_A4, OUTPUT);
        pinMode(kPin_A5, OUTPUT);
        pinMode(kPin_A6, OUTPUT);
        pinMode(kPin_A7, OUTPUT);
        pinMode(kPin_A8, OUTPUT);
        pinMode(kPin_A9, OUTPUT);
        pinMode(kPin_A10, OUTPUT);
        pinMode(kPin_A11, OUTPUT);
        pinMode(kPin_A12, OUTPUT);
        pinMode(kPin_A13, OUTPUT);
        pinMode(kPin_A14, OUTPUT);

        pinMode(kPin_D0, INPUT);
        pinMode(kPin_D1, INPUT);
        pinMode(kPin_D2, INPUT);
        pinMode(kPin_D3, INPUT);
        pinMode(kPin_D4, INPUT);
        pinMode(kPin_D5, INPUT);
        pinMode(kPin_D6, INPUT);
        pinMode(kPin_D7, INPUT);

        pinMode(LED_BUILTIN, OUTPUT);

        Serial.begin(9600);

        for (int i = 0; i < 5; i++) {
                digitalWrite(LED_BUILTIN, HIGH);
                delay(100);
                digitalWrite(LED_BUILTIN, LOW);
                delay(100);
        }
}

void SetAddress(int addr)
{
        // update the address lines to reflect the address we want ...
        digitalWrite(kPin_A0, (addr & 1) ? HIGH : LOW);
        digitalWrite(kPin_A1, (addr & 2) ? HIGH : LOW);
        digitalWrite(kPin_A2, (addr & 4) ? HIGH : LOW);
        digitalWrite(kPin_A3, (addr & 8) ? HIGH : LOW);
        digitalWrite(kPin_A4, (addr & 16) ? HIGH : LOW);
        digitalWrite(kPin_A5, (addr & 32) ? HIGH : LOW);
        digitalWrite(kPin_A6, (addr & 64) ? HIGH : LOW);
        digitalWrite(kPin_A7, (addr & 128) ? HIGH : LOW);
        digitalWrite(kPin_A8, (addr & 256) ? HIGH : LOW);
        digitalWrite(kPin_A9, (addr & 512) ? HIGH : LOW);
        digitalWrite(kPin_A10, (addr & 1024) ? HIGH : LOW);
        digitalWrite(kPin_A11, (addr & 2048) ? HIGH : LOW);
        digitalWrite(kPin_A12, (addr & 4096) ? HIGH : LOW);
        digitalWrite(kPin_A13, (addr & 8192) ? HIGH : LOW);
        digitalWrite(kPin_A14, (addr & 16384) ? HIGH : LOW);
}

byte ReadByte()
{
        // read the current eight-bit byte being output by the ROM ...
        byte b = 0;
        if (digitalRead(kPin_D0)) b |= 1;
        if (digitalRead(kPin_D1)) b |= 2;
        if (digitalRead(kPin_D2)) b |= 4;
        if (digitalRead(kPin_D3)) b |= 8;
        if (digitalRead(kPin_D4)) b |= 16;
        if (digitalRead(kPin_D5)) b |= 32;
        if (digitalRead(kPin_D6)) b |= 64;
        if (digitalRead(kPin_D7)) b |= 128;

        return(b);
}

void loop()
{
        byte d[16];
        byte checksum = 0;

        Serial.println("Reading ROM...\n");

        for (long addr = 0; addr < FW_END + 1; addr += 16)
        {
                digitalWrite(LED_BUILTIN, HIGH);
                // read 16 bytes of data from the ROM ...
                for (long x = 0; x < 16; x++)
                {
                        SetAddress(addr + x); // tells the ROM the byte we want ...
                        delayMicroseconds(1);
                        d[x] = ReadByte(); // reads the byte back from the ROM
                        checksum += d[x];
                }

                digitalWrite(LED_BUILTIN, LOW);
                // now we'll print each byte in hex ...
                for (long y = 0; y < 16; y++)
                {
                        Serial.print("0x");
                        Serial.print(hex[(d[y] & 0xF0) >> 4]);
                        Serial.print(hex[(d[y] & 0x0F)]);
                        Serial.print(", ");
                }

                Serial.println("");
        }

        Serial.print("Checksum: ");
        Serial.println(checksum);

        // All done, so lockup ...
        while (true)
        {
                delay(10000);
        }
}
