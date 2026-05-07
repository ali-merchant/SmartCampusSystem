from typing import Optional

from utils import generate_request_id


REQUEST_TYPE_CHOICES = {
    1: "Navigation_Only",
    2: "Eligibility_Check",
    3: "Booking_or_Scheduling",
    4: "Urgent_Service_Request",
    5: "Full_Service_Request",
}

ALLOWED_ROLES = ["student", "instructor", "staff"]


def prompt_text(label: str, required: bool = True) -> Optional[str]:
    while True:
        value = input(label).strip()
        if not value:
            if required:
                print("Value is required.")
                continue
            return None
        return value


def prompt_role() -> str:
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
    print("Enter Request Type:")
    for key in sorted(REQUEST_TYPE_CHOICES.keys()):
        print(f"{key}. {REQUEST_TYPE_CHOICES[key]}")
    choice = prompt_int("Enter choice: ", min_value=1, max_value=5)
    return REQUEST_TYPE_CHOICES[choice]


def prompt_yes_no(label: str, default: bool = False) -> bool:
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


def collect_request() -> dict:
    raw = {"request_id": generate_request_id()}
    raw["name"] = prompt_text("Enter Name: ")
    raw["role"] = prompt_role()
    raw["request_type"] = prompt_request_type()
    raw["eligibility_claim"] = True

    rt = raw["request_type"]

    if rt == "Navigation_Only":
        raw["current_location"] = prompt_text("Enter Current Location: ")
        raw["destination"] = prompt_text("Enter Destination: ")

    elif rt == "Eligibility_Check":
        raw["query"] = prompt_text("Enter Query: ")

    elif rt == "Booking_or_Scheduling":
        raw["category"] = prompt_text(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance): "
        )
        raw["preferred_slot"] = prompt_int("Enter Preferred Slot (1-4): ", 1, 4)
        raw["group_id"] = prompt_text("Enter Group ID (optional): ", required=False)
        raw["current_location"] = prompt_text(
            "Enter Current Location (optional for route): ", required=False
        )
        raw["route_requested"] = prompt_yes_no(
            "Need route guidance after assignment?", default=False
        )

    elif rt == "Urgent_Service_Request":
        raw["category"] = prompt_text(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance): "
        )
        raw["current_location"] = prompt_text("Enter Current Location: ")
        raw["severity"] = prompt_int("Enter Severity (1-10): ", 1, 10)
        raw["time_sensitivity"] = prompt_int("Enter Time Sensitivity (1-10): ", 1, 10)
        raw["crowd_level"] = prompt_int("Enter Crowd Level (1-10): ", 1, 10)
        raw["preferred_slot"] = prompt_int(
            "Enter Preferred Slot (optional 1-4): ", 1, 4, allow_blank=True
        )
        raw["route_requested"] = prompt_yes_no(
            "Need route guidance after assignment?", default=True
        )

    elif rt == "Full_Service_Request":
        raw["category"] = prompt_text(
            "Enter Category (AI_Lab_Support / Viva / Access / Maintenance): "
        )
        raw["current_location"] = prompt_text("Enter Current Location: ")
        raw["preferred_slot"] = prompt_int("Enter Preferred Slot (1-4): ", 1, 4)
        raw["severity"] = prompt_int("Enter Severity (1-10): ", 1, 10)
        raw["time_sensitivity"] = prompt_int("Enter Time Sensitivity (1-10): ", 1, 10)
        raw["crowd_level"] = prompt_int("Enter Crowd Level (1-10): ", 1, 10)
        raw["description_note"] = prompt_text(
            "Enter Description Note (optional): ", required=False
        )

    return raw
