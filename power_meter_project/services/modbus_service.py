from pymodbus.client import ModbusSerialClient
import struct

# =====================================================
# CLIENT
# =====================================================

def create_client(port):

    return ModbusSerialClient(
        port=port,
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=0.5
    )


# =====================================================
# HOLDING REGISTER
# =====================================================

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

    if result.isError():
        raise Exception(
            f"Holding Register Error {address}"
        )

    return result.registers[0]


# =====================================================
# FLOAT DECODER
# =====================================================

def decode_float(
    regs,
    offset
):

    raw = struct.pack(
        '>HH',
        regs[offset],
        regs[offset + 1]
    )

    return struct.unpack(
        '>f',
        raw
    )[0]


# =====================================================
# BULK READ REALTIME
# 0x2000 - 0x2051
# =====================================================

def read_realtime_block(
    client,
    slave_id
):

    result = client.read_input_registers(
        address=0x2000,
        count=82,
        device_id=slave_id
    )

    if result.isError():
        raise Exception(
            "Realtime Block Read Error"
        )

    return result.registers


# =====================================================
# BULK READ ENERGY
# 0x401E - 0x4051
# =====================================================

def read_energy_block(
    client,
    slave_id
):

    result = client.read_input_registers(
        address=0x401E,
        count=52,
        device_id=slave_id
    )

    if result.isError():
        raise Exception(
            "Energy Block Read Error"
        )

    return result.registers


# =====================================================
# READ FLOAT FROM REALTIME BLOCK
# =====================================================

def get_realtime_value(
    regs,
    address
):

    offset = address - 0x2000

    return decode_float(
        regs,
        offset
    )


# =====================================================
# READ FLOAT FROM ENERGY BLOCK
# =====================================================

def get_energy_value(
    regs,
    address
):

    offset = address - 0x401E

    return decode_float(
        regs,
        offset
    )