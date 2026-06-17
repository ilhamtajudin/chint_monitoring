from pymodbus.client import ModbusSerialClient

ports = [
    "/dev/ttyACM0",
    "/dev/ttyACM1",
    "/dev/ttyACM2",
    "/dev/ttyACM3",
    "/dev/ttyACM4",
    "/dev/ttyACM5",
]

for port in ports:

    print(f"\n===== {port} =====")

    client = ModbusSerialClient(
        port=port,
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    client.connect()

    for slave in range(1, 20):

        try:
            result = client.read_input_registers(
                address=0x2000,
                count=2,
                slave=slave
            )

            if not result.isError():
                print(f"FOUND SLAVE {slave}")

        except:
            pass

    client.close()
