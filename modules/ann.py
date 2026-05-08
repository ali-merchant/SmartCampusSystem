from models.response import PRIORITY_OUTPUT_TEMPLATE


FEATURE_ORDER = [
    "Role",
    "RequestType",
    "Severity",
    "TimeSensitivity",
    "CrowdLevel",
    "Distance",
    "Eligibility",
]

ROLE_ENCODING = {
    "student": 0,
    "instructor": 1,
    "staff": 2,
}

REQUEST_TYPE_ENCODING = {
    "AI_Lab_Support": 0,
    "Viva_Scheduling": 1,
    "Access_Request": 2,
    "Maintenance": 3,
    "Emergency_Help": 4,
}


def build_feature_vector(request, ann_inputs: dict) -> list:
    # Encode request fields into a numeric feature vector for ANN use.
    # Keeps the feature order aligned with the project specification.
    role_value = ROLE_ENCODING.get(request.role, 0)
    request_type_value = REQUEST_TYPE_ENCODING.get(request.category, 0)
    severity = ann_inputs.get("severity", 0) or 0
    time_sensitivity = ann_inputs.get("time_sensitivity", 0) or 0
    crowd_level = ann_inputs.get("crowd_level", 0) or 0
    distance = ann_inputs.get("distance", 0) or 0
    eligibility = 1 if ann_inputs.get("eligibility", True) else 0

    return [
        role_value,
        request_type_value,
        severity,
        time_sensitivity,
        crowd_level,
        distance,
        eligibility,
    ]


def predict_priority(request, ann_inputs: dict) -> dict:
    # Predict binary and multiclass priority using a simple scoring heuristic.
    # Returns a standard priority output object.
    features = build_feature_vector(request, ann_inputs)
    severity = features[2]
    time_sensitivity = features[3]
    crowd_level = features[4]

    score = (severity + time_sensitivity + crowd_level) / 3.0

    if score >= 9:
        final_priority = "urgent"
    elif score >= 7:
        final_priority = "high"
    elif score >= 4:
        final_priority = "normal"
    else:
        final_priority = "low"

    binary_priority = "urgent" if score >= 7 else "not_urgent"
    confidence = min(0.99, max(0.5, score / 10.0))

    output = PRIORITY_OUTPUT_TEMPLATE.copy()
    output["binary_priority"] = binary_priority
    output["final_priority"] = final_priority
    output["confidence"] = round(confidence, 2)
    return output
