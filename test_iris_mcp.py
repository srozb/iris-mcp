import os
import sys
import types
from unittest.mock import MagicMock, patch

#! Mock dfir_iris_client before importing iris_mcp so tests run without the dependency installed
sys.modules["dfir_iris_client"] = MagicMock()
sys.modules["dfir_iris_client.session"] = MagicMock()
sys.modules["dfir_iris_client.case"] = MagicMock()
sys.modules["dfir_iris_client.alert"] = MagicMock()
sys.modules["dfir_iris_client.customer"] = MagicMock()


class DummyFastMCP:
    def __init__(self, *_args, **_kwargs):
        self.registered = []

    def tool(self):
        def decorator(fn):
            self.registered.append(fn.__name__)
            return fn
        return decorator

    def run(self, **_kwargs):
        return None


sys.modules["fastmcp"] = types.SimpleNamespace(FastMCP=DummyFastMCP)

# Now import the module to test
# We need to make sure the script can be imported, so we might need to adjust sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iris_mcp import (
    _list_cases,
    _get_case,
    _create_case,
    _add_note,
    _list_events,
    _list_evidence,
    _list_iocs,
    _list_note_directories,
    _list_notes,
    _list_customers,
    _get_customer_by_id,
    _lookup_customer,
    add_event,
    update_event,
    add_evidence,
    update_evidence,
    add_ioc,
    list_tasks,
    add_task,
    update_task,
    delete_task,
    add_task_comment,
    list_task_comments,
    update_task_comment,
    delete_task_comment,
    list_asset_types,
    list_ioc_types,
    list_analysis_statuses,
    list_alert_resolution_statuses,
    list_alert_statuses,
    list_task_statuses,
    list_severities,
    list_evidence_types,
    list_event_categories,
    list_os_types,
    list_tlp_levels,
    list_types,
)

# Sample live-like payloads captured from the test instance (case 16) to catch schema drift.
TIMELINE_PAYLOAD = {
    "timeline": [
        {
            "event_id": 97,
            "event_title": "Phishing delivery to LAP-CFO01",
            "event_content": "08:14 CET: invoice_Q4_2025.iso received...",
            "event_date": "2025-12-02T08:14:00.000000",
            "event_tz": "+00:00",
            "category_name": "Initial Access",
        },
        {
            "event_id": 98,
            "event_title": "Beaconing to darkvault-support[.]com",
            "event_content": "Beaconing...",
            "event_date": "2025-12-02T08:20:00.000000",
            "event_tz": "+00:00",
            "category_name": "Command and Control",
        },
    ],
    "state": {"object_state": 8, "object_last_update": "2025-12-03T20:09:15.784333"},
}

EVIDENCES_PAYLOAD = {
    "evidences": [
        {
            "id": 22,
            "filename": "encryptor-binary.exe",
            "file_size": 789456,
            "file_description": "Captured BlackDawn encryptor ...",
            "date_added": "2025-12-03T20:10:16.612557",
        },
        {
            "id": 18,
            "filename": "fs-fin01-evtx.zip",
            "file_size": 20480,
            "file_description": "Security/Application logs...",
            "date_added": "2025-12-03T20:09:36.409582",
        },
    ],
    "state": {"object_state": 5, "object_last_update": "2025-12-03T20:10:16.615247"},
}

IOCS_PAYLOAD = {
    "ioc": [
        {
            "ioc_id": 59,
            "ioc_value": "darkvault-support[.]com",
            "ioc_type": "domain",
            "ioc_description": "C2 domain contacted...",
            "tlp_name": "amber",
            "ioc_tags": None,
        },
        {
            "ioc_id": 60,
            "ioc_value": "https://darkvault-support.com/api/v1/register",
            "ioc_type": "url",
            "ioc_description": "Beacon endpoint",
            "tlp_name": "amber",
            "ioc_tags": None,
        },
    ],
    "state": {"object_state": 7, "object_last_update": "2025-12-03T16:45:15.348093"},
}

NOTE_DIRS_PAYLOAD = [
    {
        "id": 32,
        "name": "Root Notes",
        "note_count": 3,
        "notes": [
            {"id": 71, "title": "Evidence collected"},
            {"id": 69, "title": "Incident summary"},
            {"id": 70, "title": "Timeline"},
        ],
    }
]

def test_tools():
    print("Testing tools...")
    
    # Mock environment variables
    with patch.dict(os.environ, {"IRIS_API_KEY": "test", "IRIS_HOST": "http://localhost"}):
        # Mock the classes imported in iris_mcp
        with patch("iris_mcp.ClientSession") as MockSession, \
             patch("iris_mcp.Case") as MockCase, \
             patch("iris_mcp.Alert") as MockAlert, \
             patch("iris_mcp.Customer") as MockCustomer:
            
            # Setup mock instances
            mock_session = MockSession.return_value
            mock_case = MockCase.return_value
            mock_alert = MockAlert.return_value
            mock_customer = MockCustomer.return_value
            
            # Test list_cases
            mock_case.list_cases.return_value.is_error.return_value = False
            mock_case.list_cases.return_value.get_data.return_value = [
                {"case_id": 1, "case_name": "Test Case", "case_customer": "Cust", "case_status_id": 1}
            ]
            mock_customer.list_customers.return_value.is_error.return_value = False
            mock_customer.list_customers.return_value.get_data.return_value = [
                {"customer_id": 1, "customer_name": "Cust"}
            ]
            print(f"list_cases output: {_list_cases()}")
            MockCase.assert_called_with(mock_session)
            MockCase.reset_mock()
            
            # Test get_case
            mock_case.get_case.return_value.is_error.return_value = False
            mock_case.get_case.return_value.get_data.return_value = {
                "case_id": 1,
                "case_name": "Test Case",
                "case_description": "Desc",
                "case_customer": "Cust",
                "case_status_id": 1,
                "case_open_date": "2023-01-01",
            }
            print(f"get_case output: {_get_case(1)}")
            MockCase.assert_called_with(mock_session)
            MockCase.reset_mock()
            
            # Test create_case
            mock_case.add_case.return_value.is_error.return_value = False
            mock_case.add_case.return_value.get_data.return_value = {"case_id": 2}
            print(f"create_case output: {_create_case('New Case', 1)}")
            MockCase.assert_called_with(mock_session)
            MockCase.reset_mock()
            
            # Test add_note
            mock_case.list_notes_directories.return_value.is_error.return_value = False
            mock_case.list_notes_directories.return_value.get_data.return_value = [
                {"id": 1, "name": "Root"}
            ]
            mock_case.add_note.return_value.is_error.return_value = False
            mock_case.add_note.return_value.get_data.return_value = {"note_id": 5}
            print(f"add_note output: {_add_note(1, 'Note content', 'Note title', None, None)}")
            MockCase.assert_called_with(mock_session)

            # Ensure note directory resolution picks first directory id
            mock_case.list_notes_directories.return_value.is_error.return_value = False
            mock_case.list_notes_directories.return_value.get_data.return_value = [
                {"id": 12, "name": "Root"}
            ]
            mock_case.add_note.return_value.get_data.return_value = {"note_id": 77}
            note_out = _add_note(1, "Content", "Title")
            assert "ID: 77" in note_out
            mock_case.add_note.assert_called_with(
                note_title="Title",
                note_content="Content",
                directory_id=12,
                cid=1,
            )

            # Test event listing parses nested timeline
            mock_case.list_events.return_value.is_error.return_value = False
            mock_case.list_events.return_value.get_data.return_value = TIMELINE_PAYLOAD
            ev_out = _list_events(1)
            assert "Phishing delivery" in ev_out and "Initial Access" in ev_out
            assert "Beaconing to darkvault-support" in ev_out and "Command and Control" in ev_out

            # Test evidence listing parses evidences key
            mock_case.list_evidences.return_value.is_error.return_value = False
            mock_case.list_evidences.return_value.get_data.return_value = EVIDENCES_PAYLOAD
            evd_out = _list_evidence(1)
            assert "encryptor-binary.exe" in evd_out and "789456" in evd_out
            assert "fs-fin01-evtx.zip" in evd_out and "20480" in evd_out

            # Test IOC listing parses ioc key
            mock_case.list_iocs.return_value.is_error.return_value = False
            mock_case.list_iocs.return_value.get_data.return_value = IOCS_PAYLOAD
            ioc_out = _list_iocs(1)
            assert "darkvault-support[.]com" in ioc_out and "domain" in ioc_out
            assert "https://darkvault-support.com/api/v1/register" in ioc_out and "url" in ioc_out

            # Test note directory listing and note listing
            mock_case.list_notes_directories.return_value.get_data.return_value = NOTE_DIRS_PAYLOAD
            dir_out = _list_note_directories(1)
            notes_out = _list_notes(1)
            assert "Root Notes" in dir_out and "Note ID: 71" in dir_out
            assert "Directory 32" in notes_out and "Incident summary" in notes_out

            # Test update_event wiring includes cid
            mock_case.update_event.return_value.is_error.return_value = False
            mock_case.update_event.return_value.get_data.return_value = {}
            out = update_event(event_id=97, case_id=1, fields={"display_in_summary": True})
            assert "updated" in out
            mock_case.update_event.assert_called_with(event_id=97, cid=1, display_in_summary=True)

            # Test add_event parses ISO datetime and calls client
            mock_case.add_event.return_value.is_error.return_value = False
            mock_case.add_event.return_value.get_data.return_value = {"event_id": 200}
            add_event_out = add_event(case_id=1, name="Test Event", date_time="2024-01-01T00:00:00+00:00")
            assert "Event added" in add_event_out
            kwargs = mock_case.add_event.call_args.kwargs
            assert isinstance(kwargs["date_time"], object)  # datetime instance
            assert kwargs["cid"] == 1

            # Test evidence update wiring includes cid
            mock_case.update_evidence.return_value.is_error.return_value = False
            mock_case.update_evidence.return_value.get_data.return_value = {}
            ev_update_out = update_evidence(evidence_id=18, case_id=1, fields={"file_hash": "abc"})
            assert "updated" in ev_update_out
            mock_case.update_evidence.assert_called_with(evidence_id=18, cid=1, file_hash="abc")

            # Test add_evidence parameter pass-through
            mock_case.add_evidence.return_value.is_error.return_value = False
            mock_case.add_evidence.return_value.get_data.return_value = {"evidence_id": 99}
            ev_add_out = add_evidence(case_id=1, filename="file.txt", file_size=10, description="desc", file_hash="hash")
            assert "Evidence added" in ev_add_out
            mock_case.add_evidence.assert_called_with(
                filename="file.txt",
                file_size=10,
                description="desc",
                file_hash="hash",
                custom_attributes=None,
                cid=1,
            )

            # Test add_ioc pass-through of tlp/tags/custom_attributes
            mock_case.add_ioc.return_value.is_error.return_value = False
            mock_case.add_ioc.return_value.get_data.return_value = {"ioc_id": 123}
            ioc_add_out = add_ioc(case_id=1, value="example.com", ioc_type="domain", ioc_tlp="amber", ioc_tags="tag1,tag2")
            assert "IOC added" in ioc_add_out
            mock_case.add_ioc.assert_called_with(
                value="example.com",
                ioc_type="domain",
                description="",
                ioc_tlp="amber",
                ioc_tags=["tag1", "tag2"],
                custom_attributes=None,
                cid=1,
            )

            # Task operations
            mock_case.list_tasks.return_value.is_error.return_value = False
            mock_case.list_tasks.return_value.get_data.return_value = [
                {"task_id": 1, "task_title": "Do thing", "task_status": "To do", "assignees": ["analyst"]}
            ]
            tlist = list_tasks(case_id=1)
            assert "Do thing" in tlist

            mock_case.add_task.return_value.is_error.return_value = False
            mock_case.add_task.return_value.get_data.return_value = {"task_id": 10}
            add_task_out = add_task(case_id=1, title="T1", status="To do", assignees=["me"])
            assert "Task added" in add_task_out
            mock_case.add_task.assert_called_with(
                title="T1",
                status="To do",
                assignees=["me"],
                description=None,
                tags=None,
                custom_attributes=None,
                cid=1,
            )

            mock_case.update_task.return_value.is_error.return_value = False
            mock_case.update_task.return_value.get_data.return_value = {}
            upd_task_out = update_task(case_id=1, task_id=10, fields={"status": "Done"})
            assert "updated" in upd_task_out
            mock_case.update_task.assert_called_with(task_id=10, cid=1, status="Done")

            mock_case.delete_task.return_value.is_error.return_value = False
            mock_case.delete_task.return_value.get_data.return_value = {}
            del_task_out = delete_task(case_id=1, task_id=10)
            assert "deleted" in del_task_out
            mock_case.delete_task.assert_called_with(task_id=10, cid=1)

            mock_case.list_task_comments.return_value.is_error.return_value = False
            mock_case.list_task_comments.return_value.get_data.return_value = [
                {"comment_id": 5, "comment_content": "ok"}
            ]
            tcomments = list_task_comments(case_id=1, task_id=10)
            assert "ok" in tcomments

            mock_case.add_task_comment.return_value.is_error.return_value = False
            mock_case.add_task_comment.return_value.get_data.return_value = {}
            add_comment_out = add_task_comment(case_id=1, task_id=10, comment="hey")
            assert "Comment added" in add_comment_out
            mock_case.add_task_comment.assert_called_with(task_id=10, comment="hey", cid=1)

            mock_case.update_task_comment.return_value.is_error.return_value = False
            mock_case.update_task_comment.return_value.get_data.return_value = {}
            upd_comment_out = update_task_comment(case_id=1, task_id=10, comment_id=5, comment="upd")
            assert "updated" in upd_comment_out
            mock_case.update_task_comment.assert_called_with(task_id=10, comment_id=5, comment="upd", cid=1)

            mock_case.delete_task_comment.return_value.is_error.return_value = False
            mock_case.delete_task_comment.return_value.get_data.return_value = {}
            del_comment_out = delete_task_comment(case_id=1, task_id=10, comment_id=5)
            assert "deleted" in del_comment_out
            mock_case.delete_task_comment.assert_called_with(task_id=10, comment_id=5, cid=1)

            # Test list_customers
            mock_customer.list_customers.return_value.is_error.return_value = False
            mock_customer.list_customers.return_value.get_data.return_value = [
                {"customer_id": 1, "customer_name": "Cust A", "customer_sector": "Tech"}
            ]
            print(f"list_customers output: {_list_customers()}")
            MockCustomer.assert_called_with(mock_session)
            MockCustomer.reset_mock()

            # Test get_customer_by_id
            mock_customer.get_customer_by_id.return_value.is_error.return_value = False
            mock_customer.get_customer_by_id.return_value.get_data.return_value = {
                "customer_id": 2,
                "customer_name": "Cust B",
                "customer_sector": "Finance",
                "customer_description": "VIP",
            }
            print(f"get_customer_by_id output: {_get_customer_by_id(2)}")
            MockCustomer.assert_called_with(mock_session)
            MockCustomer.reset_mock()

            # Test lookup_customer
            mock_customer.lookup_customer.return_value.is_error.return_value = False
            mock_customer.lookup_customer.return_value.get_data.return_value = {
                "customer_id": 3,
                "customer_name": "Cust C",
            }
            print(f"lookup_customer output: {_lookup_customer('Cust C')}")
            MockCustomer.assert_called_with(mock_session)

    # Static catalogs should always be populated
    ioc_types = list_ioc_types()
    assert isinstance(ioc_types, list)
    assert any(item.get("type") == "md5" for item in ioc_types)

    asset_types = list_asset_types()
    assert isinstance(asset_types, list)
    assert any(asset.get("asset_name") == "Account" for asset in asset_types)

    statuses = list_analysis_statuses()
    assert isinstance(statuses, list)
    assert any(status.get("name") == "Done" for status in statuses)

    assert any(status.get("name") == "False Positive" for status in list_alert_resolution_statuses())
    assert any(status.get("name") == "New" for status in list_alert_statuses())
    assert any(status.get("name") == "To do" for status in list_task_statuses())
    assert any(level.get("name") == "Critical" for level in list_severities())
    assert any(ev.get("name") == "Unspecified" for ev in list_evidence_types())
    assert any(cat.get("name") == "Impact" for cat in list_event_categories())
    assert any(os.get("name") == "Linux" for os in list_os_types())
    assert any(tlp.get("name") == "amber" for tlp in list_tlp_levels())

    # Generic catalog lookup
    assert any(entry.get("asset_name") == "Firewall" for entry in list_types("assets"))
    assert any(entry.get("type") == "md5" for entry in list_types("iocs"))
    assert any(entry.get("name") == "Windows" for entry in list_types("os"))
    print("catalog outputs validated")

if __name__ == "__main__":
    test_tools()
