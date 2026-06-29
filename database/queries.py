import sqlite3

DATABASE_NAME = "maintenance.db"


# ==========================
# Database Connection
# ==========================
def connect():
    return sqlite3.connect(DATABASE_NAME)


# ==========================
# Users
# ==========================
def create_user(username, email, password, role):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (username, email, password, role))

    conn.commit()
    conn.close()


def login_user(email, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================
# Predictions
# ==========================
def insert_prediction(engine_id, cycle, prediction, confidence):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (engine_id, cycle, prediction, confidence)
        VALUES (?, ?, ?, ?)
    """, (engine_id, cycle, prediction, confidence))

    conn.commit()
    conn.close()


def get_predictions():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM predictions
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Maintenance
# ==========================
def insert_maintenance(prediction_id, status, recommendation):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO maintenance
        (prediction_id, status, recommendation)
        VALUES (?, ?, ?)
    """, (prediction_id, status, recommendation))

    conn.commit()
    conn.close()


def get_maintenance():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM maintenance
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Dashboard Statistics
# ==========================
def get_dashboard_stats():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='Healthy'")
    healthy = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='Needs Maintenance'")
    needs_maintenance = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='Critical'")
    critical = cursor.fetchone()[0]

    conn.close()

    return {
        "Total Predictions": total_predictions,
        "Healthy": healthy,
        "Needs Maintenance": needs_maintenance,
        "Critical": critical
    }

if __name__ == "__main__":

    # Insert Prediction
    insert_prediction(
        engine_id=1,
        cycle=150,
        prediction="Critical",
        confidence=98.5
    )

    print("Prediction added successfully!")

    predictions = get_predictions()

    print(predictions)