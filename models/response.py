from typing import Optional

FINAL_RESPONSE_TEMPLATE = {
    "request_id": "",
    "decision": "",
    "priority": {},
    "eligibility": {},
    "assignment": {},
    "route": {},
    "message": "",
}

ROUTER_OUTPUT_TEMPLATE = {
    "request_id": "",
    "selected_pipeline": [],
    "needs_ann": False,
    "needs_logic": False,
    "needs_csp": False,
    "needs_search": False,
}

PRIORITY_OUTPUT_TEMPLATE = {
    "binary_priority": "",
    "final_priority": "",
    "confidence": 0.0,
}

LOGIC_OUTPUT_TEMPLATE = {
    "allowed": False,
    "entailed": False,
    "explanation": "",
}

CSP_OUTPUT_TEMPLATE = {
    "decision": "",
    "assigned_room": "",
    "assigned_slot": None,
    "destination": "",
    "notes": "",
}

SEARCH_OUTPUT_TEMPLATE = {
    "algorithm_used": "",
    "path": [],
    "cost": 0,
    "steps": 0,
}


def build_final_response(
    request_id: str,
    decision: str,
    priority: Optional[dict] = None,
    eligibility: Optional[dict] = None,
    assignment: Optional[dict] = None,
    route: Optional[dict] = None,
    message: str = "",
) -> dict:
    response = FINAL_RESPONSE_TEMPLATE.copy()
    response["request_id"] = request_id
    response["decision"] = decision
    response["priority"] = priority or {}
    response["eligibility"] = eligibility or {}
    response["assignment"] = assignment or {}
    response["route"] = route or {}
    response["message"] = message
    return response
