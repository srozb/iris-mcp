---
name: iris-mcp
description: Bridge between your AI agent and the DFIR Iris platform. Automate incident response workflows, including case management, evidence tracking, IOC handling, and timeline construction directly from your chat interface.
---

# DFIR Iris MCP Skill

## Overview
The `iris-mcp` server provides a bridge between your AI agent and the [DFIR Iris](https://dfir-iris.org/) platform. This skill enables you to automate incident response workflows, including case management, evidence tracking, IOC handling, and timeline construction directly from your chat interface.

## Configuration
Ensure the following environment variables are set before using the tools:
- `IRIS_API_KEY`: Your API key for authentication.
- `IRIS_HOST`: The URL of your DFIR Iris instance (e.g., `https://iris.example.com`).
- `IRIS_VERIFY_SSL`: Set to `false` if using self-signed certificates (default: `true`).

## Available Tools & Workflows

### 1. Discovery & Reference
Before performing actions, you can query the system for supported types and definitions. This ensures you use valid values for creating objects.

*   **List supported IOC types**: `list_ioc_types()` (e.g., `domain`, `ip-src`, `md5`)
*   **List asset types**: `list_asset_types()` (e.g., `Windows - Computer`, `Firewall`)
*   **List analysis statuses**: `list_analysis_statuses()` (e.g., `New`, `In progress`, `Done`)
*   **List severities**: `list_severities()`
*   **List TLP levels**: `list_tlp_levels()`

### 2. Case Management
Manage the lifecycle of an incident case.

*   **List Cases**: Use `list_cases()` to find existing cases. You can filter by customer, name, status, or date.
    *   *Example*: `list_cases(case_name="Phishing", case_status_id=1)`
*   **Get Case Details**: Use `get_case(case_id=...)` to retrieve full details of a specific case.
*   **Create Case**: Use `create_case()` to start a new investigation.
    *   *Required*: `name`, `customer_id`.
    *   *Optional*: `description`, `soc_id`, `classification_id`.

### 3. IOC Management (Indicators of Compromise)
Add and track indicators related to the case.

*   **Add IOC**: Use `add_ioc()` to register an indicator.
    *   *Example*: `add_ioc(case_id=123, value="malicious.com", ioc_type="domain", ioc_tlp="amber")`
    *   *Note*: Ensure `ioc_type` is valid by checking `list_ioc_types()`.
*   **List IOCs**: Use `list_iocs(case_id=...)` to see all indicators associated with a case.

### 4. Asset Management
Track affected systems and devices.

*   **Add Asset**: Use `add_asset()` to register a compromised or involved system.
    *   *Example*: `add_asset(case_id=123, name="WORKSTATION-01", asset_type="Windows - Computer", analysis_status="Compromised")`
*   **List Assets**: Use `list_assets(case_id=...)`.

### 5. Evidence Handling
Manage forensic artifacts and files.

*   **Add Evidence**: Use `add_evidence()` to log a file or artifact.
    *   *Required*: `case_id`, `filename`, `file_size`.
    *   *Example*: `add_evidence(case_id=123, filename="memory_dump.mem", file_size=1073741824, description="RAM capture from infected host")`
*   **List Evidence**: Use `list_evidence(case_id=...)`.

### 6. Timeline & Events
Build a chronological view of the incident.

*   **Add Event**: Use `add_event()` to add an entry to the timeline.
    *   *Required*: `case_id`, `name`, `date_time` (ISO format).
    *   *Example*: `add_event(case_id=123, name="Malware Execution", date_time="2023-10-27T14:30:00Z", category="Execution")`
*   **List Events**: Use `list_events(case_id=...)`.

### 7. Notes & Documentation
Keep a record of analyst findings and thoughts.

*   **Add Note**: Use `add_note()` to save text content.
    *   *Example*: `add_note(case_id=123, title="Initial Assessment", content="The host appears to be infected with...")`
*   **List Notes**: Use `list_notes(case_id=...)` to view all notes.
*   **Organize**: Use `create_note_directory()` to structure notes if needed.

### 8. Tasks
Manage the to-do list for the investigation.

*   **Add Task**: Use `add_task()` to assign work.
    *   *Example*: `add_task(case_id=123, title="Analyze Memory Dump", status="To do", assignees=[1])`
*   **List Tasks**: Use `list_tasks(case_id=...)`.

### 9. Alert Management
Handle incoming alerts that might escalate to cases.

*   **Create Alert**: Use `create_alert()` to register a new security alert.
    *   *Example*: `create_alert(title="Suspicious Login", description="Multiple failed attempts", source="SIEM", source_ref="ALERT-999")`

## Best Practices
1.  **Verify IDs**: Always list entities (cases, customers, assets) to get the correct IDs before performing updates or additions.
2.  **Use Valid Types**: Refer to the catalog tools (`list_ioc_types`, etc.) to ensure data consistency.
3.  **Check Prerequisites**: Ensure you have a valid `case_id` before trying to add elements to a case.
