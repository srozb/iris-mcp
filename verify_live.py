import os
import sys
import time

from dfir_iris_client.alert import Alert
from dfir_iris_client.case import Case
from dfir_iris_client.session import ClientSession
from dotenv import load_dotenv

import iris_mcp

# Load environment variables
load_dotenv()

API_KEY = os.getenv("IRIS_API_KEY")
HOST = os.getenv("IRIS_HOST")
CASE_ID = 16

if not API_KEY or not HOST:
    print("Error: IRIS_API_KEY and IRIS_HOST must be set in .env")
    sys.exit(1)

print(f"DEBUG: API_KEY starts with: {API_KEY[:4] if API_KEY else 'None'}")


def verify_live():
    # Ensure iris_mcp uses the correct host with scheme
    # iris_mcp.get_iris_client handles scheme addition, so we just need to ensure env var is set.
    # But verify_live.py loaded .env, so os.environ is populated.

    print(f"Connecting to {HOST} with Case ID {CASE_ID}...")
    # We still use direct session for verification
    host_url = HOST
    if not host_url.startswith("http"):
        host_url = f"https://{host_url}"
    session = ClientSession(host=host_url, apikey=API_KEY, ssl_verify=False)
    case_handler = Case(session)

    # 1. Verify Connection & Case Access
    print(f"[-] Checking access to Case {CASE_ID}...")
    resp = case_handler.get_case(CASE_ID)
    if resp.is_error():
        print(f"[!] Failed to get case: {resp}")
        return
    print(f"[+] Successfully accessed Case {CASE_ID}: {resp.get_data().get('case_name')}")

    # 2. Add Note via MCP
    print("[-] Adding a test note via MCP...")
    note_title = "MCP Verification Note"
    note_content = "This note was created by the MCP verification script."

    # MCP _add_note handles directory resolution
    result = iris_mcp._add_note(CASE_ID, note_content, note_title)
    print(f"[+] MCP Result: {result}")

    if "Note added" in result:
        # Verify note exists
        # Extract ID from result string "Note added. ID: <id>"
        try:
            # Result format: "Note added to case 16. ID: 76, Directory: 32"
            note_id_part = result.split("ID: ")[1]
            if "," in note_id_part:
                note_id = int(note_id_part.split(",")[0])
            else:
                note_id = int(note_id_part)

            resp = case_handler.get_note(note_id, cid=CASE_ID)
            if not resp.is_error() and resp.get_data().get("note_title") == note_title:
                print("[+] Note verification successful.")

                # Delete note
                print("[-] Deleting note...")
                resp = case_handler.delete_note(note_id, cid=CASE_ID)
                if not resp.is_error():
                    print("[+] Note deleted.")
                else:
                    print(f"[!] Failed to delete note: {resp}")
            else:
                print(f"[!] Note verification failed: {resp}")
        except Exception as e:
            print(f"[!] Failed to parse note ID or verify: {e}")

    # 3. Add Event via MCP
    print("[-] Adding a test event via MCP...")
    event_title = "MCP Verification Event"
    event_date = "2025-12-04T12:00:00+00:00"
    result = iris_mcp._add_event(CASE_ID, event_title, date_time=event_date, description="Verification event content")
    print(f"[+] MCP Result: {result}")

    if "Event added" in result:
        try:
            event_id = int(result.split("ID: ")[1])
            # Delete event
            print("[-] Deleting event...")
            resp = case_handler.delete_event(event_id, cid=CASE_ID)
            if not resp.is_error():
                print("[+] Event deleted.")
            else:
                print(f"[!] Failed to delete event: {resp}")
        except Exception as e:
            print(f"[!] Failed to parse event ID or verify: {e}")

    # 4. Add IOC via MCP
    print("[-] Adding a test IOC via MCP...")
    ioc_value = "example.com"
    ioc_type = "domain"
    result = iris_mcp._add_ioc(CASE_ID, ioc_value, ioc_type, description="Verification IOC")
    print(f"[+] MCP Result: {result}")

    if "IOC added" in result:
        try:
            ioc_id = int(result.split("ID: ")[1])
            # Delete IOC
            print("[-] Deleting IOC...")
            resp = case_handler.delete_ioc(ioc_id, cid=CASE_ID)
            if not resp.is_error():
                print("[+] IOC deleted.")
            else:
                print(f"[!] Failed to delete IOC: {resp}")
        except Exception as e:
            print(f"[!] Failed to parse IOC ID or verify: {e}")

    # 5. Create Alert via MCP
    print("[-] Creating a test Alert via MCP...")
    alert_title = "MCP Verification Alert"
    result = iris_mcp._create_alert(alert_title, "Description", "Source", "Ref", "tag1,tag2")
    print(f"[+] MCP Result: {result}")

    if "Alert created" in result:
        try:
            alert_id = int(result.split("ID: ")[1])
            # Delete alert (using Alert handler)
            alert_handler = Alert(session)
            print("[-] Deleting alert...")
            resp = alert_handler.delete_alert(alert_id)
            if not resp.is_error():
                print("[+] Alert deleted.")
            else:
                print(f"[!] Failed to delete alert: {resp}")
        except Exception as e:
            print(f"[!] Failed to parse alert ID or verify: {e}")

    # 6. Task Management
    print("[-] Testing Task Management...")
    task_title = "MCP Verification Task"
    result = iris_mcp._add_task(CASE_ID, task_title, "To do", [])
    print(f"[+] MCP Result: {result}")

    if "Task added" in result:
        try:
            task_id = int(result.split("ID: ")[1])

            # Debug list_tasks
            print("[-] Debugging list_tasks raw response...")
            raw_tasks = case_handler.list_tasks(cid=CASE_ID)
            print(f"[DEBUG] Raw tasks data: {raw_tasks.get_data()}")

            # List tasks via MCP
            tasks_list = iris_mcp._list_tasks(CASE_ID)
            print(f"[+] MCP list_tasks output:\n{tasks_list}")

            # Update task
            print("[-] Updating task...")
            result = iris_mcp._update_task(CASE_ID, task_id, status="In progress")
            print(f"[+] MCP Result: {result}")

            # Delete task
            print("[-] Deleting task...")
            result = iris_mcp._delete_task(CASE_ID, task_id)
            print(f"[+] MCP Result: {result}")

        except Exception as e:
            print(f"[!] Failed to parse task ID or verify: {e}")

    # 7. Customer Management
    print("[-] Testing Customer Management...")
    customer_name = f"MCP_Test_Customer_{int(time.time())}"
    result = iris_mcp._create_customer(customer_name, "Test description", "Gold")
    print(f"[+] MCP Result: {result}")

    if "Customer created" in result:
        try:
            customer_id = int(result.split("ID: ")[1])
            print(f"[+] Customer created with ID: {customer_id}")
            # Note: No delete_customer exposed yet, so we leave it (or use AdminHelper to delete if we wanted)
        except Exception as e:
            print(f"[!] Failed to parse customer ID: {e}")

    # 8. Event Update with CID
    print("[-] Testing Event Update with CID...")
    event_title = "Event for Update Test"
    result = iris_mcp._add_event(CASE_ID, event_title, date_time="2025-12-04T12:00:00+00:00")
    if "Event added" in result:
        event_id = int(result.split("ID: ")[1])
        print(f"[-] Updating event {event_id} with display_in_summary=True...")
        # Explicitly passing case_id to update_event
        result = iris_mcp._update_event(event_id, case_id=CASE_ID, display_in_summary=True)
        print(f"[+] MCP Result: {result}")

        # Verify update
        resp = case_handler.get_event(event_id, cid=CASE_ID)
        if not resp.is_error():
            in_summary = resp.get_data().get("event_in_summary")
            print(f"[+] Event in_summary status: {in_summary}")
            if in_summary:
                print("[+] Event update successful.")
            else:
                print("[!] Event update failed (in_summary is False).")

        # Cleanup
        iris_mcp._delete_event(event_id, CASE_ID)


if __name__ == "__main__":
    verify_live()
