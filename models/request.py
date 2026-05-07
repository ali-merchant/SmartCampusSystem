from dataclasses import dataclass, field
from typing import Optional

REQUEST_TEMPLATE = {
    "request_id": "",
    "name": "",
    "role": "",
    "request_type": "",
    "category": "",
    "current_location": "",
    "destination": "",
    "preferred_slot": None,
    "severity": 0,
    "time_sensitivity": 0,
    "crowd_level": 0,
    "group_id": "",
    "query": "",
    "eligibility_claim": False,
    "description_note": "",
}

REQUEST_TYPES = {
    "Navigation_Only",
    "Eligibility_Check",
    "Booking_or_Scheduling",
    "Urgent_Service_Request",
    "Full_Service_Request",
}


@dataclass
class Request:
    request_id: str
    name: str
    role: str
    request_type: str

    category: Optional[str] = None
    current_location: Optional[str] = None
    destination: Optional[str] = None
    preferred_slot: Optional[int] = None
    severity: Optional[int] = None
    time_sensitivity: Optional[int] = None
    crowd_level: Optional[int] = None
    group_id: Optional[str] = ""
    query: Optional[str] = None
    eligibility_claim: bool = False
    description_note: Optional[str] = ""

    _normalized_role: str = field(init=False, repr=False)

    def __post_init__(self):
        self._validate_request_id()
        self._validate_name()
        self._validate_role()
        self._validate_request_type()
        self._validate_conditionals()

    def _validate_request_id(self):
        if not self.request_id or not isinstance(self.request_id, str):
            raise ValueError("request_id is required")

    def _validate_name(self):
        if not self.name or len(self.name) >= 30:
            raise ValueError("Name must be less than 30 characters")

    def _validate_role(self):
        allowed = ["student", "instructor", "staff"]
        if self.role is None or self.role.lower() not in allowed:
            raise ValueError(f"Invalid role. Must be one of: {allowed}")
        self.role = self.role.lower()
        self._normalized_role = self.role

    def _validate_request_type(self):
        if self.request_type not in REQUEST_TYPES:
            raise ValueError(f"Invalid request_type. Must be one of: {sorted(REQUEST_TYPES)}")

    def _validate_conditionals(self):
        rt = self.request_type

        if rt == "Navigation_Only":
            if not self.current_location or not self.destination:
                raise ValueError("Navigation_Only requires current_location and destination")

        elif rt == "Eligibility_Check":
            if not self.query:
                raise ValueError("Eligibility_Check requires query")

        elif rt == "Booking_or_Scheduling":
            if not self.category or self.preferred_slot is None:
                raise ValueError("Booking_or_Scheduling requires category and preferred_slot")

        elif rt == "Urgent_Service_Request":
            required = [
                self.category,
                self.current_location,
                self.severity,
                self.time_sensitivity,
                self.crowd_level,
            ]
            if any(x is None for x in required):
                raise ValueError("Urgent_Service_Request missing required fields")

        elif rt == "Full_Service_Request":
            required = [
                self.category,
                self.current_location,
                self.preferred_slot,
                self.severity,
                self.time_sensitivity,
                self.crowd_level,
            ]
            if any(x is None for x in required):
                raise ValueError("Full_Service_Request missing required fields")
