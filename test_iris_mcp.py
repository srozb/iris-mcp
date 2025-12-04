import os
from unittest.mock import patch

import pytest

from iris_mcp import (
    _add_note,
    _create_case,
    _create_customer,
    _get_case,
    _list_cases,
    _list_events,
    _list_evidence,
    _list_iocs,
    _list_tasks,
    _update_event,
    list_alert_resolution_statuses,
    list_alert_statuses,
    list_analysis_statuses,
    list_asset_types,
    list_event_categories,
    list_evidence_types,
    list_ioc_types,
    list_os_types,
    list_severities,
    list_task_statuses,
    list_tlp_levels,
    list_types,
)

# ... (Sample payloads remain the same) ...
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


@pytest.fixture
def mock_env():
    with patch.dict(os.environ, {"IRIS_API_KEY": "test", "IRIS_HOST": "http://localhost"}):
        yield


@pytest.fixture
def mock_client_classes():
    with (
        patch("iris_mcp.ClientSession") as MockSession,
        patch("iris_mcp.Case") as MockCase,
        patch("iris_mcp.Customer") as MockCustomer,
        patch("iris_mcp.AdminHelper") as MockAdmin,
    ):
        yield MockSession, MockCase, MockCustomer, MockAdmin


def test_list_cases(mock_env, mock_client_classes):
    _, MockCase, MockCustomer, _ = mock_client_classes
    mock_case = MockCase.return_value
    mock_customer = MockCustomer.return_value

    mock_case.list_cases.return_value.is_error.return_value = False
    mock_case.list_cases.return_value.get_data.return_value = [{"case_id": 1, "case_name": "Test Case", "case_customer": "Cust", "case_status_id": 1}]
    mock_customer.list_customers.return_value.is_error.return_value = False
    mock_customer.list_customers.return_value.get_data.return_value = [{"customer_id": 1, "customer_name": "Cust"}]

    result = _list_cases()
    assert "Test Case" in result
    MockCase.assert_called()


def test_get_case(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.get_case.return_value.is_error.return_value = False
    mock_case.get_case.return_value.get_data.return_value = {
        "case_id": 1,
        "case_name": "Test Case",
        "case_description": "Desc",
        "case_customer": "Cust",
        "case_status_id": 1,
        "case_open_date": "2023-01-01",
    }

    result = _get_case(1)
    assert "Test Case" in result
    assert "Desc" in result


def test_create_case(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.add_case.return_value.is_error.return_value = False
    mock_case.add_case.return_value.get_data.return_value = {"case_id": 2}

    result = _create_case("New Case", 1)
    assert "Case created successfully" in result
    assert "ID: 2" in result


def test_add_note(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.list_notes_directories.return_value.is_error.return_value = False
    mock_case.list_notes_directories.return_value.get_data.return_value = [{"id": 1, "name": "Root"}]
    mock_case.add_note.return_value.is_error.return_value = False
    mock_case.add_note.return_value.get_data.return_value = {"note_id": 5}

    result = _add_note(1, "Note content", "Note title", None, None)
    assert "Note added" in result
    assert "ID: 5" in result


def test_list_events(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.list_events.return_value.is_error.return_value = False
    mock_case.list_events.return_value.get_data.return_value = TIMELINE_PAYLOAD

    result = _list_events(1)
    assert "Phishing delivery" in result
    assert "Initial Access" in result


def test_list_evidence(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.list_evidences.return_value.is_error.return_value = False
    mock_case.list_evidences.return_value.get_data.return_value = EVIDENCES_PAYLOAD

    result = _list_evidence(1)
    assert "encryptor-binary.exe" in result
    assert "789456" in result


def test_list_iocs(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.list_iocs.return_value.is_error.return_value = False
    mock_case.list_iocs.return_value.get_data.return_value = IOCS_PAYLOAD

    result = _list_iocs(1)
    assert "darkvault-support[.]com" in result
    assert "domain" in result


def test_list_tasks(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.list_tasks.return_value.is_error.return_value = False
    # Mocking the dict response structure
    mock_case.list_tasks.return_value.get_data.return_value = {
        "tasks": [{"task_id": 33, "task_title": "Test Task", "task_status_name": "To do", "task_assignees": []}]
    }

    result = _list_tasks(1)
    assert "Test Task" in result
    assert "ID: 33" in result


def test_create_customer(mock_env, mock_client_classes):
    _, _, _, MockAdmin = mock_client_classes
    mock_admin = MockAdmin.return_value

    mock_admin.add_customer.return_value.is_error.return_value = False
    mock_admin.add_customer.return_value.get_data.return_value = {"customer_id": 15}

    result = _create_customer("Test Customer")
    assert "Customer created successfully" in result
    assert "ID: 15" in result


def test_update_event(mock_env, mock_client_classes):
    _, MockCase, _, _ = mock_client_classes
    mock_case = MockCase.return_value

    mock_case.update_event.return_value.is_error.return_value = False

    # Test with case_id in args
    result = _update_event(119, case_id=16, display_in_summary=True)
    assert "Event 119 updated" in result
    mock_case.update_event.assert_called_with(event_id=119, cid=16, display_in_summary=True)


def test_catalogs():
    assert isinstance(list_ioc_types(), list)
    assert isinstance(list_asset_types(), list)
    assert isinstance(list_analysis_statuses(), list)
    assert isinstance(list_alert_resolution_statuses(), list)
    assert isinstance(list_alert_statuses(), list)
    assert isinstance(list_task_statuses(), list)
    assert isinstance(list_severities(), list)
    assert isinstance(list_evidence_types(), list)
    assert isinstance(list_event_categories(), list)
    assert isinstance(list_os_types(), list)
    assert isinstance(list_tlp_levels(), list)

    assert any(entry.get("type") == "md5" for entry in list_types("iocs"))
