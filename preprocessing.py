from typing import Optional

from campus_map import KNOWN_LOCATIONS
from models.request import Request
from modules.search_module import estimate_distance
from utils import generate_request_id


CATEGORY_MAP = {
    "ai lab": "AI_Lab_Support",
    "ai_lab": "AI_Lab_Support",
    "ai_lab_support": "AI_Lab_Support",
    "viva": "Viva_Scheduling",
    "viva_scheduling": "Viva_Scheduling",
    "access": "Access_Request",
    "access_request": "Access_Request",
    "maintenance": "Maintenance",
    "emergency": "Emergency_Help",
    "emergency_help": "Emergency_Help",
}

ALLOWED_CATEGORIES = {
    "AI_Lab_Support",
    "Viva_Scheduling",
    "Access_Request",
    "Maintenance",
    "Emergency_Help",
}

LOCATION_MAP = {
    "hostel": "Hostel",
    "ai_lab": "AI_Lab",
    "library": "Library",
    "auditorium": "Auditorium",
    "cafeteria": "Cafeteria",
    "science_block": "Science_Block",
}

REQUEST_TYPE_MAP = {
    "navigation_only": "Navigation_Only",
    "eligibility_check": "Eligibility_Check",
    "booking_or_scheduling": "Booking_or_Scheduling",
    "urgent_service_request": "Urgent_Service_Request",
    "full_service_request": "Full_Service_Request",
}

REQUEST_TYPE_BY_CHOICE = {
    1: "Navigation_Only",
    2: "Eligibility_Check",
    3: "Booking_or_Scheduling",
    4: "Urgent_Service_Request",
    5: "Full_Service_Request",
}


def normalize_location(value: Optional[str]) -> Optional[str]:
    # Normalize a location string to the canonical campus node name.
    # Returns None when the input is empty.
    if not value:
        return None
    key = value.strip().lower().replace(" ", "_")
    return LOCATION_MAP.get(key, value.strip())


def normalize_category(value: Optional[str]) -> Optional[str]:
    # Normalize a category string to the standard category label.
    # Returns None when the input is empty.
    if not value:
        return None
    key = value.strip().lower()
    return CATEGORY_MAP.get(key, value.strip())


def normalize_request_type(value: Optional[str]) -> str:
    # Normalize request type strings to the official request_type values.
    # Returns an empty string for missing input to trigger validation errors.
    if not value:
        return ""
    key = value.strip().lower().replace(" ", "_")
    return REQUEST_TYPE_MAP.get(key, value.strip())


def parse_int(value: Optional[object], field_name: str) -> Optional[int]:
    # Convert a value to int or raise a clear error for invalid input.
    # Empty strings return None to support optional numeric fields.
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        if value.strip() == "":
            return None
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"{field_name} must be an integer") from exc
    raise ValueError(f"{field_name} must be an integer")
    return None


def validate_location(field_name: str, value: Optional[str]):
    # Ensure a location value exists in the known campus map.
    # Raises a ValueError to block invalid nodes.
    if value and value not in KNOWN_LOCATIONS:
        allowed = ", ".join(sorted(KNOWN_LOCATIONS))
        raise ValueError(f"{field_name} must be one of: {allowed}")


def validate_category(value: Optional[str]):
    # Validate category against the allowed category list.
    # Rejects unknown categories to enforce strict input.
    if value and value not in ALLOWED_CATEGORIES:
        allowed = ", ".join(sorted(ALLOWED_CATEGORIES))
        raise ValueError(f"category must be one of: {allowed}")


def validate_slot(value: Optional[int]):
    # Validate slot selections against the allowed range.
    # Raises a ValueError for out-of-range values.
    if value is None:
        return
    if value not in {1, 2, 3, 4}:
        raise ValueError("preferred_slot must be between 1 and 4")


def validate_scale(field_name: str, value: Optional[int]):
    # Validate numeric scales like severity or crowd level.
    # Raises a ValueError if the value is outside 1-10.
    if value is None:
        return
    if value < 1 or value > 10:
        raise ValueError(f"{field_name} must be between 1 and 10")


def preprocess_request(raw: dict):
    # Normalize, validate, and build a standard Request with module inputs.
    # Returns the Request object and module-specific prepared data.
    data = dict(raw)
    route_requested = bool(data.pop("route_requested", False))

    if not data.get("request_id"):
        data["request_id"] = generate_request_id()

    if not data.get("request_type") and data.get("choice"):
        data["request_type"] = REQUEST_TYPE_BY_CHOICE.get(data.get("choice"))
    data.pop("choice", None)

    data["request_type"] = normalize_request_type(data.get("request_type"))
    data["role"] = (data.get("role") or "").strip().lower()
    data["current_location"] = normalize_location(data.get("current_location"))
    data["destination"] = normalize_location(data.get("destination"))
    data["category"] = normalize_category(data.get("category"))
    data["group_id"] = data.get("group_id") or ""
    data["description_note"] = data.get("description_note") or ""
    if data.get("eligibility_claim") is None:
        data["eligibility_claim"] = True

    data["preferred_slot"] = parse_int(data.get("preferred_slot"), "preferred_slot")
    data["severity"] = parse_int(data.get("severity"), "severity")
    data["time_sensitivity"] = parse_int(data.get("time_sensitivity"), "time_sensitivity")
    data["crowd_level"] = parse_int(data.get("crowd_level"), "crowd_level")

    validate_location("current_location", data.get("current_location"))
    validate_location("destination", data.get("destination"))
    validate_category(data.get("category"))
    validate_slot(data.get("preferred_slot"))
    validate_scale("severity", data.get("severity"))
    validate_scale("time_sensitivity", data.get("time_sensitivity"))
    validate_scale("crowd_level", data.get("crowd_level"))

    request = Request(**data)

    distance = estimate_distance(request.current_location, request.destination)

    module_inputs = {
        "logic_query": data.get("query"),
        "route_requested": route_requested,
        "search": {
            "source": request.current_location,
            "destination": request.destination,
        },
        "ann_features": {
            "severity": request.severity or 0,
            "time_sensitivity": request.time_sensitivity or 0,
            "crowd_level": request.crowd_level or 0,
            "distance": distance,
            "eligibility": bool(request.eligibility_claim),
        },
        "csp": {
            "category": request.category,
            "preferred_slot": request.preferred_slot,
            "group_id": request.group_id,
        },
    }

    return request, module_inputs
