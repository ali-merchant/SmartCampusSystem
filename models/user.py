from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    role: str
    choice: int # derices request

    current_location: Optional[str] = None
    destination: Optional[str] = None
    query: Optional[str] = None
    category: Optional[str] = None
    preferred_slot: Optional[int] = None
    group_id: Optional[str] = None
    severity: Optional[int] = None
    time_sensitivity: Optional[int] = None
    crowd_level: Optional[int] = None
    description_note: Optional[str] = None

    _REQUEST_TYPES = {
        1: "Navigation_Only",
        2: "Eligibility_Check",
        3: "Booking_or_Scheduling",
        4: "Urgent_Service_Request",
        5: "Full_Service_Request",
    }

    def __post_init__(self):
        # Validate required fields and determine request type from choice.
        # Ensures the user input meets baseline constraints.
        self._validate_name()
        self._validate_role()
        self._validate_choice()
        self.requestType = self._REQUEST_TYPES[self.choice]
        self._validate_conditionals()

    def _validate_name(self):
        # Validate name length to keep identifiers reasonable.
        # Rejects overly long names.
        if len(self.name) >= 30:
            raise ValueError("Name must be less than 30 characters")

    def _validate_role(self):
        # Validate role against allowed values and normalize casing.
        # Keeps roles consistent across the system.
        allowed = ["student", "instructor", "staff"]
        if self.role.lower() not in allowed:
            raise ValueError(f"Invalid role. Must be one of: {allowed}")
        self.role = self.role.lower()

    def _validate_choice(self):
        # Validate request choice selection from the available options.
        # Rejects values outside the supported range.
        if self.choice not in self._REQUEST_TYPES:
            raise ValueError("Choice must be between 1 and 5")

    def _validate_conditionals(self):
        # Validate required fields based on the derived request type.
        # Ensures each request has the necessary inputs.
        request_type = self.requestType

        if request_type == "Navigation_Only":
            if not self.current_location or not self.destination:
                raise ValueError("Navigation_Only requires current_location and destination")

        elif request_type == "Eligibility_Check":
            if not self.query:
                raise ValueError("Eligibility_Check requires query")

        elif request_type == "Booking_or_Scheduling":
            if not self.category or self.preferred_slot is None:
                raise ValueError("Booking_or_Scheduling requires category and preferred_slot")
            # optional: current_location

        elif request_type == "Urgent_Service_Request":
            required = [
                self.category, self.current_location, self.severity,
                self.time_sensitivity, self.crowd_level
            ]
            if any(x is None for x in required):
                raise ValueError("Urgent_Service_Request missing required fields")

        elif request_type == "Full_Service_Request":
            required = [
                self.category, self.current_location, self.preferred_slot,
                self.severity, self.time_sensitivity, self.crowd_level
            ]
            if any(x is None for x in required):
                raise ValueError("Full_Service_Request missing required fields")
            # optional: description_note