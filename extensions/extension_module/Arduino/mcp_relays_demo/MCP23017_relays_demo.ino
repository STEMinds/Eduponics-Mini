/**
 * On every loop, the state of the port B is copied to port A.
 *
 * Use active low inputs on port A. Internal pullups are enabled by default by the library so there is no need for external resistors.
 * Place LEDS on port B for instance.
 * When pressing a button, the corresponding led is shut down.
 *
 * You can also uncomment one line to invert the input (when pressing a button the corresponding led is lit)
 */
#include <Wire.h>
#include <MCP23017.h>

#define MCP23017_ADDR 0x20
MCP23017 mcp = MCP23017(MCP23017_ADDR);

void setup() {
    Wire.begin(33,32);
    Serial.begin(115200);

    mcp.init();

    mcp.portMode(MCP23017Port::A, 0); //Port A as output
    mcp.portMode(MCP23017Port::B, 0); //Port B as output
    mcp.portMode(MCP23017Port::C, 0); //Port C as output
    mcp.portMode(MCP23017Port::D, 0); //Port D as output

    mcp.writeRegister(MCP23017Register::GPIO_A, 0x00);  //Reset port A
    mcp.writeRegister(MCP23017Register::GPIO_B, 0x00);  //Reset port B
    mcp.writeRegister(MCP23017Register::GPIO_C, 0x00);  //Reset port C
    mcp.writeRegister(MCP23017Register::GPIO_D, 0x00);  //Reset port D
}

void loop() {
    // open relay A
    mcp.writePort(MCP23017Port::A, 1);
    delay(500);
    // open relay B
    mcp.writePort(MCP23017Port::B, 1);
    delay(500);
    // open relay C
    mcp.writePort(MCP23017Port::C, 1);
    delay(500);
    // open relay D
    mcp.writePort(MCP23017Port::D, 1);
    delay(500);
    // close relay A
    mcp.writePort(MCP23017Port::A, 0);
    delay(500);
    // close relay B
    mcp.writePort(MCP23017Port::B, 0);
    delay(500);
    // close relay C
    mcp.writePort(MCP23017Port::C, 0);
    delay(500);
    // close relay D
    mcp.writePort(MCP23017Port::D, 0);
    delay(500);
}
