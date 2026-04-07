import sqlite3
import requests
import json

# Update this to your actual n8n webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/support-ticket"
def send_payloads():
    conn = sqlite3.connect('data/database.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id, data FROM payloads WHERE sent = 0")
    rows = cursor.fetchall()
    for row in rows:
        payload_id, data = row
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=json.loads(data))
            if response.status_code == 200:
                cursor.execute("UPDATE payloads SET sent = 1 WHERE id = ?", (payload_id,))
                print(f"Payload {payload_id} sent successfully.")
            else:
                print(f"Failed to send payload {payload_id}: {response.status_code}")
        except Exception as e:
            print(f"Error sending payload {payload_id}: {e}")
    conn.commit()
    conn.close()

def insert_payloads():
    conn = sqlite3.connect('data/database.sqlite')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            sent INTEGER DEFAULT 0
        )
    """)
    payloads = [
        {
            "name": "Test User 1",
            "email": "user1@gmail.com",
            "subject": "Test Ticket 1",
            "message": "not getting resposne from server.",
            "attachment": {
                "filename": "example1.pdf",
                "content": "Sample attachment text 1."
            }
        },
        {
            "name": "Test User 2",
            "email": "user2@gmail.com",
            "subject": "Test Ticket 2",
            "message": "hey no response from server.",
            "attachment": None
        }
    ]
    for payload in payloads:
        cursor.execute(
            "INSERT INTO payloads (data, sent) VALUES (?, 0)",
            (json.dumps(payload),)
        )
    conn.commit()
    conn.close()
    print(f"Inserted {len(payloads)} payloads.")

if __name__ == "__main__":
    insert_payloads()
    send_payloads()