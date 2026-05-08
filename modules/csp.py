from models.response import CSP_OUTPUT_TEMPLATE


ROOM_BY_CATEGORY = {
    "AI_Lab_Support": "AI_Lab",
    "Viva_Scheduling": "Auditorium",
    "Access_Request": "Library",
    "Maintenance": "Library",
    "Emergency_Help": "AI_Lab",
}

AVAILABLE_SLOTS = [1, 2, 3, 4]


def assign_slot(request, csp_inputs: dict) -> dict:
    # Assign a room and time slot based on category and preference.
    # Returns a standard CSP output with acceptance or rejection.
    output = CSP_OUTPUT_TEMPLATE.copy()

    if not request.category:
        output["decision"] = "rejected"
        output["notes"] = "Missing category for scheduling."
        return output

    preferred = csp_inputs.get("preferred_slot")
    if preferred in AVAILABLE_SLOTS:
        slot = preferred
        notes = "Preferred slot assigned."
    else:
        slot = AVAILABLE_SLOTS[0] if AVAILABLE_SLOTS else None
        notes = "Preferred slot unavailable. Assigned next available slot."

    if slot is None:
        output["decision"] = "rejected"
        output["notes"] = "No slots available."
        return output

    output["decision"] = "accepted"
    output["assigned_room"] = ROOM_BY_CATEGORY.get(request.category, "AI_Lab")
    output["assigned_slot"] = slot
    output["destination"] = output["assigned_room"]
    output["notes"] = notes
    return output
