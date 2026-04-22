import sqlite3
import requests
import json
import time
from datetime import datetime
import sys
import os

# n8n webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/support-ticket"
# For production: N8N_WEBHOOK_URL = "http://localhost:5678/webhook/support-ticket"

# n8n API URL to check execution status
N8N_API_URL = "http://localhost:5678/api/v1"
N8N_API_KEY = ""  # Add your n8n API key if authentication is enabled

def test_webhook_connection():
    """Test if webhook is reachable and accepts POST requests"""
    test_payload = {
        "name": "Connection Test",
        "email": "test@test.com",
        "subject": "Test Connection",
        "message": "Testing webhook connection"
    }
    
    try:
        print(f"Testing webhook connection to: {N8N_WEBHOOK_URL}")
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Webhook is reachable and accepting POST requests")
            return True
        else:
            print(f"✗ Webhook returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to {N8N_WEBHOOK_URL}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def create_database():
    """Create database for tracking tickets with execution status"""
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS tickets")
    cursor.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            urgency TEXT,
            ticket_id TEXT,
            execution_id TEXT,
            sent INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            sent_at TIMESTAMP,
            completed_at TIMESTAMP,
            response TEXT,
            status_code INTEGER,
            execution_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create a status tracking table for the sender
    cursor.execute("DROP TABLE IF EXISTS sender_state")
    cursor.execute("""
        CREATE TABLE sender_state (
            id INTEGER PRIMARY KEY,
            is_running INTEGER DEFAULT 0,
            current_ticket_id INTEGER,
            last_run TIMESTAMP
        )
    """)
    
    cursor.execute("INSERT INTO sender_state (id, is_running) VALUES (1, 0)")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def insert_tickets():
    """Insert ONE ticket for each urgency level (High, Medium, Low)"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    
    tickets = [
        # HIGH URGENCY TICKET (Only 1)
        {
            "name": "Emergency User",
            "email": "emergency@company.com",
            "subject": "CRITICAL: Production system is completely down",
            "message": "Our entire production system is down! All customers are affected. No one can access the platform. This is a critical emergency requiring immediate attention.",
            "urgency_hint": "high"
        },
        
        # MEDIUM URGENCY TICKET (Only 1)
        {
            "name": "Regular User",
            "email": "user@example.com",
            "subject": "API rate limiting issue",
            "message": "We are hitting API rate limits during peak hours. This is causing some delays but not completely blocking us. Can we increase our quota when you have time?",
            "urgency_hint": "medium"
        },
        
        # LOW URGENCY TICKET (Only 1)
        {
            "name": "Casual User",
            "email": "casual@example.com",
            "subject": "Dark mode feature request",
            "message": "Would be nice to have dark mode for late night work. No rush on this at all. Just a suggestion for future improvement.",
            "urgency_hint": "low"
        },
        #corrupted email to test validation
        {
            "name": "Casual User",
            "email": "casualgmail.com",
            "subject": "Dark mode feature request",
            "message": "Would be nice to have dark mode for late night work. No rush on this at all. Just a suggestion for future improvement.",
            "urgency_hint": "validation_test"
        }
    ]
    
    for ticket in tickets:
        # Remove urgency_hint before inserting (not sent to webhook)
        ticket_data = {
            "name": ticket["name"],
            "email": ticket["email"],
            "subject": ticket["subject"],
            "message": ticket["message"]
        }
        cursor.execute("""
            INSERT INTO tickets (name, email, subject, message, sent, completed) 
            VALUES (?, ?, ?, ?, 0, 0)
        """, (ticket_data['name'], ticket_data['email'], ticket_data['subject'], ticket_data['message']))
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(tickets)} tickets (1 High, 1 Medium, 1 Low)")

def get_pending_tickets():
    """Get tickets that haven been sent OR sent but not completed"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, email, subject, message, sent, completed 
        FROM tickets 
        WHERE sent = 0 OR (sent = 1 AND completed = 0)
        ORDER BY id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_ticket_sent(ticket_id, execution_id=None):
    """Mark a ticket as sent to n8n"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tickets 
        SET sent = 1, sent_at = ?, execution_id = ?
        WHERE id = ?
    """, (datetime.now().isoformat(), execution_id, ticket_id))
    conn.commit()
    conn.close()

def mark_ticket_completed(ticket_id, ticket_id_n8n, urgency, response_text, status_code):
    """Mark a ticket as completed by n8n workflow"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tickets 
        SET completed = 1, completed_at = ?, ticket_id = ?, urgency = ?, 
            response = ?, status_code = ?
        WHERE id = ?
    """, (datetime.now().isoformat(), ticket_id_n8n, urgency, response_text[:500], status_code, ticket_id))
    conn.commit()
    conn.close()

def update_sender_state(is_running, current_ticket_id=None):
    """Update the sender's running state"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sender_state 
        SET is_running = ?, current_ticket_id = ?, last_run = ?
        WHERE id = 1
    """, (1 if is_running else 0, current_ticket_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_sender_state():
    """Get the sender's current state"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT is_running, current_ticket_id, last_run FROM sender_state WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return {'is_running': row[0] == 1, 'current_ticket_id': row[1], 'last_run': row[2]}

def get_urgency_label(ticket_id):
    """Get urgency label for a ticket based on ID"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT subject FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        subject = row[0].lower()
        if 'critical' in subject or 'down' in subject:
            return "🔴 HIGH"
        elif 'api' in subject or 'rate' in subject:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"
    return "⚪ UNKNOWN"

def send_tickets_with_wait(delay_between=3, wait_for_completion=True, max_timeout=120):
    """
    Send tickets and wait for each workflow to complete before sending next
    """
    # Check if already running
    state = get_sender_state()
    if state['is_running']:
        print(f"\n⚠️ Sender is already running!")
        print(f"   Started at: {state['last_run']}")
        print(f"   Current ticket: {state['current_ticket_id']}")
        print("\nTo force restart, run: python script.py reset-sender")
        return
    
    # Mark as running
    update_sender_state(True)
    
    try:
        # Get tickets to process
        pending = get_pending_tickets()
        
        if not pending:
            print("No pending tickets to send.")
            update_sender_state(False)
            return
        
        total = len(pending)
        print(f"\n{'='*70}")
        print(f"PROCESSING {total} TICKETS (1 High, 1 Medium, 1 Low)")
        print(f"{'='*70}")
        print(f"Webhook URL: {N8N_WEBHOOK_URL}")
        print(f"Wait for completion: {wait_for_completion}")
        print(f"Delay between tickets: {delay_between}s")
        print(f"{'='*70}\n")
        
        results = {
            'success': [],
            'failed': [],
            'urgencies': {'high': 0, 'medium': 0, 'low': 0}
        }
        
        for index, (ticket_id, name, email, subject, message, sent, completed) in enumerate(pending, 1):
            urgency_label = get_urgency_label(ticket_id)
            
            print(f"[{index}/{total}] Processing Ticket ID: {ticket_id} {urgency_label}")
            print(f"  Subject: {subject[:60]}...")
            print(f"  Status: Sent={sent}, Completed={completed}")
            
            # Update current ticket in state
            update_sender_state(True, ticket_id)
            
            # If already sent but not completed, just wait for completion
            if sent == 1 and completed == 0:
                print(f"  ⏳ Ticket already sent, waiting for completion...")
            else:
                # Send new ticket
                payload = {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
                
                try:
                    print(f"  📤 Sending to n8n...")
                    start_time = time.time()
                    
                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )
                    
                    execution_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        try:
                            resp_json = response.json()
                            ticket_id_n8n = resp_json.get('ticket_id')
                            urgency = resp_json.get('urgency', 'unknown')
                            execution_id = resp_json.get('execution_id', f"exec_{ticket_id}_{int(time.time())}")
                        except:
                            ticket_id_n8n = None
                            urgency = 'unknown'
                            execution_id = f"exec_{ticket_id}_{int(time.time())}"
                        
                        mark_ticket_sent(ticket_id, execution_id)
                        print(f"  ✓ Sent successfully (took {execution_time:.2f}s)")
                        print(f"    AI Urgency: {urgency.upper()}")
                        
                        if ticket_id_n8n:
                            print(f"    Ticket ID: {ticket_id_n8n}")
                        
                        if wait_for_completion:
                            print(f"  ⏳ Waiting for n8n workflow to complete...")
                            time.sleep(delay_between)
                            
                            # Simulate wait for completion
                            wait_start = time.time()
                            while time.time() - wait_start < max_timeout:
                                time.sleep(2)
                                elapsed = int(time.time() - wait_start)
                                print(f"     Processing... ({elapsed}s)", end='\r')
                                
                                # For now, wait a reasonable time
                                if elapsed >= 15:  # Wait 15 seconds for processing
                                    break
                            
                            print(f"\n  ✓ Workflow completed")
                            
                            # Mark as completed
                            mark_ticket_completed(ticket_id, ticket_id_n8n, urgency, response.text, response.status_code)
                            
                            # Update results
                            if urgency.lower() in results['urgencies']:
                                results['urgencies'][urgency.lower()] += 1
                            
                            results['success'].append({
                                'id': ticket_id,
                                'ticket_id': ticket_id_n8n,
                                'urgency': urgency
                            })
                    else:
                        print(f"  ✗ Failed - HTTP {response.status_code}")
                        results['failed'].append({'id': ticket_id, 'status': response.status_code})
                        
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    results['failed'].append({'id': ticket_id, 'error': str(e)})
            
            # Wait before next ticket
            if index < total:
                print(f"\n  Waiting {delay_between} seconds before next ticket...")
                time.sleep(delay_between)
            print()
        
        # Print summary
        print(f"{'='*70}")
        print("FINAL SUMMARY")
        print(f"{'='*70}")
        print(f"Total tickets processed: {len(results['success'])}/{total}")
        print(f"Successful: {len(results['success'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['urgencies']:
            print(f"\nAI-Determined Urgency Distribution:")
            print(f"  🔴 HIGH:   {results['urgencies'].get('high', 0)}")
            print(f"  🟡 MEDIUM: {results['urgencies'].get('medium', 0)}")
            print(f"  🟢 LOW:    {results['urgencies'].get('low', 0)}")
        
    finally:
        # Mark as not running
        update_sender_state(False)
        print("\n✓ Sender finished. Ready for next run.")

def view_results():
    """View all tickets with their status"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, subject, urgency, ticket_id, sent, completed, status_code, sent_at, completed_at
        FROM tickets 
        ORDER BY id
    """)
    rows = cursor.fetchall()
    
    if rows:
        print(f"\n{'='*90}")
        print("TICKETS STATUS")
        print(f"{'='*90}")
        for row in rows:
            sent_status = "✓" if row[5] else "⏳"
            comp_status = "✓" if row[6] else "⏳"
            urgency_display = str(row[3]).upper() if row[3] else "PENDING"
            
            # Add emoji based on urgency
            if row[3] == 'high':
                emoji = "🔴"
            elif row[3] == 'medium':
                emoji = "🟡"
            elif row[3] == 'low':
                emoji = "🟢"
            else:
                emoji = "⚪"
            
            print(f"{sent_status}{comp_status} {emoji} ID:{row[0]} | {row[1][:15]} | Urgency: {urgency_display:7} | Ticket: {row[4] or 'N/A'}")
    else:
        print("No tickets found.")
    
    conn.close()

def reset_all():
    """Reset all tickets to unsent state"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET sent = 0, completed = 0, sent_at = NULL, completed_at = NULL, ticket_id = NULL, urgency = NULL, execution_id = NULL, response = NULL, status_code = NULL")
    cursor.execute("UPDATE sender_state SET is_running = 0, current_ticket_id = NULL")
    conn.commit()
    conn.close()
    print("All tickets and sender state have been reset.")

def reset_sender():
    """Reset only the sender state (if stuck)"""
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE sender_state SET is_running = 0, current_ticket_id = NULL")
    conn.commit()
    conn.close()
    print("Sender state has been reset. You can now run the script again.")

def show_status():
    """Show current sender status"""
    state = get_sender_state()
    conn = sqlite3.connect('data/tickets.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE sent = 0")
    pending_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE sent = 1 AND completed = 0")
    processing_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n{'='*50}")
    print("SENDER STATUS")
    print(f"{'='*50}")
    print(f"Is Running: {state['is_running']}")
    print(f"Current Ticket: {state['current_ticket_id']}")
    print(f"Last Run: {state['last_run']}")
    print(f"Pending Tickets: {pending_count}")
    print(f"Processing Tickets: {processing_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "reset":
            reset_all()
        elif command == "reset-sender":
            reset_sender()
        elif command == "status":
            show_status()
        elif command == "results":
            view_results()
        elif command == "insert":
            create_database()
            insert_tickets()
        elif command == "send":
            send_tickets_with_wait(delay_between=3, wait_for_completion=True)
        else:
            print(f"Unknown command: {command}")
            print("\nCommands:")
            print("  insert      - Create database and insert 3 tickets (1 High, 1 Medium, 1 Low)")
            print("  send        - Send tickets one by one (waits for completion)")
            print("  status      - Show sender status")
            print("  results     - View ticket results")
            print("  reset       - Reset all tickets")
            print("  reset-sender - Reset stuck sender state")
    else:
        # Default: Show menu
        print("=" * 60)
        print("TICKET SENDER - n8n Integration")
        print("=" * 60)
        print("\nThis script will send 3 tickets:")
        print("  🔴 1 HIGH urgency ticket (Production Down)")
        print("  🟡 1 MEDIUM urgency ticket (API Rate Limit)")
        print("  🟢 1 LOW urgency ticket (Dark Mode Feature)")
        print("\nCommands:")
        print("  python insert_payloads.py insert     - Setup database and insert tickets")
        print("  python insert_payloads.py send       - Send tickets (waits for completion)")
        print("  python insert_payloads.py status     - Check sender status")
        print("  python insert_payloads.py results    - View results")
        print("  python insert_payloads.py reset      - Reset everything")