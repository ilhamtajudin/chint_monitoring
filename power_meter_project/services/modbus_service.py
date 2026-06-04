from pymodbus.client import ModbusSerialClient
import struct

def create_client(port):

    client = ModbusSerialClient(
        port=port,
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=3
    )

    return client

def read_holding_int(client, address, slave_id):

    result = client.read_holding_registers(
        address=address,
        count=1,
        device_id=1
    )

    if result.isError():
        raise Exception("Modbus Read Error")
    
    return result.registers[0]


def read_float(client, address, slave_id):

    result = client.read_input_registers(
        address=address,
        count=2,
        device_id=1
    )
    
    if result.isError():
        raise Exception("Modbus Read Error")

    regs = result.registers

    raw = struct.pack('>HH', regs[0], regs[1])

    value = struct.unpack('>f', raw)[0]

    return value

def read_holding_int(
    client,
    address,
    slave_id
):

    result = client.read_holding_registers(
        address=address,
        count=1,
        device_id=slave_id
    )

    return result.registers[0]

def read_float(
    client,
    address,
    slave_id
):

    result = client.read_input_registers(
        address=address,
        count=2,
        device_id=slave_id
    )

    regs = result.registers

    raw = struct.pack(
        '>HH',
        regs[0],
        regs[1]
    )

    return struct.unpack(
        '>f',
        raw
    )[0]