from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import re

app = Flask(__name__)
CORS(app)

# =====================================================
# DATABASE CONFIG
# =====================================================

DB_CONFIG = {
    "host": "192.168.100.248",
    "port": 5438,
    "database": "energy_meter",
    "user": "test",
    "password": "sundayaTEST*2023"
}

# =====================================================
# ALLOWED DEVICES
# =====================================================

ALLOWED_DEVICES = [
    "chint_1",
    "chint_2",
    "chint_3",
    "chint_4",
    "chint_5",
    "chint_6"
]

# =====================================================
# CONNECTION
# =====================================================

def get_connection():

    try:

        conn = psycopg2.connect(**DB_CONFIG)

        with conn.cursor() as cur:
            cur.execute("""
                SET search_path TO power_mol, public;
            """)

        return conn

    except Exception as e:

        print("DATABASE ERROR:", e)
        return None


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/")
def home():

    return jsonify({
        "status": "ok",
        "service": "CHINT API"
    })


# =====================================================
# REALTIME DATA
# URL:
# /api/chint_1
# /api/chint_2
# =====================================================

@app.route("/api/<device>")
def get_data(device):

    device = device.lower()

    if device not in ALLOWED_DEVICES:

        return jsonify({
            "error": "Device tidak valid"
        }), 400

    conn = get_connection()

    if conn is None:

        return jsonify({
            "error": "Database connection failed"
        }), 500

    try:

        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        query = f"""
            SELECT *
            FROM power_mol.{device}
            ORDER BY created_at DESC
            LIMIT 100
        """

        cur.execute(query)

        rows = cur.fetchall()

        cur.close()

        return jsonify(rows)

    except Exception as e:

        print("GET DATA ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conn.close()


# =====================================================
# DATA PEAK
# URL:
# /api/data_peak/chint_1
# =====================================================

@app.route("/api/data_peak/<device>")
def get_data_peak(device):

    device = device.lower()

    if device not in ALLOWED_DEVICES:

        return jsonify({
            "error": "Device tidak valid"
        }), 400

    conn = get_connection()

    if conn is None:

        return jsonify({
            "error": "Database connection failed"
        }), 500

    try:

        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        query = """
            SELECT
                id,
                created_at,
                device_name,
                parameter,
                value
            FROM power_mol.data_peak
            WHERE device_name = %s
            ORDER BY created_at DESC
            LIMIT 410
        """

        cur.execute(query, (device,))

        rows = cur.fetchall()

        cur.close()

        return jsonify(rows)

    except Exception as e:

        print("DATA PEAK ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conn.close()


# =====================================================
# LATEST DATA
# URL:
# /api/latest/chint_1
# =====================================================

@app.route("/api/latest/<device>")
def get_latest(device):

    device = device.lower()

    if device not in ALLOWED_DEVICES:

        return jsonify({
            "error": "Device tidak valid"
        }), 400

    conn = get_connection()

    if conn is None:

        return jsonify({
            "error": "Database connection failed"
        }), 500

    try:

        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        query = f"""
            SELECT *
            FROM power_mol.{device}
            ORDER BY created_at DESC
            LIMIT 1
        """

        cur.execute(query)

        row = cur.fetchone()

        cur.close()

        return jsonify(row)

    except Exception as e:

        print("LATEST ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conn.close()


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )