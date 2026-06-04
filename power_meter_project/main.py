print("STEP 1")

import threading
import time

print("STEP 2")

from config.device_config import devices

print("STEP 3")

from services.processor import process_device

print("STEP 4")

for name, config in devices.items():

    print("START THREAD:", name)

    thread = threading.Thread(
        target=process_device,
        args=(
            name,
            config["port"],
            config["slave_id"]
        ),
        daemon=True
    )

    thread.start()

print("STEP 5")

while True:
    time.sleep(1)