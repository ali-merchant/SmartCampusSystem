from models.response import build_final_response


def compose_response(
    request,
    router_output,
    ann_output=None,
    logic_output=None,
    csp_output=None,
    search_output=None,
    rejection_reason: str = "",
) -> dict:
    decision = resolve_decision(request.request_type, rejection_reason)

    priority = ann_output if router_output.get("needs_ann") and ann_output else {}
    eligibility = build_eligibility(request, router_output, logic_output, decision)
    assignment = build_assignment(router_output, csp_output, decision)
    route = build_route(router_output, search_output, decision)
    message = build_message(
        request,
        decision,
        assignment,
        route,
        logic_output,
        rejection_reason,
    )

    return build_final_response(
        request_id=request.request_id,
        decision=decision,
        priority=priority,
        eligibility=eligibility,
        assignment=assignment,
        route=route,
        message=message,
    )


def resolve_decision(request_type: str, rejection_reason: str) -> str:
    if rejection_reason:
        return "rejected"
    if request_type == "Navigation_Only":
        return "completed"
    if request_type == "Eligibility_Check":
        return "answered"
    return "accepted"


def build_eligibility(request, router_output, logic_output, decision: str) -> dict:
    if not router_output.get("needs_logic") or not logic_output:
        return {}

    if request.request_type == "Eligibility_Check":
        return {
            "entailed": bool(logic_output.get("entailed")),
            "explanation": logic_output.get("explanation", ""),
        }

    allowed = bool(logic_output.get("allowed"))
    eligibility = {"allowed": allowed}
    if decision == "rejected":
        eligibility["explanation"] = logic_output.get("explanation", "")
    return eligibility


def build_assignment(router_output, csp_output, decision: str) -> dict:
    if decision == "rejected" or not router_output.get("needs_csp"):
        return {}
    if not csp_output:
        return {}
    return {
        "room": csp_output.get("assigned_room", ""),
        "slot": csp_output.get("assigned_slot"),
    }


def build_route(router_output, search_output, decision: str) -> dict:
    if decision == "rejected" or not router_output.get("needs_search"):
        return {}
    if not search_output:
        return {}
    return {
        "algorithm": search_output.get("algorithm_used", ""),
        "path": search_output.get("path", []),
        "cost": search_output.get("cost", 0),
        "steps": search_output.get("steps", 0),
    }


def build_message(
    request,
    decision: str,
    assignment: dict,
    route: dict,
    logic_output,
    rejection_reason: str,
) -> str:
    if decision == "rejected":
        reason = rejection_reason or "the request could not be processed"
        return f"Your request has been rejected because {reason}."

    if request.request_type == "Navigation_Only":
        return "Best route generated successfully."

    if request.request_type == "Eligibility_Check":
        return "Eligibility query answered successfully."

    if request.request_type == "Booking_or_Scheduling":
        return "Booking assigned successfully."

    if request.request_type in {"Urgent_Service_Request", "Full_Service_Request"}:
        room = assignment.get("room")
        slot = assignment.get("slot")
        if room and slot is not None:
            if route:
                return (
                    "Your request has been accepted. You are assigned "
                    f"{room} in slot {slot}. Please follow the recommended route."
                )
            return (
                "Your request has been accepted. You are assigned "
                f"{room} in slot {slot}."
            )
        return "Your request has been accepted."

    if logic_output and logic_output.get("allowed") is False:
        return "Your request is not eligible."

    return "Request processed successfully."
