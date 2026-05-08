from typing import Optional

from campus_map import KNOWN_LOCATIONS
from utils import generate_request_id


REQUEST_TYPE_CHOICES = {
    1: "Navigation_Only",
    2: "Eligibility_Check",
    3: "Booking_or_Scheduling",
    4: "Urgent_Service_Request",
    5: "Full_Service_Request",
}

ALLOWED_ROLES = ["student", "instructor", "staff"]

ALLOWED_CATEGORY_INPUTS = {
    "ai_lab_support": "AI_Lab_Support",
    "ai lab support": "AI_Lab_Support",
    "ai_lab": "AI_Lab_Support",
    "ai lab": "AI_Lab_Support",
    "viva": "Viva_Scheduling",
    "viva_scheduling": "Viva_Scheduling",
    "access": "Access_Request",
    "access_request": "Access_Request",
    "maintenance": "Maintenance",
    "emergency_help": "Emergency_Help",
    "emergency": "Emergency_Help",
}

ALLOWED_CATEGORY_LABELS = [
    "AI_Lab_Support",
    "Viva_Scheduling (Viva)",
    "Access_Request (Access)",
    "Maintenance",
    "Emergency_Help",
]

LOCATION_INPUTS = {
    "hostel": "Hostel",
    "ai_lab": "AI_Lab",
    "ai lab": "AI_Lab",
    "library": "Library",
    "auditorium": "Auditorium",
    "cafeteria": "Cafeteria",
    "science_block": "Science_Block",
    "science block": "Science_Block",
}


def prompt_text(label: str, required: bool = True) -> Optional[str]:
    # Collect a required or optional text value from the user.
    # Loop until a valid input is provided.
    while True:
        value = input(label).strip()
        if not value:
            if required:
                print("Value is required.")
                continue
            return None
        return value


def prompt_role() -> str:
    # Collect and validate the user's role.
    # Only allow roles from the approved list.
    while True:
        value = input("Enter Role (student/instructor/staff): ").strip().lower()
        if value in ALLOWED_ROLES:
            return value
        print("Invalid role. Try again.")


def prompt_int(
    label: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    allow_blank: bool = False,
) -> Optional[int]:
    # Collect an integer value with optional range validation.
    # Reject invalid numbers and enforce bounds when provided.
    while True:
        value = input(label).strip()
        if not value:
            if allow_blank:
                return None
            print("Value is required.")
            continue
        try:
            num = int(value)
        except ValueError:
            print("Enter a valid number.")
            continue
        if min_value is not None and num < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and num > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return num


def prompt_request_type() -> str:
    # Display request type choices and return the selected value.
    # Uses the numbered menu to avoid invalid request_type input.
    print("Enter Request Type:")
    for key in sorted(REQUEST_TYPE_CHOICES.keys()):
        print(f"{key}. {REQUEST_TYPE_CHOICES[key]}")
    choice = prompt_int("Enter choice: ", min_value=1, max_value=5)
    if choice is None:
        raise ValueError("Request type choice is required")
    return REQUEST_TYPE_CHOICES[choice]


def prompt_yes_no(label: str, default: bool = False) -> bool:
    # Collect a yes/no answer with a default fallback.
    # Keeps input handling consistent for optional flags.
    suffix = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} ({suffix}): ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Enter y or n.")


def prompt_location(label: str, required: bool = True) -> Optional[str]:
    # Collect a campus location and validate against known nodes.
    # Enforces strict location input to avoid invalid routes.
    allowed_locations = ", ".join(sorted(KNOWN_LOCATIONS))
    while True:
        value = input(label).strip()
        if not value:
            if required:
                print(f"Value is required. Allowed: {allowed_locations}.")
                continue
            return None
        if value in KNOWN_LOCATIONS:
            return value
        key = value.strip().lower().replace(" ", "_")
        if key in LOCATION_INPUTS:
            candidate = LOCATION_INPUTS[key]
            if candidate in KNOWN_LOCATIONS:
                return candidate
        print(f"Invalid location. Allowed: {allowed_locations}.")


def prompt_category(label: str) -> str:
    # Collect a category and map it to a canonical value.
    # Only accepts known categories to prevent invalid requests.
    allowed_labels = ", ".join(ALLOWED_CATEGORY_LABELS)
    while True:
        value = input(label).strip()
        if not value:
            print(f"Value is required. Allowed: {allowed_labels}.")
            continue
        key = value.strip().lower().replace(" ", "_")
        if key in ALLOWED_CATEGORY_INPUTS:
            return ALLOWED_CATEGORY_INPUTS[key]
        print(f"Invalid category. Allowed: {allowed_labels}.")


def collect_request() -> dict:
    # Collect structured request fields based on the selected request type.
    # Produces a raw request dict ready for preprocessing.
    raw = {"request_id": generate_request_id()}
    raw["name"] = prompt_text("Enter Name: ")
    raw["role"] = prompt_role()
    raw["request_type"] = prompt_request_type()
    raw["eligibility_claim"] = True

    request_type = raw["request_type"]

    if request_type == "Navigation_Only":
        raw["current_location"] = prompt_location("Enter Current Location: ")
        raw["destination"] = prompt_location("Enter Destination: ")

    elif request_type == "Eligibility_Check":
        raw["query"] = prompt_text("Enter Query: ")

    elif request_type == "Booking_or_Scheduling":
        raw["category"] = prompt_category(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance / Emergency_Help): "
        )
        raw["preferred_slot"] = prompt_int("Enter Preferred Slot (1-4): ", 1, 4)
        raw["group_id"] = prompt_text("Enter Group ID (optional): ", required=False)
        raw["current_location"] = prompt_location(
            "Enter Current Location (optional for route): ", required=False
        )
        raw["route_requested"] = prompt_yes_no(
            "Need route guidance after assignment?", default=False
        )

    elif request_type == "Urgent_Service_Request":
        raw["category"] = prompt_category(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance / Emergency_Help): "
        )
        raw["current_location"] = prompt_location("Enter Current Location: ")
        raw["severity"] = prompt_int("Enter Severity (1-10): ", 1, 10)
        raw["time_sensitivity"] = prompt_int("Enter Time Sensitivity (1-10): ", 1, 10)
        raw["crowd_level"] = prompt_int("Enter Crowd Level (1-10): ", 1, 10)
        raw["preferred_slot"] = prompt_int(
            "Enter Preferred Slot (optional 1-4): ", 1, 4, allow_blank=True
        )
        raw["route_requested"] = prompt_yes_no(
            "Need route guidance after assignment?", default=True
        )

    elif request_type == "Full_Service_Request":
        raw["category"] = prompt_category(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance / Emergency_Help): "
        )
        raw["current_location"] = prompt_location("Enter Current Location: ")
        raw["preferred_slot"] = prompt_int("Enter Preferred Slot (1-4): ", 1, 4)
        raw["severity"] = prompt_int("Enter Severity (1-10): ", 1, 10)
        raw["time_sensitivity"] = prompt_int("Enter Time Sensitivity (1-10): ", 1, 10)
        raw["crowd_level"] = prompt_int("Enter Crowd Level (1-10): ", 1, 10)
        raw["description_note"] = prompt_text(
            "Enter Description Note (optional): ", required=False
        )

    return raw
