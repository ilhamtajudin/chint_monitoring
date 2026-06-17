import time
import struct
from datetime import datetime

import psycopg2
import RPi.GPIO as GPIO

from pymodbus.client import ModbusSerialClient

# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "postgresql://test:sundayaTEST*2023@192.168.100.248:5438/energy_meter"

# =====================================================
# GPIO
# =====================================================

PIN = 14

# =====================================================
# CHINT
# =====================================================

CHINT_PORT = "/dev/ttyACM1"
SLAVE_ID = 2

# Sesuaikan dengan CT Ratio CHINT Anda
CT_RATIO = 30

# =====================================================
# MODBUS
# =====================================================

def create_client():

    return ModbusSerialClient(
        port=CHINT_PORT,
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=1
    )


def read_imp_ep():

    result = client.read_input_registers(
        address=0x401E,
        count=2,
        slave=SLAVE_ID
    )

    if result.isError():
        raise Exception("Read ImpEp Error")

    raw = struct.pack(
        ">HH",
        result.registers[0],
        result.registers[1]
    )

    value = struct.unpack(
        ">f",
        raw
    )[0]

    # Energy dikalikan CT Ratio
    imp_ep = value * CT_RATIO

    return round(imp_ep, 4)

# =====================================================
# DATABASE CONNECT
# =====================================================

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

# =====================================================
# SAVE CYCLE
# =====================================================

def save_cycle(
    cycle_count,
    start_time,
    end_time,
    imp_ep_start,
    imp_ep_end
):

    cycle_time = (
        end_time - start_time
    ).total_seconds()

    energy_kwh = round(
        imp_ep_end - imp_ep_start,
        4
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO power_mol.molding_cycle
        (
            cycle_count,
            start_time,
            end_time,
            cycle_time_sec,
            imp_ep_start,
            imp_ep_end,
            energy_kwh
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            cycle_count,
            start_time,
            end_time,
            cycle_time,
            imp_ep_start,
            imp_ep_end,
            energy_kwh
        )
    )

    cur.close()

    print(
        f"[SAVE] "
        f"Cycle={cycle_count} "
        f"Duration={cycle_time:.2f}s "
        f"Energy={energy_kwh:.4f} kWh"
    )

# =====================================================
# GPIO SETUP
# =====================================================

GPIO.setmode(GPIO.BCM)
GPIO.setup(
    PIN,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP
)

# =====================================================
# MODBUS CONNECT
# =====================================================

client = create_client()

if not client.connect():
    raise Exception(
        f"Gagal konek CHINT di {CHINT_PORT}"
    )

# =====================================================
# INIT
# =====================================================

cycle_count = 0

waiting_high = False

start_time = None

imp_ep_start = None

prev_state = GPIO.input(PIN)

print("====================================")
print("Monitoring molding cycle...")
print("Pattern : LOW -> HIGH -> LOW")
print("====================================")

# =====================================================
# LOOP
# =====================================================

try:

    while True:

        current_state = GPIO.input(PIN)

        # ---------------------------------
        # LOW -> HIGH
        # ---------------------------------

        if (
            prev_state == GPIO.LOW
            and current_state == GPIO.HIGH
        ):

            start_time = datetime.now()

            imp_ep_start = read_imp_ep()

            waiting_high = True

            print(
                f"[START] "
                f"{start_time} "
                f"ImpEp={imp_ep_start:.4f}"
            )

        # ---------------------------------
        # HIGH -> LOW
        # ---------------------------------

        elif (
            waiting_high
            and prev_state == GPIO.HIGH
            and current_state == GPIO.LOW
        ):

            cycle_count += 1

            end_time = datetime.now()

            imp_ep_end = read_imp_ep()

            save_cycle(
                cycle_count,
                start_time,
                end_time,
                imp_ep_start,
                imp_ep_end
            )

            print(
                f"[END] "
                f"{end_time} "
                f"ImpEp={imp_ep_end:.4f}"
            )

            waiting_high = False

        prev_state = current_state

        time.sleep(0.1)

except KeyboardInterrupt:

    print("\nMonitoring stopped.")

finally:

    GPIO.cleanup()

    client.close()

    conn.close()
