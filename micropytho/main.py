# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script initializes the E220 LoRa module with MicroPython,
# retrieves the current configuration, and prints it to the console.
# The code demonstrates how to use the LoRaE32 library to interact with the module and read its configuration.
#
# Note: This code was written and tested using MicroPython on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

import utime
from machine import UART, Pin

from lora_e220 import LoRaE220, print_configuration, Configuration
from lora_e220_operation_constant import ResponseStatusCode
from lora_e220_constants import (
    OperatingFrequency,
    FixedTransmission,
    TransmissionPower,
    AirDataRate,
    UARTParity,
    UARTBaudRate,
    RssiAmbientNoiseEnable,
    SubPacketSetting,
    WorPeriod,
    LbtEnableByte,
    RssiEnableByte,
    TransmissionPower22,
)

uart2 = UART(1)
lora = LoRaE220("900T22D", uart2, aux_pin=2, m0_pin=10, m1_pin=11)

code = lora.begin()
print("Initialization: ", ResponseStatusCode.get_description(code))


configuration_to_set = Configuration("900T22D")
configuration_to_set.CHAN = 19
configuration_to_set.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_000_24
configuration_to_set.OPTION.transmissionPower = (
    TransmissionPower("900T22D").get_transmission_power().POWER_17
)
configuration_to_set.ADDH = 0x00 # Address of this receive no sender
configuration_to_set.ADDL = 0x01 # Address of this receive no sender
configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
configuration_to_set.OPTION.subPacketSetting = SubPacketSetting.SPS_032_11
code, confSetted = lora.set_configuration(configuration_to_set)


code, configuration = lora.get_configuration()


print("Retrieve configuration: ", ResponseStatusCode.get_description(code))

print_configuration(configuration)


print("Waiting for messages...")

led = Pin(25, Pin.OUT)
led.value(0)

while True:

    if lora.available() > 0:
      code, mesg = lora.receive_message()

      if mesg == 'H':
        led.value(1)
        utime.sleep_ms(500)
        led.value(0)

      elif mesg == 'L':
        led.value(1)
        utime.sleep_ms(500)
        led.value(0)
