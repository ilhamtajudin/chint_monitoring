import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/power_meter.db")
cursor = conn.cursor()

# =========================
# CONFIG LOGS
# =========================
print("\n" + "=" * 70)
print("CONFIG LOGS")
print("=" * 70)

cursor.execute("""
SELECT
    c.id,
    d.name,
    d.ip,
    c.timestamp,
    c.parameter,
    c.value
FROM config_logs c
JOIN devices d ON c.device_id = d.id
ORDER BY c.id DESC
LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:

    readable_time = datetime.fromtimestamp(row[3]).strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-" * 60)
    print(f"ID       : {row[0]}")
    print(f"DEVICE   : {row[1]}")
    print(f"IP       : {row[2]}")
    print(f"TIME     : {readable_time}")
    print(f"PARAM    : {row[4]}")
    print(f"VALUE    : {row[5]}")


# =========================
# DATA LOGS (SNAPSHOT 5 MENIT)
# =========================
print("\n" + "=" * 70)
print("DATA LOGS (5 MIN SNAPSHOT)")
print("=" * 70)

cursor.execute("""
SELECT
    c.id,
    d.name,
    d.ip,
    c.timestamp,
    c.parameter,
    c.value
FROM data_logs c
JOIN devices d ON c.device_id = d.id
ORDER BY c.id DESC
LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:

    readable_time = datetime.fromtimestamp(row[3]).strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-" * 60)
    print(f"ID       : {row[0]}")
    print(f"DEVICE   : {row[1]}")
    print(f"IP       : {row[2]}")
    print(f"TIME     : {readable_time}")
    print(f"PARAM    : {row[4]}")
    print(f"VALUE    : {row[5]}")
    
# =========================
# DATA PEAK (REALTIME PEAK)
# =========================
print("\n" + "=" * 70)
print("DATA PEAK (HIGHEST VALUE DETECTION)")
print("=" * 70)

cursor.execute("""
SELECT
    p.id,
    d.name,
    d.ip,
    p.timestamp,
    p.parameter,
    p.value
FROM data_peak p
JOIN devices d ON p.device_id = d.id
ORDER BY p.id DESC
LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:

    readable_time = datetime.fromtimestamp(row[3]).strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-" * 60)
    print(f"ID       : {row[0]}")
    print(f"DEVICE   : {row[1]}")
    print(f"IP       : {row[2]}")
    print(f"TIME     : {readable_time}")
    print(f"PARAM    : {row[4]}")
    print(f"VALUE    : {row[5]}")

conn.close()