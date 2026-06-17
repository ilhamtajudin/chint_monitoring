import time
from datetime import datetime

import psycopg2
import RPi.GPIO as GPIO

DATABASE_URL = "postgresql://test:sundayaTEST*2023@192.168.100.248:5438/energy_meter"

PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

cycle_count = 0

# state machine
waiting_high = False
start_time = None

prev_state = GPIO.input(PIN)

print("Monitoring molding cycle...")

def save_cycle(cycle_count, start_time, end_time):

    cycle_time = (
        end_time - start_time
    ).total_seconds()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO power_mol.molding_cycle
        (
            cycle_count,
            start_time,
            end_time,
            cycle_time_sec
        )
        VALUES
        (
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
            cycle_time
        )
    )

    cur.close()

    print(
        f"SAVE Cycle #{cycle_count} "
        f"Duration={cycle_time:.2f} sec"
    )


try:

    while True:

        current_state = GPIO.input(PIN)

        # ===================================
        # LOW -> HIGH
        # ===================================
        if (
            prev_state == GPIO.LOW
            and current_state == GPIO.HIGH
        ):

            waiting_high = True

            print(
                "LOW -> HIGH",
                datetime.now()
            )

        # ===================================
        # HIGH -> LOW
        # setelah sebelumnya LOW -> HIGH
        # ===================================
        elif (
            waiting_high
            and prev_state == GPIO.HIGH
            and current_state == GPIO.LOW
        ):

            cycle_count += 1

            end_time = datetime.now()

            if start_time is None:
                start_time = end_time

            save_cycle(
                cycle_count,
                start_time,
                end_time
            )

            start_time = end_time

            waiting_high = False

            print(
                f"CYCLE #{cycle_count} COMPLETE"
            )

        prev_state = current_state

        time.sleep(0.1)

except KeyboardInterrupt:

    GPIO.cleanup()
    conn.close()
