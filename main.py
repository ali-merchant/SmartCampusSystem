from models.request import Request
from models.response import build_final_response
from pprint import pprint
from router import route_request


KNOWN_LOCATIONS = {"Hostel", "AI_Lab", "Library", "Auditorium"}

CATEGORY_MAP = {
    "ai lab": "AI_Lab_Support",
    "ai_lab": "AI_Lab_Support",
    "viva": "Viva",
    "access": "Access",
    "maintenance": "Maintenance",
}

def normalize_location(value: str) -> str:
    v = value.strip()
    if not v:
        return v
    return v[:1].upper() + v[1:].lower()

def normalize_category(value: str) -> str:
    return CATEGORY_MAP.get(value.strip().lower(), value.strip())

def preprocess(raw: dict):
    # normalize fields
    raw["current_location"] = normalize_location(raw.get("current_location", ""))
    raw["destination"] = normalize_location(raw.get("destination", ""))
    raw["category"] = normalize_category(raw.get("category", ""))

    # build and validate request object
    request = Request(**raw)

    # prepare module inputs (example stubs)
    module_inputs = {
        "logic_query": raw.get("query"),
        "search": {
            "source": request.current_location,
            "destination": request.destination,
        },
        "ann_features": {
            "severity": request.severity,
            "time_sensitivity": request.time_sensitivity,
            "crowd_level": request.crowd_level,
        },
        "csp": {
            "category": request.category,
            "preferred_slot": request.preferred_slot,
            "group_id": request.group_id,
        },
    }

    return request, module_inputs

def inp():
    raw = {
        "request_id": "REQ403",
        "name": "Ali",
        "role": "student",
        "request_type": "Full_Service_Request",
        "category": "ai lab",  # will normalize to AI_Lab_Support
        "current_location": "hostel",  # will normalize to Hostel
        "preferred_slot": 2,
        "severity": 8,
        "time_sensitivity": 9,
        "crowd_level": 5,
        "description_note": "Need urgent help before practical evaluation",
    }

    try:
        request, module_inputs = preprocess(raw)
        router_output = route_request(request)

        print("Request type:", request.request_type)
        print("Router output:")
        pprint(router_output, width=80, sort_dicts=False)
        print("Prepared module inputs:")
        pprint(module_inputs, width=80, sort_dicts=False)

        response = build_final_response(
            request_id=request.request_id,
            decision="accepted",
            message="Request accepted for processing.",
        )
        print("Final response template:")
        pprint(response, width=80, sort_dicts=False)
    except ValueError as e:
        print("Invalid input:", e)

if __name__ == "__main__":
    inp()