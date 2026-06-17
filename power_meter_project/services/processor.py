import json
import time

from services.database_service import (
    save_data,
    save_data_peak
)

from config.register_map import registers

from services.modbus_service import (
    create_client,
    read_holding_int,
    read_realtime_block,
    read_energy_block,
    get_realtime_value,
    get_energy_value
)

# from services.mqtt_service import mqtt_client

from utils.converter import convert_value

from utils.logger import (
    print_header,
    print_error
)

# =====================================================
# PEAK CACHE
# =====================================================

last_peak_values = {}

# =====================================================
# PROCESS DEVICE
# =====================================================

def process_device(
    name,
    port,
    slave_id
):

    client = None

    while True:

        try:

            # =====================================================
            # CONNECT ONCE
            # =====================================================

            if client is None:

                client = create_client(port)

                if not client.connect():

                    print(
                        f"\n{name} CONNECT FAILED"
                    )

                    time.sleep(2)

                    continue

                print(
                    f"{name} CONNECTED"
                )

            start_time = time.time()

            # =====================================================
            # CT RATIO
            # =====================================================

            ct_ratio = read_holding_int(
                client,
                0x0006,
                slave_id
            )

            if ct_ratio <= 0:
                ct_ratio = 1

            print_header(
                name,
                port,
                ct_ratio
            )

            print("-" * 50)

            # =====================================================
            # BULK READ
            # =====================================================

            realtime_regs = read_realtime_block(
                client,
                slave_id
            )

            energy_regs = read_energy_block(
                client,
                slave_id
            )

            # =====================================================
            # PROCESS DATA
            # =====================================================

            data = {}

            for reg_name, addr in registers.items():

                try:

                    # -----------------------------------------
                    # ENERGY BLOCK
                    # -----------------------------------------

                    if addr >= 0x401E:

                        value = get_energy_value(
                            energy_regs,
                            addr
                        )

                    # -----------------------------------------
                    # REALTIME BLOCK
                    # -----------------------------------------

                    else:

                        value = get_realtime_value(
                            realtime_regs,
                            addr
                        )

                    final, unit = convert_value(
                        reg_name,
                        value,
                        ct_ratio
                    )

                    # -----------------------------------------
                    # FORMAT 3 DIGIT
                    # -----------------------------------------

                    if final < 10:

                        final_3_digit = float(
                            f"{final:.2f}"
                        )

                    elif final < 100:

                        final_3_digit = float(
                            f"{final:.1f}"
                        )

                    else:

                        final_3_digit = int(
                            round(final)
                        )

                    data[reg_name] = final_3_digit

                    print(
                        f"[{name}] "
                        f"{reg_name:<6}: "
                        f"{final_3_digit:>10} "
                        f"{unit}"
                    )

                except Exception as e:

                    print(
                        f"[{name}] "
                        f"{reg_name} ERROR : "
                        f"{e}"
                    )

                    data[reg_name] = 0

            # =====================================================
            # SAVE DATABASE
            # =====================================================

            save_data(
                name.lower(),
                data
            )

            print(
                f"{name} SAVE_DATA OK"
            )

            save_data_peak(
                name.lower(),
                data,
                last_peak_values
            )

            print(
                f"{name} PEAK OK"
            )

            print(
                f"DATABASE SAVED -> {name}"
            )

            # =====================================================
            # MQTT
            # =====================================================

            # payload = {
            #     "device": name,
            #     "port": port,
            #     "timestamp": int(time.time()),
            #     "data": data
            # }

            # mqtt_client.publish(
            #     f"power_meter/{name}",
            #     json.dumps(payload),
            #     qos=0,
            #     retain=False
            # )

            # =====================================================
            # PERFORMANCE
            # =====================================================

            elapsed = time.time() - start_time

            print(
                f"{name} LOOP TIME = "
                f"{elapsed:.3f} sec"
            )

        except Exception as e:

            print_error(
                name,
                e
            )

            try:

                if client:

                    client.close()

            except:
                pass

            client = None

            time.sleep(2)

        # =====================================================
        # TARGET SAMPLING
        # =====================================================

        time.sleep(0.5)