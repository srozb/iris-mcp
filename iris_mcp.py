#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "dfir-iris-client>=2.0.0",
#   "fastmcp>=2.13.2"
# ]
# ///

import inspect
import os
import sys

# Add vendor directory to path to ensure we use the local client version
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor/iris-client"))

from datetime import datetime
from typing import Any

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.alert import Alert
from dfir_iris_client.case import Case
from dfir_iris_client.customer import Customer
from dfir_iris_client.session import ClientSession
from fastmcp import FastMCP

# Static catalog data loaded from a dedicated module
from types_catalog import (
    ALERT_RESOLUTION_STATUSES,
    ALERT_STATUSES,
    ANALYSIS_STATUSES,
    ASSET_TYPES,
    CATALOG,
    EVENT_CATEGORIES,
    EVIDENCE_TYPES,
    IOC_TYPES,
    OS_TYPES,
    SEVERITIES,
    TASK_STATUSES,
    TLP_LEVELS,
)

# Initialize FastMCP server
mcp = FastMCP("dfir-iris")


def _normalize_key(name: str) -> str:
    return name.replace("_", "").replace("-", "").lower()


def _get_field(item: Any, *names: str) -> Any:
    """Return the first matching attribute/key from an API payload object or dict.

    Tries direct matches first, then falls back to case/underscore-insensitive matches
    against dict keys or object attributes to avoid None placeholders when API
    payloads vary slightly.
    """
    candidates = list(names)
    normalized_targets = {_normalize_key(n): n for n in candidates}

    # Direct lookup
    for name in candidates:
        if isinstance(item, dict) and name in item:
            return item[name]
        if hasattr(item, name):
            return getattr(item, name)

    # Fuzzy lookup on dict keys
    if isinstance(item, dict):
        for key, value in item.items():
            if _normalize_key(key) in normalized_targets:
                return value

    # Fuzzy lookup on object attributes
    for attr in dir(item):
        if attr.startswith("__"):
            continue
        if _normalize_key(attr) in normalized_targets:
            try:
                return getattr(item, attr)
            except Exception:
                continue
    return None


def _extract_data(resp: Any, action: str) -> Any:
    """Unwrap ApiResponse data or raise a helpful error."""
    if hasattr(resp, "is_error") and resp.is_error():
        msg = resp.get_msg() if hasattr(resp, "get_msg") else None
        details = None
        if hasattr(resp, "as_json"):
            try:
                details = resp.as_json()
            except Exception:
                details = None
        debug = f" | response={details}" if details else ""
        raise ValueError(f"{action} failed: {msg or resp}{debug}")
    if hasattr(resp, "get_data"):
        return resp.get_data()
    return getattr(resp, "data", None)


def _try_case_methods(
    case_obj: Any,
    method_candidates: list[str],
    action: str,
    payload_options: list[dict[str, Any]],
    allow_positional: bool = True,
) -> tuple[Any, str]:
    """Attempt multiple method names/payload shapes; return (data, method_used) or raise last error."""
    last_error: Exception | None = None
    for meth in method_candidates:
        if not hasattr(case_obj, meth):
            continue
        func = getattr(case_obj, meth)
        for payload in payload_options:
            try:
                resp = func(**payload)
            except TypeError:
                if not allow_positional:
                    last_error = None
                    continue
                try:
                    args = []
                    for key in ("cid", "case_id"):
                        if key in payload:
                            args.append(payload[key])
                            break
                    remaining = [v for k, v in payload.items() if k not in ("cid", "case_id")]
                    resp = func(*args, *remaining)
                except Exception as e:
                    last_error = e
                    continue
            try:
                data = _extract_data(resp, action)
                return data, meth
            except Exception as e:
                last_error = e
                continue
    if last_error:
        raise last_error
    raise AttributeError(f"No method found for {action}. Tried: {method_candidates}")


def _ensure_list(data: Any) -> list[Any]:
    """Normalize Iris API data payloads to a list for safe iteration."""
    if data is None:
        return []
    if isinstance(data, list | tuple):
        return list(data)
    if isinstance(data, dict):
        # Prefer common collection keys returned by the Iris API
        for key in (
            "timeline",
            "events",
            "evidences",
            "assets",
            "ioc",
            "iocs",
            "notes",
            "note",
        ):
            if key in data and isinstance(data[key], list | tuple):
                return list(data[key])
        # Prefer nested "data" key if present; otherwise, iterate values
        nested = data.get("data") if hasattr(data, "get") else None
        if isinstance(nested, list | tuple):
            return list(nested)
        return list(data.values())
    # Single object case
    return [data]


def _prepare_case(session: ClientSession, case_id: int | None) -> Case:
    case_obj = Case(session)
    try:
        if case_id is not None and hasattr(case_obj, "set_cid"):
            case_obj.set_cid(case_id)
    except Exception:
        pass
    return case_obj


def _introspect_case_methods(case_id: int, filter_text: str = "") -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        names = [n for n in dir(case_obj) if not n.startswith("__")]
        if filter_text:
            lt = filter_text.lower()
            names = [n for n in names if lt in n.lower()]
        parts = []
        for name in sorted(names):
            attr = getattr(case_obj, name)
            if callable(attr):
                try:
                    sig = str(inspect.signature(attr))
                except Exception:
                    sig = "()"
                parts.append(f"{name}{sig}")
            else:
                parts.append(name)
        if not parts:
            return f"No case methods matched filter '{filter_text}'."
        return "Case methods:\n" + "\n".join(parts)
    except Exception as e:
        return f"Error introspecting case methods: {e!s}"


def _format_customer(customer: Any, customer_map: dict[int, str] | None = None) -> str:
    """Render customer info from id/dict/str with optional lookup map."""
    if customer is None:
        return "Unassigned"
    if isinstance(customer, str | bytes):
        return str(customer)
    if isinstance(customer, dict):
        name = _get_field(customer, "customer_name", "name")
        cid = _get_field(customer, "customer_id", "id")
        if name and cid is not None:
            return f"{name} (ID {cid})"
        if name:
            return str(name)
        if cid is not None:
            return f"ID {cid}"
    if isinstance(customer, int) and customer_map and customer in customer_map:
        return f"{customer_map[customer]} (ID {customer})"
    if isinstance(customer, int):
        return f"ID {customer}"
    return str(customer)


def get_iris_client() -> ClientSession:
    """
    Initialize and return the DFIR Iris session.
    Reads configuration from environment variables.
    """
    api_key = os.environ.get("IRIS_API_KEY")
    host = os.environ.get("IRIS_HOST")
    verify_ssl = os.environ.get("IRIS_VERIFY_SSL", "true").lower() == "true"

    if not api_key:
        raise ValueError("IRIS_API_KEY environment variable is not set")
    if not host:
        raise ValueError("IRIS_HOST environment variable is not set")

    if not host.startswith("http"):
        host = f"https://{host}"

    return ClientSession(apikey=api_key, host=host, ssl_verify=verify_ssl)


def _get_catalog(kind: str) -> list[dict[str, str]]:
    """Return a catalog list by key with some friendly aliases."""
    normalized = (kind or "").strip().lower()
    aliases = {
        "ioc": "iocs",
        "ioc_types": "iocs",
        "asset": "assets",
        "asset_types": "assets",
        "analysis_status": "analysis_statuses",
        "analysis": "analysis_statuses",
        "alert_resolution": "alert_resolution_statuses",
        "alert_resolutions": "alert_resolution_statuses",
        "task_status": "task_statuses",
        "severity": "severities",
        "alert_status": "alert_statuses",
        "evidence": "evidence_types",
        "event_category": "event_categories",
        "events": "event_categories",
        "os": "os_types",
        "os_type": "os_types",
        "tlp": "tlp_levels",
        "tlps": "tlp_levels",
    }
    key = aliases.get(normalized, normalized)
    catalog = CATALOG.get(key)
    if catalog is None:
        available = ", ".join(sorted(CATALOG))
        raise ValueError(f"Unknown catalog '{kind}'. Available: {available}")
    return catalog


@mcp.tool()
def list_types(kind: str) -> list[dict[str, str]]:
    """Return a catalog of supported types/statuses (e.g., assets, iocs, severities)."""
    return _get_catalog(kind)


@mcp.tool()
def list_ioc_types() -> list[dict[str, str]]:
    """Return all supported IOC types (with optional validation hints)."""
    return IOC_TYPES


@mcp.tool()
def list_asset_types() -> list[dict[str, str]]:
    """Return all supported asset types (with icon hints)."""
    return ASSET_TYPES


@mcp.tool()
def list_analysis_statuses() -> list[dict[str, str]]:
    """Return all analysis statuses used for assets/IOCs."""
    return ANALYSIS_STATUSES


@mcp.tool()
def list_alert_resolution_statuses() -> list[dict[str, str]]:
    """Return alert resolution statuses."""
    return ALERT_RESOLUTION_STATUSES


@mcp.tool()
def list_alert_statuses() -> list[dict[str, str]]:
    """Return alert lifecycle statuses."""
    return ALERT_STATUSES


@mcp.tool()
def list_task_statuses() -> list[dict[str, str]]:
    """Return task statuses."""
    return TASK_STATUSES


@mcp.tool()
def list_severities() -> list[dict[str, str]]:
    """Return severity levels."""
    return SEVERITIES


@mcp.tool()
def list_evidence_types() -> list[dict[str, str]]:
    """Return evidence types."""
    return EVIDENCE_TYPES


@mcp.tool()
def list_event_categories() -> list[dict[str, str]]:
    """Return event categories."""
    return EVENT_CATEGORIES


@mcp.tool()
def list_os_types() -> list[dict[str, str]]:
    """Return operating system types."""
    return OS_TYPES


@mcp.tool()
def list_tlp_levels() -> list[dict[str, str]]:
    """Return TLP levels."""
    return TLP_LEVELS


def _list_cases(
    customer_id: int | None = None,
    case_name: str | None = None,
    description: str | None = None,
    case_status_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    try:
        session = get_iris_client()
        # Filter out None values
        kwargs = {
            "case_customer": customer_id,
            "case_name": case_name,
            "case_description": description,
            "case_status_id": case_status_id,
            "case_open_date_gt": start_date,
            "case_open_date_lt": end_date,
        }
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        cases = Case(session).list_cases(**filtered_kwargs)
        data = _extract_data(cases, "Listing cases")
        items = _ensure_list(data)

        customer_lookup: dict[int, str] | None = None
        try:
            customers_resp = Customer(session).list_customers()
            customers_data = _extract_data(customers_resp, "Listing customers")
            if customers_data:
                customer_lookup = {}
                for cust in _ensure_list(customers_data):
                    cid = _get_field(cust, "customer_id", "id")
                    name = _get_field(cust, "customer_name", "name")
                    if cid is not None and name:
                        customer_lookup[int(cid)] = name
        except Exception:
            # If customer lookup fails, still return cases.
            customer_lookup = None

        if not items:
            return "No cases found."

        result = "Cases:\n"
        for case in items:
            cid = _get_field(case, "case_id", "id", "cid")
            name = _get_field(case, "case_name", "name")
            customer = _format_customer(
                _get_field(case, "case_customer", "customer", "customer_id", "case_customer_id"),
                customer_lookup,
            )
            status = _get_field(case, "case_status_id", "status_id", "status")
            result += f"- ID: {cid}, Name: {name}, Customer: {customer}, Status: {status}\n"

        return result
    except Exception as e:
        return f"Error listing cases: {e!s}"


@mcp.tool()
def list_cases(
    customer_id: int | None = None,
    case_name: str | None = None,
    description: str | None = None,
    case_status_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """
    List cases with optional filtering.
    """
    return _list_cases(customer_id, case_name, description, case_status_id, start_date, end_date)


def _get_case(case_id: int) -> str:
    try:
        session = get_iris_client()
        case = Case(session).get_case(cid=case_id)
        data = _extract_data(case, f"Getting case {case_id}")

        if not data:
            return f"Case with ID {case_id} not found."

        return (
            "Case Details:\n"
            f"ID: {_get_field(data, 'case_id', 'id', 'cid')}\n"
            f"Name: {_get_field(data, 'case_name', 'name')}\n"
            f"Description: {_get_field(data, 'case_description', 'description')}\n"
            f"Customer: {_format_customer(_get_field(data, 'case_customer', 'customer', 'customer_id', 'case_customer_id'))}\n"
            f"Status: {_get_field(data, 'case_status_id', 'status_id', 'status')}\n"
            f"Opened: {_get_field(data, 'case_open_date', 'open_date')}"
        )
    except Exception as e:
        return f"Error getting case {case_id}: {e!s}"


@mcp.tool()
def get_case(case_id: int) -> str:
    """
    Get detailed information about a specific case.
    """
    return _get_case(case_id)


def _create_case(name: str, customer_id: int, description: str = "", soc_id: str = "", classification_id: int | None = None) -> str:
    try:
        session = get_iris_client()
        # Note: add_case requires soc_id and case_classification
        kwargs = {
            "case_name": name,
            "case_customer": customer_id,
            "case_description": description,
            "soc_id": soc_id,
        }
        if classification_id is not None:
            kwargs["case_classification_id"] = classification_id
        else:
            # Default classification if not provided and required by API
            kwargs["case_classification"] = "other:other"

        new_case = Case(session).add_case(**kwargs)

        created = _extract_data(new_case, "Creating case")
        if not created:
            return "Failed to create case."
        return f"Case created successfully. ID: {_get_field(created, 'case_id', 'id', 'cid')}"
    except Exception as e:
        return f"Error creating case: {e!s}"


@mcp.tool()
def create_case(
    name: str,
    customer_id: int,
    description: str = "",
    soc_id: str = "",
    classification_id: int | None = None,
) -> str:
    """
    Create a new case.
    """
    return _create_case(name, customer_id, description, soc_id, classification_id)


def _create_alert(
    title: str,
    description: str,
    source: str,
    source_ref: str,
    tags: str = "",
    severity_id: int = 2,  # Low
    status_id: int = 1,  # New
    customer_id: int = 1,  # Default customer
) -> str:
    try:
        session = get_iris_client()
        alert_handler = Alert(session)
        alert_data = {
            "alert_title": title,
            "alert_description": description,
            "alert_source": source,
            "alert_source_ref": source_ref,
            "alert_tags": tags,
            "alert_severity_id": severity_id,
            "alert_status_id": status_id,
            "alert_customer_id": customer_id,
        }
        resp = alert_handler.add_alert(alert_data)
        data = _extract_data(resp, "Creating alert")
        alert_id = _get_field(data, "alert_id", "id")
        return f"Alert created successfully. ID: {alert_id}"
    except Exception as e:
        return f"Error creating alert: {e!s}"


@mcp.tool()
def create_alert(
    title: str,
    description: str,
    source: str,
    source_ref: str,
    tags: str = "",
    severity_id: int = 2,  # Low
    status_id: int = 1,  # New
    customer_id: int = 1,  # Default customer
) -> str:
    """
    Create a new alert.
    """
    return _create_alert(title, description, source, source_ref, tags, severity_id, status_id, customer_id)


def _create_customer(name: str, description: str | None = None, sla: str | None = None) -> str:
    try:
        session = get_iris_client()
        admin_handler = AdminHelper(session)
        resp = admin_handler.add_customer(customer_name=name, customer_description=description, customer_sla=sla)
        data = _extract_data(resp, "Creating customer")
        cid = _get_field(data, "customer_id", "id")
        return f"Customer created successfully. ID: {cid}"
    except Exception as e:
        return f"Error creating customer: {e!s}"


@mcp.tool()
def create_customer(name: str, description: str | None = None, sla: str | None = None) -> str:
    """Create a new customer."""
    return _create_customer(name, description, sla)


def _resolve_note_directory_id(case_obj: Any, case_id: int, directory_id: int | None) -> int | None:
    """Return a usable directory_id, creating a default one if needed."""
    if directory_id is not None:
        return directory_id
    try:
        resp = case_obj.list_notes_directories(cid=case_id)
        data = _extract_data(resp, f"Listing note directories for case {case_id}")
        for item in _ensure_list(data):
            dir_id = _get_field(item, "id", "directory_id", "note_directory_id", "dir_id")
            if dir_id is not None:
                return int(dir_id)
    except Exception:
        pass

    # As a fallback, try to create a root directory
    try:
        resp = case_obj.add_notes_directory(directory_name="Root Notes", cid=case_id)
        data = _extract_data(resp, f"Creating default note directory for case {case_id}")
        val = _get_field(data, "id", "directory_id", "note_directory_id", "dir_id")
        return int(val) if val is not None else None
    except Exception:
        return None


def _add_note(
    case_id: int,
    content: str,
    title: str = "Note",
    directory_id: int | None = None,
    group_id: int | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        # group_id is deprecated in the client; treat it as an alias if provided
        resolved_dir = _resolve_note_directory_id(case_obj, case_id, directory_id or group_id)
        if resolved_dir is None:
            raise ValueError("No valid note directory_id found or created for this case")

        kwargs = {
            "note_title": title,
            "note_content": content,
            "directory_id": resolved_dir,
            "custom_attributes": custom_attributes,
            "cid": case_id,
        }
        note = case_obj.add_note(**{k: v for k, v in kwargs.items() if v is not None})
        data = _extract_data(note, f"Adding note to case {case_id}")
        note_id = _get_field(data, "note_id", "id")
        return f"Note added to case {case_id}. ID: {note_id}, Directory: {resolved_dir}"
    except Exception as e:
        return f"Error adding note: {e!s}"


def _list_notes(case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_notes_directories(cid=case_id)
        data = _extract_data(resp, f"Listing note directories for case {case_id}")
        directories = _ensure_list(data)
        if not directories:
            return f"No notes found for case {case_id}."

        result = f"Notes for Case {case_id}:\n"
        for directory in directories:
            dir_id = _get_field(directory, "id", "directory_id", "note_directory_id", "dir_id")
            dir_name = _get_field(directory, "name", "directory_name", "note_directory_name") or "(unnamed directory)"
            note_count = _get_field(directory, "note_count", "notes_count", "notes_nb")
            notes = directory.get("notes") if isinstance(directory, dict) else None
            result += f"- Directory {dir_id} ({dir_name})"
            if note_count is not None:
                result += f" — {note_count} notes"
            result += "\n"
            if notes:
                for note in notes:
                    nid = _get_field(note, "id", "note_id")
                    title = _get_field(note, "title", "note_title")
                    result += f"  • ID: {nid}, Title: {title}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error listing notes: {e!s}"


def _list_note_directories(case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        data, used = _try_case_methods(
            case_obj,
            ["list_notes_directories", "list_note_directories"],
            f"Listing note directories for case {case_id}",
            [{"cid": case_id}, {"case_id": case_id}],
            allow_positional=False,
        )
        items = _ensure_list(data)
        if not items:
            return f"No note directories found for case {case_id} (method {used})."

        result = f"Note directories for Case {case_id} (method {used}):\n"
        for item in items:
            dir_id = _get_field(item, "id", "directory_id", "note_directory_id", "dir_id")
            name = _get_field(item, "name", "directory_name", "note_directory_name")
            note_count = _get_field(item, "note_count", "notes_count", "notes_nb")
            notes = item.get("notes") if isinstance(item, dict) else None
            result += f"- ID: {dir_id}, Name: {name}"
            if note_count is not None:
                result += f", Notes: {note_count}"
            result += "\n"
            if notes:
                for note in notes:
                    nid = _get_field(note, "id", "note_id")
                    title = _get_field(note, "title", "note_title")
                    result += f"  • Note ID: {nid}, Title: {title}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error listing note directories: {e!s}"


def _create_note_directory(case_id: int, name: str, parent_directory_id: int | None = None) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        try:
            resp = case_obj.add_notes_directory(directory_name=name, parent_directory_id=parent_directory_id, cid=case_id)
            data = _extract_data(resp, f"Creating note directory '{name}' for case {case_id}")
            dir_id = _get_field(data, "id", "directory_id", "note_directory_id", "dir_id")
            return f"Note directory created. ID: {dir_id}"
        except Exception:
            pass

        # Fallback to other potential method names if the above failed
        candidates = ["add_note_directory", "create_note_directory", "add_notedirectory"]
        for meth in candidates:
            if not hasattr(case_obj, meth):
                continue
            kw_options = [
                {"cid": case_id, "directory_name": name, "parent_directory_id": parent_directory_id},
                {"cid": case_id, "name": name, "parent_directory_id": parent_directory_id},
            ]
            try:
                data, used = _try_case_methods(case_obj, [meth], f"Creating note directory '{name}' for case {case_id}", kw_options)
                dir_id = _get_field(data, "directory_id", "id", "note_directory_id", "dir_id")
                return f"Note directory created. ID: {dir_id} (via {used})"
            except Exception:
                continue

        note_methods = [m for m in dir(case_obj) if "note" in m]
        return f"Note directory creation not available on Case client. Available note-related attributes: {note_methods}"
    except Exception as e:
        return f"Error creating note directory: {e!s}"


def _get_note(note_id: int, case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.get_note(note_id=note_id, cid=case_id)
        data = _extract_data(resp, f"Getting note {note_id}")
        title = _get_field(data, "note_title", "title")
        content = _get_field(data, "note_content", "content")
        directory = _get_field(data, "directory_id", "note_directory_id", "dir_id")
        return f"Note {note_id} (Case {case_id}):\nTitle: {title}\nDirectory: {directory}\nContent:\n{content}"
    except Exception as e:
        return f"Error getting note: {e!s}"


def _update_note(note_id: int, case_id: int, **fields: Any) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        payload = {"note_id": note_id, "cid": case_id}
        payload.update({k: v for k, v in fields.items() if v is not None})
        resp = case_obj.update_note(**payload)
        _extract_data(resp, f"Updating note {note_id}")
        return f"Note {note_id} updated."
    except Exception as e:
        return f"Error updating note: {e!s}"


def _delete_note(note_id: int, case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.delete_note(note_id=note_id, cid=case_id)
        _extract_data(resp, f"Deleting note {note_id}")
        return f"Note {note_id} deleted."
    except Exception as e:
        return f"Error deleting note: {e!s}"


def _add_note_comment(note_id: int, comment: str, case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.add_note_comment(note_id=note_id, comment=comment, cid=case_id)
        _extract_data(resp, f"Adding comment to note {note_id}")
        return f"Comment added to note {note_id}."
    except Exception as e:
        return f"Error adding note comment: {e!s}"


def _list_note_comments(note_id: int, case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_note_comments(note_id=note_id, cid=case_id)
        data = _extract_data(resp, f"Listing note comments for note {note_id}")
        items = _ensure_list(data)
        if not items:
            return f"No comments found for note {note_id}."
        result = f"Comments for note {note_id}:\n"
        for c in items:
            cid = _get_field(c, "comment_id", "id")
            author = _get_field(c, "user", "author", "comment_author")
            if isinstance(author, dict):
                author = _get_field(author, "user_login", "user_name", "name")
            content = _get_field(c, "comment_content", "comment")
            result += f"- ID: {cid}, Author: {author}, Comment: {content}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error listing note comments: {e!s}"


def _search_notes(case_id: int, search_term: str = "%") -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.search_notes(search_term=search_term, cid=case_id)
        data = _extract_data(resp, f"Searching notes for case {case_id}")
        items = _ensure_list(data)
        if not items:
            return f"No notes matched '{search_term}' in case {case_id}."
        result = f"Notes matching '{search_term}' in case {case_id}:\n"
        for note in items:
            nid = _get_field(note, "note_id", "id")
            title = _get_field(note, "note_title", "title")
            directory = _get_field(note, "directory_id", "note_directory_id", "dir_id")
            result += f"- ID: {nid}, Title: {title}, Directory: {directory}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error searching notes: {e!s}"


def _list_evidence(case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_evidences(cid=case_id)
        data = _extract_data(resp, f"Listing evidence for case {case_id}")
        items = _ensure_list(data)
        if not items:
            return f"No evidence found for case {case_id}."
        result = f"Evidence for Case {case_id}:\n"
        for ev in items:
            evid = _get_field(ev, "evidence_id", "id")
            name = _get_field(ev, "evidence_name", "name", "title", "filename")
            etype = _get_field(ev, "evidence_type", "type", "evidence_type_id", "type_id")
            tlp = _get_field(ev, "tlp", "tlp_name", "color")
            size = _get_field(ev, "file_size", "size")
            file_hash = _get_field(ev, "file_hash", "hash")
            desc = _get_field(ev, "file_description", "description", "evidence_description")
            added = _get_field(ev, "date_added", "created_at")

            if all(v is None for v in (evid, name, etype, tlp, size, file_hash, desc)):
                result += f"- {ev}\n"
            else:
                result += f"- ID: {evid}, Name: {name}, Type: {etype}, TLP: {tlp}, Size: {size}, Hash: {file_hash}, Added: {added}, Desc: {desc}\n"
        return result
    except Exception as e:
        return f"Error listing evidence: {e!s}"


def _add_evidence(
    case_id: int,
    filename: str | None = None,
    file_size: int | None = None,
    description: str = "",
    file_hash: str | None = None,
    custom_attributes: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
    name: str | None = None,
) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        extra = extra or {}
        filename = filename or name or extra.get("filename")
        if file_size is None:
            file_size = extra.get("file_size")
        if file_hash is None:
            file_hash = extra.get("file_hash")
        if custom_attributes is None:
            custom_attributes = extra.get("custom_attributes")

        if filename is None:
            raise ValueError("filename is required for evidence")
        if file_size is None:
            raise ValueError("file_size is required for evidence")

        resp = case_obj.add_evidence(
            filename=filename,
            file_size=file_size,
            description=description,
            file_hash=file_hash,
            custom_attributes=custom_attributes,
            cid=case_id,
        )
        data = _extract_data(resp, f"Adding evidence to case {case_id}")
        evid = _get_field(data, "evidence_id", "id")
        return f"Evidence added. ID: {evid}"
    except Exception as e:
        return f"Error adding evidence: {e!s}"


def _update_evidence(evidence_id: int, case_id: int | None = None, **fields: Any) -> str:
    try:
        session = get_iris_client()
        if case_id is None:
            case_id = fields.pop("cid", fields.pop("case_id", None))
        if case_id is None:
            raise ValueError("case_id is required for updating an evidence item")
        case_obj = _prepare_case(session, case_id)
        payload = {"evidence_id": evidence_id, "cid": case_id}
        payload.update({k: v for k, v in fields.items() if v is not None})
        resp = case_obj.update_evidence(**payload)
        _extract_data(resp, f"Updating evidence {evidence_id}")
        return f"Evidence {evidence_id} updated."
    except Exception as e:
        return f"Error updating evidence: {e!s}"


def _delete_evidence(evidence_id: int, case_id: int | None = None) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        payload = {"evidence_id": evidence_id}
        if case_id is not None:
            payload["cid"] = case_id
        resp = case_obj.delete_evidence(**payload)
        _extract_data(resp, f"Deleting evidence {evidence_id}")
        return f"Evidence {evidence_id} deleted."
    except Exception as e:
        return f"Error deleting evidence: {e!s}"


def _list_events(case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_events(cid=case_id)
        data = _extract_data(resp, f"Listing events for case {case_id}")
        items = _ensure_list(data)
        if not items:
            return f"No events found for case {case_id}."
        result = f"Events for Case {case_id}:\n"
        for ev in items:
            evid = _get_field(ev, "event_id", "id")
            name = _get_field(ev, "event_title", "event_name", "name", "title")
            desc = _get_field(ev, "event_content", "event_description", "description", "content")
            category = _get_field(ev, "category_name", "event_category", "category", "event_category_name", "event_category_id")
            tlp = _get_field(ev, "tlp", "tlp_name", "color", "event_color")
            dt = _get_field(ev, "event_date", "event_date_wtz", "date_time", "datetime", "event_datetime", "time", "timestamp")
            tz = _get_field(ev, "event_tz", "timezone", "timezone_string")
            if all(v is None for v in (evid, name, category, tlp, desc, dt)):
                result += f"- {ev}\n"
            else:
                when = f"{dt}{' ' + tz if tz else ''}"
                result += f"- ID: {evid}, Name: {name}, Category: {category}, TLP/Color: {tlp}, Time: {when}, Desc: {desc}\n"
        return result
    except Exception as e:
        return f"Error listing events: {e!s}"


def _add_event(
    case_id: int,
    name: str,
    description: str = "",
    category: str | int | None = None,
    date_time: str | None = None,
    raw_content: str | None = None,
    source: str | None = None,
    linked_assets: list[Any] | None = None,
    linked_iocs: list[Any] | None = None,
    tags: list[str] | None = None,
    color: str | None = None,
    display_in_graph: bool | None = None,
    display_in_summary: bool | None = None,
    custom_attributes: dict[str, Any] | None = None,
    timezone_string: str | None = None,
    sync_ioc_with_assets: bool = False,
    extra: dict[str, Any] | None = None,
    tlp: str | None = None,
) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        extra = extra or {}
        if date_time is None:
            date_time = extra.get("date_time") or extra.get("datetime")
        parsed_dt: Any = date_time
        if isinstance(parsed_dt, str):
            try:
                parsed_dt = datetime.fromisoformat(parsed_dt)
            except Exception:
                parsed_dt = None
        if parsed_dt is None:
            raise ValueError("date_time is required for an event and must be ISO format if string")

        if color is None and tlp is not None:
            color = tlp

        payload = {
            "title": name,
            "date_time": parsed_dt,
            "content": description,
            "raw_content": raw_content or extra.get("raw_content"),
            "source": source or extra.get("source"),
            "linked_assets": linked_assets or extra.get("linked_assets"),
            "linked_iocs": linked_iocs or extra.get("linked_iocs"),
            "category": category,
            "tags": tags or extra.get("tags"),
            "color": color,
            "display_in_graph": display_in_graph if display_in_graph is not None else extra.get("display_in_graph"),
            "display_in_summary": display_in_summary if display_in_summary is not None else extra.get("display_in_summary"),
            "custom_attributes": custom_attributes or extra.get("custom_attributes"),
            "timezone_string": timezone_string or extra.get("timezone_string"),
            "sync_ioc_with_assets": extra.get("sync_ioc_with_assets", sync_ioc_with_assets),
            "cid": case_id,
        }

        resp = case_obj.add_event(**{k: v for k, v in payload.items() if v is not None})
        data = _extract_data(resp, f"Adding event to case {case_id}")
        evid = _get_field(data, "event_id", "id")
        return f"Event added. ID: {evid}"
    except Exception as e:
        return f"Error adding event: {e!s}"


def _update_event(event_id: int, case_id: int | None = None, **fields: Any) -> str:
    try:
        session = get_iris_client()
        # Allow cid inside fields to avoid "No case ID provided" errors
        if case_id is None:
            case_id = fields.pop("cid", fields.pop("case_id", None))
        if case_id is None:
            raise ValueError("case_id is required for updating an event")
        case_obj = _prepare_case(session, case_id)
        payload = {"event_id": event_id, "cid": case_id}
        payload.update({k: v for k, v in fields.items() if v is not None})
        resp = case_obj.update_event(**payload)
        _extract_data(resp, f"Updating event {event_id}")
        return f"Event {event_id} updated."
    except Exception as e:
        return f"Error updating event: {e!s}"


def _delete_event(event_id: int, case_id: int | None = None) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        payload = {"event_id": event_id}
        if case_id is not None:
            payload["cid"] = case_id
        resp = case_obj.delete_event(**payload)
        _extract_data(resp, f"Deleting event {event_id}")
        return f"Event {event_id} deleted."
    except Exception as e:
        return f"Error deleting event: {e!s}"


@mcp.tool()
def list_notes(case_id: int) -> str:
    """List notes for a case (includes directory ids)."""
    return _list_notes(case_id)


@mcp.tool()
def list_note_directories(case_id: int) -> str:
    """List note directories for a case (best-effort across client versions)."""
    return _list_note_directories(case_id)


@mcp.tool()
def create_note_directory(case_id: int, name: str, parent_directory_id: int | None = None) -> str:
    """Create a note directory for a case (best-effort across client versions)."""
    return _create_note_directory(case_id, name, parent_directory_id)


@mcp.tool()
def list_evidence(case_id: int) -> str:
    """List evidence for a case (best-effort across client versions)."""
    return _list_evidence(case_id)


@mcp.tool()
def add_evidence(
    case_id: int,
    filename: str | None = None,
    file_size: int | None = None,
    description: str = "",
    file_hash: str | None = None,
    custom_attributes: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
    name: str | None = None,
) -> str:
    """Add evidence to a case."""
    return _add_evidence(case_id, filename, file_size, description, file_hash, custom_attributes, extra, name)


@mcp.tool()
def update_evidence(evidence_id: int, case_id: int | None = None, fields: dict[str, Any] | None = None) -> str:
    """Update evidence fields (pass additional fields in 'fields')."""
    fields = fields or {}
    return _update_evidence(evidence_id, case_id, **fields)


@mcp.tool()
def delete_evidence(evidence_id: int, case_id: int | None = None) -> str:
    """Delete an evidence item."""
    return _delete_evidence(evidence_id, case_id)


@mcp.tool()
def list_events(case_id: int) -> str:
    """List events for a case."""
    return _list_events(case_id)


@mcp.tool()
def add_event(
    case_id: int,
    name: str,
    description: str = "",
    category: str | int | None = None,
    date_time: str | None = None,
    raw_content: str | None = None,
    source: str | None = None,
    linked_assets: list[Any] | None = None,
    linked_iocs: list[Any] | None = None,
    tags: list[str] | None = None,
    color: str | None = None,
    display_in_graph: bool | None = None,
    display_in_summary: bool | None = None,
    custom_attributes: dict[str, Any] | None = None,
    timezone_string: str | None = None,
    sync_ioc_with_assets: bool = False,
    extra: dict[str, Any] | None = None,
    tlp: str | None = None,
) -> str:
    """Add an event to a case."""
    return _add_event(
        case_id,
        name,
        description,
        category,
        date_time,
        raw_content,
        source,
        linked_assets,
        linked_iocs,
        tags,
        color,
        display_in_graph,
        display_in_summary,
        custom_attributes,
        timezone_string,
        sync_ioc_with_assets,
        extra,
        tlp,
    )


@mcp.tool()
def update_event(event_id: int, case_id: int | None = None, fields: dict[str, Any] | None = None) -> str:
    """Update an event's fields (pass additional fields in 'fields')."""
    fields = fields or {}
    return _update_event(event_id, case_id, **fields)


@mcp.tool()
def delete_event(event_id: int, case_id: int | None = None) -> str:
    """Delete an event."""
    return _delete_event(event_id, case_id)


@mcp.tool()
def debug_case_methods(case_id: int, filter_text: str = "") -> str:
    """List available Case methods (optionally filtered), useful for wiring missing tools."""
    return _introspect_case_methods(case_id, filter_text)


@mcp.tool()
def add_note(
    case_id: int,
    content: str,
    title: str = "Note",
    directory_id: int | None = None,
    group_id: int | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    """
    Add a note to a case.
    """
    return _add_note(case_id, content, title, directory_id, group_id, custom_attributes)


@mcp.tool()
def get_note(case_id: int, note_id: int) -> str:
    """Fetch a specific note (title, directory, and content)."""
    return _get_note(note_id, case_id)


@mcp.tool()
def update_note(case_id: int, note_id: int, fields: dict[str, Any] | None = None) -> str:
    """Update a note (title/content/custom_attributes/directory_id)."""
    fields = fields or {}
    return _update_note(note_id, case_id, **fields)


@mcp.tool()
def delete_note(case_id: int, note_id: int) -> str:
    """Delete a note."""
    return _delete_note(note_id, case_id)


@mcp.tool()
def add_note_comment(case_id: int, note_id: int, comment: str) -> str:
    """Add a comment to a note."""
    return _add_note_comment(note_id, comment, case_id)


@mcp.tool()
def list_note_comments(case_id: int, note_id: int) -> str:
    """List comments for a note."""
    return _list_note_comments(note_id, case_id)


@mcp.tool()
def search_notes(case_id: int, search_term: str = "%") -> str:
    """Search notes by term (use '%' to list all titles/ids)."""
    return _search_notes(case_id, search_term)


# -------------------------------
# Task helpers
# -------------------------------


def _list_tasks(case_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_tasks(cid=case_id)
        data = _extract_data(resp, f"Listing tasks for case {case_id}")

        # The API returns a dict with 'tasks' key
        if isinstance(data, dict) and "tasks" in data:
            items = data["tasks"]
        else:
            items = _ensure_list(data)

        if not items:
            return f"No tasks found for case {case_id}."
        result = f"Tasks for Case {case_id}:\n"
        for task in items:
            tid = _get_field(task, "task_id", "id")
            title = _get_field(task, "task_title", "title", "name")
            status = _get_field(task, "task_status", "status", "status_name", "task_status_name")
            assignees = _get_field(task, "assignees", "task_assignees")
            result += f"- ID: {tid}, Title: {title}, Status: {status}, Assignees: {assignees}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error listing tasks: {e!s}"


def _add_task(
    case_id: int,
    title: str,
    status: str | int,
    assignees: list[str | int],
    description: str | None = None,
    tags: list[str] | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.add_task(
            title=title,
            status=status,
            assignees=assignees,
            description=description,
            tags=tags,
            custom_attributes=custom_attributes,
            cid=case_id,
        )
        data = _extract_data(resp, f"Adding task to case {case_id}")
        tid = _get_field(data, "task_id", "id")
        return f"Task added. ID: {tid}"
    except Exception as e:
        return f"Error adding task: {e!s}"


def _update_task(case_id: int, task_id: int, **fields: Any) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        payload = {"task_id": task_id, "cid": case_id}
        payload.update({k: v for k, v in fields.items() if v is not None})
        resp = case_obj.update_task(**payload)
        _extract_data(resp, f"Updating task {task_id}")
        return f"Task {task_id} updated."
    except Exception as e:
        return f"Error updating task: {e!s}"


def _delete_task(case_id: int, task_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.delete_task(task_id=task_id, cid=case_id)
        _extract_data(resp, f"Deleting task {task_id}")
        return f"Task {task_id} deleted."
    except Exception as e:
        return f"Error deleting task: {e!s}"


def _add_task_comment(case_id: int, task_id: int, comment: str) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.add_task_comment(task_id=task_id, comment=comment, cid=case_id)
        _extract_data(resp, f"Adding comment to task {task_id}")
        return f"Comment added to task {task_id}."
    except Exception as e:
        return f"Error adding task comment: {e!s}"


def _list_task_comments(case_id: int, task_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.list_task_comments(task_id=task_id, cid=case_id)
        data = _extract_data(resp, f"Listing task comments for task {task_id}")
        items = _ensure_list(data)
        if not items:
            return f"No comments found for task {task_id}."
        result = f"Comments for task {task_id}:\n"
        for c in items:
            cid = _get_field(c, "comment_id", "id")
            author = _get_field(c, "user", "author")
            if isinstance(author, dict):
                author = _get_field(author, "user_login", "user_name", "name")
            content = _get_field(c, "comment_content", "comment")
            result += f"- ID: {cid}, Author: {author}, Comment: {content}\n"
        return result.rstrip()
    except Exception as e:
        return f"Error listing task comments: {e!s}"


def _update_task_comment(case_id: int, task_id: int, comment_id: int, comment: str) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.update_task_comment(task_id=task_id, comment_id=comment_id, comment=comment, cid=case_id)
        _extract_data(resp, f"Updating comment {comment_id} on task {task_id}")
        return f"Task comment {comment_id} updated."
    except Exception as e:
        return f"Error updating task comment: {e!s}"


def _delete_task_comment(case_id: int, task_id: int, comment_id: int) -> str:
    try:
        session = get_iris_client()
        case_obj = _prepare_case(session, case_id)
        resp = case_obj.delete_task_comment(task_id=task_id, comment_id=comment_id, cid=case_id)
        _extract_data(resp, f"Deleting comment {comment_id} on task {task_id}")
        return f"Task comment {comment_id} deleted."
    except Exception as e:
        return f"Error deleting task comment: {e!s}"


@mcp.tool()
def list_tasks(case_id: int) -> str:
    """List tasks for a case."""
    return _list_tasks(case_id)


@mcp.tool()
def add_task(
    case_id: int,
    title: str,
    status: str | int,
    assignees: list[str | int],
    description: str | None = None,
    tags: list[str] | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    """Add a task to a case."""
    return _add_task(case_id, title, status, assignees, description, tags, custom_attributes)


@mcp.tool()
def update_task(case_id: int, task_id: int, fields: dict[str, Any] | None = None) -> str:
    """Update a task (status/title/assignees/etc)."""
    fields = fields or {}
    return _update_task(case_id, task_id, **fields)


@mcp.tool()
def delete_task(case_id: int, task_id: int) -> str:
    """Delete a task."""
    return _delete_task(case_id, task_id)


@mcp.tool()
def add_task_comment(case_id: int, task_id: int, comment: str) -> str:
    """Add a comment to a task."""
    return _add_task_comment(case_id, task_id, comment)


@mcp.tool()
def list_task_comments(case_id: int, task_id: int) -> str:
    """List comments for a task."""
    return _list_task_comments(case_id, task_id)


@mcp.tool()
def update_task_comment(case_id: int, task_id: int, comment_id: int, comment: str) -> str:
    """Update a task comment."""
    return _update_task_comment(case_id, task_id, comment_id, comment)


@mcp.tool()
def delete_task_comment(case_id: int, task_id: int, comment_id: int) -> str:
    """Delete a task comment."""
    return _delete_task_comment(case_id, task_id, comment_id)


def _list_assets(case_id: int) -> str:
    try:
        session = get_iris_client()
        assets = Case(session).list_assets(cid=case_id)
        data = _extract_data(assets, f"Listing assets for case {case_id}")
        items = _ensure_list(data)
        if not items:
            return f"No assets found for case {case_id}."

        result = f"Assets for Case {case_id}:\n"
        for asset in items:
            aid = _get_field(asset, "asset_id", "id")
            name = _get_field(asset, "asset_name", "name")
            atype = _get_field(asset, "asset_type_id", "asset_type", "asset_type_name")
            status = _get_field(asset, "analysis_status_id", "analysis_status", "analysis_status_name")

            if aid is None and name is None and atype is None and status is None:
                result += f"- {asset}\n"
            else:
                result += f"- ID: {aid}, Name: {name}, Type: {atype}, Status: {status}\n"
        return result
    except Exception as e:
        return f"Error listing assets: {e!s}"


@mcp.tool()
def list_assets(case_id: int) -> str:
    """
    List assets for a specific case.
    """
    return _list_assets(case_id)


def _add_asset(
    case_id: int,
    name: str,
    asset_type: str,
    analysis_status: str = "New",
    description: str = "",
    compromise_status: str | int | None = None,
    tags: list[str] | str | None = None,
    domain: str | None = None,
    ip: str | None = None,
    additional_info: str | None = None,
    ioc_links: list[int] | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    try:
        session = get_iris_client()
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        asset = Case(session).add_asset(
            name=name,
            asset_type=asset_type,
            analysis_status=analysis_status,
            compromise_status=compromise_status,
            tags=tags,
            description=description,
            domain=domain,
            ip=ip,
            additional_info=additional_info,
            ioc_links=ioc_links,
            custom_attributes=custom_attributes,
            cid=case_id,
        )
        data = _extract_data(asset, f"Adding asset to case {case_id}")
        return f"Asset added successfully. ID: {_get_field(data, 'asset_id', 'id')}"
    except Exception as e:
        return f"Error adding asset: {e!s}"


@mcp.tool()
def add_asset(
    case_id: int,
    name: str,
    asset_type: str,
    analysis_status: str = "New",
    description: str = "",
    compromise_status: str | int | None = None,
    tags: list[str] | str | None = None,
    domain: str | None = None,
    ip: str | None = None,
    additional_info: str | None = None,
    ioc_links: list[int] | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    """
    Add an asset to a case.
    """
    return _add_asset(
        case_id,
        name,
        asset_type,
        analysis_status,
        description,
        compromise_status,
        tags,
        domain,
        ip,
        additional_info,
        ioc_links,
        custom_attributes,
    )


def _list_iocs(case_id: int) -> str:
    try:
        session = get_iris_client()
        iocs = Case(session).list_iocs(cid=case_id)
        data = _extract_data(iocs, f"Listing IOCs for case {case_id}")
        items = _ensure_list(data)
        if not items:
            return f"No IOCs found for case {case_id}."

        result = f"IOCs for Case {case_id}:\n"
        for ioc in items:
            iid = _get_field(ioc, "ioc_id", "id")
            value = _get_field(ioc, "ioc_value", "value", "ioc", "indicator")
            itype = _get_field(ioc, "ioc_type", "ioc_type_id", "ioc_type_name", "type")
            desc = _get_field(ioc, "ioc_description", "description", "ioc_desc")
            tlp = _get_field(ioc, "tlp_name", "ioc_tlp", "ioc_tlp_id", "tlp")
            tags = _get_field(ioc, "ioc_tags", "tags")

            if iid is None and value is None and itype is None and desc is None:
                result += f"- {ioc}\n"
            else:
                result += f"- ID: {iid}, Value: {value}, Type: {itype}, TLP: {tlp}, Tags: {tags}, Description: {desc}\n"
        return result
    except Exception as e:
        return f"Error listing IOCs: {e!s}"


@mcp.tool()
def list_iocs(case_id: int) -> str:
    """
    List IOCs for a specific case.
    """
    return _list_iocs(case_id)


def _add_ioc(
    case_id: int,
    value: str,
    ioc_type: str,
    description: str = "",
    ioc_tlp: str | int | None = None,
    ioc_tags: list[str] | str | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    try:
        session = get_iris_client()
        if isinstance(ioc_tags, str):
            ioc_tags = [t.strip() for t in ioc_tags.split(",") if t.strip()]
        ioc = Case(session).add_ioc(
            value=value,
            ioc_type=ioc_type,
            description=description,
            ioc_tlp=ioc_tlp,
            ioc_tags=ioc_tags,
            custom_attributes=custom_attributes,
            cid=case_id,
        )
        data = _extract_data(ioc, f"Adding IOC to case {case_id}")
        return f"IOC added successfully. ID: {_get_field(data, 'ioc_id', 'id')}"
    except Exception as e:
        return f"Error adding IOC: {e!s}"


@mcp.tool()
def add_ioc(
    case_id: int,
    value: str,
    ioc_type: str,
    description: str = "",
    ioc_tlp: str | int | None = None,
    ioc_tags: list[str] | str | None = None,
    custom_attributes: dict[str, Any] | None = None,
) -> str:
    """
    Add an IOC to a case.
    """
    return _add_ioc(case_id, value, ioc_type, description, ioc_tlp, ioc_tags, custom_attributes)


def _list_customers() -> str:
    try:
        session = get_iris_client()
        customers = Customer(session).list_customers()
        data = _extract_data(customers, "Listing customers")
        items = _ensure_list(data)
        if not items:
            return "No customers found."

        result = "Customers:\n"
        for customer in items:
            cid = _get_field(customer, "customer_id", "id")
            name = _get_field(customer, "customer_name", "name")
            sector = _get_field(customer, "customer_sector", "sector")
            result += f"- ID: {cid}, Name: {name}, Sector: {sector}\n"
        return result
    except Exception as e:
        return f"Error listing customers: {e!s}"


@mcp.tool()
def list_customers() -> str:
    """
    List all customers.
    """
    return _list_customers()


def _get_customer_by_id(customer_id: int) -> str:
    try:
        session = get_iris_client()
        customer = Customer(session).get_customer_by_id(customer_id=customer_id)
        data = _extract_data(customer, f"Getting customer {customer_id}")
        if not data:
            return f"Customer with ID {customer_id} not found."

        name = _get_field(data, "customer_name", "name")
        sector = _get_field(data, "customer_sector", "sector")
        description = _get_field(data, "customer_description", "description")
        return f"Customer Details:\nID: {customer_id}\nName: {name}\nSector: {sector}\nDescription: {description}"
    except Exception as e:
        return f"Error getting customer {customer_id}: {e!s}"


@mcp.tool()
def get_customer_by_id(customer_id: int) -> str:
    """
    Get a customer by ID.
    """
    return _get_customer_by_id(customer_id)


def _lookup_customer(customer_name: str) -> str:
    try:
        session = get_iris_client()
        customer = Customer(session).lookup_customer(customer_name=customer_name)
        data = _extract_data(customer, f"Looking up customer {customer_name}")
        if not data:
            return f"Customer '{customer_name}' not found."

        cid = _get_field(data, "customer_id", "id")
        name = _get_field(data, "customer_name", "name") or customer_name
        return f"Customer found. ID: {cid}, Name: {name}"
    except Exception as e:
        return f"Error looking up customer '{customer_name}': {e!s}"


@mcp.tool()
def lookup_customer(customer_name: str) -> str:
    """
    Lookup a customer ID by name.
    """
    return _lookup_customer(customer_name)


def run() -> None:
    """Entry point for the iris-mcp console script."""
    mcp.run(transport="http", host="127.0.0.1", port=9000)


if __name__ == "__main__":
    run()
