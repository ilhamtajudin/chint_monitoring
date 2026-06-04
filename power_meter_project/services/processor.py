import json
import time
print("PROC 1")
from services.database_service import (
    save_data,
    save_data_peak
)
print("PROC 2")
from config.register_map import registers
print("PROC 3")
from services.modbus_service import (
    create_client,
    read_holding_int,
    read_float
)
print("PROC 4")
# from services.mqtt_service import mqtt_client
print("PROC 5")
from utils.converter import convert_value
from utils.logger import (
    print_header,
    print_error
)

# =========================
# PEAK CACHE
# =========================
last_peak_values = {}

# =========================
# PROCESS DEVICE
# =========================
def process_device(name, port, slave_id):

    while True:

        try:

            # =========================
            # CONNECT MODBUS
            # =========================
            client = create_client(port)

            if not client.connect():

                print(f"\n{name} CONNECT FAILED")

                time.sleep(2)

                continue

            # =========================
            # CT RATIO
            # =========================
            ct_ratio = read_holding_int(client, 0x0006, slave_id)
            if ct_ratio <= 0:
                ct_ratio = 1

            print_header(name, port, ct_ratio)

            print("-" * 50)

            # =========================
            # REALTIME DATA
            # =========================
            data = {}

            for reg_name, addr in registers.items():

                try:

                    value = read_float(client, addr, slave_id)

                    final, unit = convert_value(
                        reg_name,
                        value,
                        ct_ratio
                    )

                    # -------------------------------------------------------
                    # TEMPAT MENAMBAHKAN KODE PEMBATASAN 3 DIGIT
                    # -------------------------------------------------------
                    # -------------------------------------------------------
                    # TEMPAT MENAMBAHKAN KODE PEMBATASAN 3 DIGIT (FIXED)
                    # -------------------------------------------------------
                    if final < 10:
                        # Maksimal 2 angka di belakang koma (Contoh: 4.52)
                        final_3_digit = float(f"{final:.2f}")
                    elif final < 100:
                        # Maksimal 1 angka di belakang koma (Contoh: 10.6)
                        final_3_digit = float(f"{final:.1f}")
                    else:
                        # Tanpa angka di belakang koma (Contoh: 220)
                        final_3_digit = int(round(final))

                    # Simpan hasil yang sudah diformat ke dalam database & MQTT
                    data[reg_name] = final_3_digit

                    # Menampilkan hasil di terminal dengan format baru
                    print(f"[{name}] {reg_name:<5}: {final_3_digit:>10} {unit}")

                except Exception:

                    data[reg_name] = 0

                    print(f"{reg_name:<5}: ERROR")

            # =========================
            # CLOSE MODBUS
            # =========================
            client.close()
            print(f"{name} READ COMPLETE")

            # =========================
            # MQTT PAYLOAD
            # =========================
            # payload = {
            #    "device": name,
            #    "port": port,
            #    "timestamp": int(time.time()),
            #    "data": data
            #}

            # =========================
            # MQTT PUBLISH
            # =========================
            #mqtt_client.publish(
            #    f"power_meter/{name}",
            #    json.dumps(payload),
            #    qos=0,
            #    retain=False
            #)

            #print("-" * 50)
            #print(f"MQTT SENT -> power_meter/{name}")

            # =========================
            # SAVE DATABASE
            # =========================
            save_data(
                name.lower(),
                data
            )
            print(f"{name} SAVE_DATA OK")

            save_data_peak(
                name.lower(),
                data,
                last_peak_values
            )
            print(f"{name} PEAK OK")

            print(f"DATABASE SAVED -> {name}")

        except Exception as e:

            print_error(name, e)

        # =========================
        # DELAY 1 DETIK
        # =========================
        time.sleep(1)
