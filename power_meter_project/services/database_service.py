import threading
import psycopg2

from config.database_config import DATABASE_URL

# =====================================================
# ALLOWED TABLES
# =====================================================

ALLOWED_TABLES = [
    "chint_1",
    "chint_2",
    "chint_3",
    "chint_4",
    "chint_5",
    "chint_6"
]

# =====================================================
# THREAD LOCAL STORAGE
# =====================================================

thread_local = threading.local()

# =====================================================
# GET CONNECTION PER THREAD
# =====================================================

def get_connection():

    try:

        if not hasattr(thread_local, "conn"):

            print(
                f"NEW DB CONNECTION -> "
                f"{threading.current_thread().name}"
            )

            conn = psycopg2.connect(
                DATABASE_URL,
                connect_timeout=5
            )

            conn.autocommit = False

            thread_local.conn = conn

        return thread_local.conn

    except Exception as e:

        print("GET CONNECTION ERROR:", e)

        raise


# =====================================================
# INIT DATABASE (RUN ONCE)
# =====================================================

def connect_db():

    conn = None
    cursor = None

    try:

        print("DB STEP 1")

        conn = psycopg2.connect(
            DATABASE_URL,
            connect_timeout=5
        )

        print("DB STEP 2")

        cursor = conn.cursor()

        print("DB STEP 3")

        cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS power_mol
        """)

        print("DB STEP 4")

        cursor.execute("""
        SET search_path TO power_mol
        """)

        print("DB STEP 5")

        for table_name in ALLOWED_TABLES:

            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (

                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT NOW(),

                Ua DOUBLE PRECISION,
                Ub DOUBLE PRECISION,
                Uc DOUBLE PRECISION,

                Uab DOUBLE PRECISION,
                Ubc DOUBLE PRECISION,
                Uca DOUBLE PRECISION,

                Ia DOUBLE PRECISION,
                Ib DOUBLE PRECISION,
                Ic DOUBLE PRECISION,

                Pt DOUBLE PRECISION,

                Pa DOUBLE PRECISION,
                Pb DOUBLE PRECISION,
                Pc DOUBLE PRECISION,

                Qa DOUBLE PRECISION,
                Qb DOUBLE PRECISION,
                Qc DOUBLE PRECISION,

                PFa DOUBLE PRECISION,
                PFb DOUBLE PRECISION,
                PFc DOUBLE PRECISION,
                PFt DOUBLE PRECISION,

                Freq DOUBLE PRECISION,

                ImpEp DOUBLE PRECISION,
                ExpEp DOUBLE PRECISION,

                Q1Eq DOUBLE PRECISION,
                Q2Eq DOUBLE PRECISION,
                Q3Eq DOUBLE PRECISION,
                Q4Eq DOUBLE PRECISION
            )
            """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_peak (

            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),

            device_name VARCHAR(50),
            parameter VARCHAR(50),
            value DOUBLE PRECISION
        )
        """)

        conn.commit()

        print("PostgreSQL Connected")

    except Exception as e:

        print("DATABASE CONNECTION ERROR:", e)

    finally:

        try:
            if cursor:
                cursor.close()
        except:
            pass

        try:
            if conn:
                conn.close()
        except:
            pass


# =====================================================
# RUN ONCE AT STARTUP
# =====================================================

connect_db()

# =====================================================
# SAVE REALTIME DATA
# =====================================================

def save_data(device_name, data):

    conn = None
    cursor = None

    try:

        if device_name not in ALLOWED_TABLES:
            raise Exception(f"Invalid table name: {device_name}")

        conn = get_connection()

        cursor = conn.cursor()

        query = f"""
        INSERT INTO power_mol.{device_name} (

            ua,ub,uc,
            uab,ubc,uca,

            ia,ib,ic,

            pt,

            pa,pb,pc,

            qa,qb,qc,

            pfa,pfb,pfc,pft,

            freq,

            impep,expep,

            q1eq,q2eq,q3eq,q4eq

        ) VALUES (

            %s,%s,%s,
            %s,%s,%s,

            %s,%s,%s,

            %s,

            %s,%s,%s,

            %s,%s,%s,

            %s,%s,%s,%s,

            %s,

            %s,%s,

            %s,%s,%s,%s
        )
        """

        values = (

            float(data.get("Ua", 0)),
            float(data.get("Ub", 0)),
            float(data.get("Uc", 0)),

            float(data.get("Uab", 0)),
            float(data.get("Ubc", 0)),
            float(data.get("Uca", 0)),

            float(data.get("Ia", 0)),
            float(data.get("Ib", 0)),
            float(data.get("Ic", 0)),

            float(data.get("Pt", 0)),

            float(data.get("Pa", 0)),
            float(data.get("Pb", 0)),
            float(data.get("Pc", 0)),

            float(data.get("Qa", 0)),
            float(data.get("Qb", 0)),
            float(data.get("Qc", 0)),

            float(data.get("PFa", 0)),
            float(data.get("PFb", 0)),
            float(data.get("PFc", 0)),
            float(data.get("PFt", 0)),

            float(data.get("Freq", 0)),

            float(data.get("ImpEp", 0)),
            float(data.get("ExpEp", 0)),

            float(data.get("Q1Eq", 0)),
            float(data.get("Q2Eq", 0)),
            float(data.get("Q3Eq", 0)),
            float(data.get("Q4Eq", 0))
        )

        cursor.execute(query, values)

        conn.commit()

    except Exception as e:

        print(
            f"[{device_name}] SAVE ERROR:",
            e
        )

        try:
            conn.rollback()
        except:
            pass

        try:
            if hasattr(thread_local, "conn"):
                thread_local.conn.close()
                del thread_local.conn
        except:
            pass

    finally:

        try:
            if cursor:
                cursor.close()
        except:
            pass


# =====================================================
# SAVE PEAK DATA
# =====================================================

def save_data_peak(
    device_name,
    data,
    last_peak_values
):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        for key, value in data.items():

            try:
                value = float(value)
            except:
                continue

            map_key = f"{device_name}_{key}"

            last_value = last_peak_values.get(map_key)

            if last_value is None:

                last_peak_values[map_key] = value
                continue

            if value > last_value:

                cursor.execute("""
                INSERT INTO power_mol.data_peak (

                    device_name,
                    parameter,
                    value

                ) VALUES (%s,%s,%s)
                """, (
                    device_name,
                    key,
                    value
                ))

                last_peak_values[map_key] = value

        conn.commit()

    except Exception as e:

        print(
            f"[{device_name}] PEAK ERROR:",
            e
        )

        try:
            conn.rollback()
        except:
            pass

        try:
            if hasattr(thread_local, "conn"):
                thread_local.conn.close()
                del thread_local.conn
        except:
            pass

    finally:

        try:
            if cursor:
                cursor.close()
        except:
            pass