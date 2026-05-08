from models.request import Request
from models.response import ROUTER_OUTPUT_TEMPLATE


def route_request(request: Request, route_requested: bool = False) -> dict:
    # Decide the module pipeline for a request based on request_type.
    # Returns the router control object for downstream processing.
    output = ROUTER_OUTPUT_TEMPLATE.copy()
    output["request_id"] = request.request_id

    request_type = request.request_type

    if request_type == "Navigation_Only":
        output["selected_pipeline"] = ["Search"]
        output["needs_search"] = True

    elif request_type == "Eligibility_Check":
        output["selected_pipeline"] = ["Logic_KB"]
        output["needs_logic"] = True

    elif request_type == "Booking_or_Scheduling":
        output["selected_pipeline"] = ["Logic_KB", "CSP"]
        output["needs_logic"] = True
        output["needs_csp"] = True
        output["needs_search"] = bool(request.destination) or route_requested
        if output["needs_search"]:
            output["selected_pipeline"].append("Search")

    elif request_type == "Urgent_Service_Request":
        output["selected_pipeline"] = ["ANN", "Logic_KB", "CSP"]
        output["needs_ann"] = True
        output["needs_logic"] = True
        output["needs_csp"] = True
        output["needs_search"] = bool(request.destination) or route_requested
        if output["needs_search"]:
            output["selected_pipeline"].append("Search")

    elif request_type == "Full_Service_Request":
        output["selected_pipeline"] = ["ANN", "Logic_KB", "CSP", "Search"]
        output["needs_ann"] = True
        output["needs_logic"] = True
        output["needs_csp"] = True
        output["needs_search"] = True

    else:
        raise ValueError("Unsupported request_type")

    return output
