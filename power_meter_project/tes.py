from pymodbus.client import ModbusSerialClient
import logging

# Matikan log pymodbus
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

ports = [f"/dev/ttyACM{i}" for i in range(8)]

for port in ports:

    client = ModbusSerialClient(
        port=port,
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    if not client.connect():
        continue

    for slave in range(1, 11):

        try:
            result = client.read_input_registers(
                address=0x2006,  # Ua
                count=2,
                device_id=slave
            )

            if not result.isError():
                print(
                    f"FOUND -> PORT={port} "
                    f"SLAVE={slave}"
                )

        except:
            pass

    client.close()