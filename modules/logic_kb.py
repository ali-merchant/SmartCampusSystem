from typing import Optional

from models.response import LOGIC_OUTPUT_TEMPLATE


ALLOWED_ROLES_BY_CATEGORY = {
    "AI_Lab_Support": {"student", "instructor", "staff"},
    "Viva_Scheduling": {"instructor", "staff"},
    "Access_Request": {"student", "instructor", "staff"},
    "Maintenance": {"staff"},
    "Emergency_Help": {"student", "instructor", "staff"},
}


def check_eligibility(request, query: Optional[str]) -> dict:
    output = LOGIC_OUTPUT_TEMPLATE.copy()

    if request.request_type == "Eligibility_Check":
        role = request.role
        entailed = bool(query) and role in {"instructor", "staff"}
        output["entailed"] = entailed
        output["allowed"] = entailed
        if entailed:
            output["explanation"] = (
                f"{request.name} has role {role}, so the query is entailed."
            )
        else:
            output["explanation"] = (
                "No rule entails the query for this role in the current knowledge base."
            )
        return output

    category = request.category or ""
    allowed_roles = ALLOWED_ROLES_BY_CATEGORY.get(category, set())
    allowed = request.role in allowed_roles if allowed_roles else False

    output["allowed"] = allowed
    output["entailed"] = allowed
    if allowed:
        output["explanation"] = "Eligibility check passed."
    else:
        output["explanation"] = "Eligibility check failed for the selected category."
    return output
