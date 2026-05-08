from typing import Optional, Tuple

from models.response import build_final_response
from modules.ann import predict_priority
from modules.csp import assign_slot
from modules.logic_kb import check_eligibility
from modules.search_module import find_route
from preprocessing import preprocess_request
from response_generator import compose_response
from router import route_request
from utils import generate_request_id


def process_raw_request(raw: dict) -> Tuple[dict, Optional[dict]]:
    # Normalize and validate raw input, returning a final response.
    # Wrap preprocessing errors into a standard rejection response.
    try:
        request, module_inputs = preprocess_request(raw)
    except ValueError as exc:
        request_id = raw.get("request_id") or generate_request_id()
        response = build_final_response(
            request_id=request_id,
            decision="rejected",
            eligibility={"allowed": False, "explanation": str(exc)},
            message=f"Your request has been rejected because {exc}.",
        )
        return response, None
    except Exception as exc:
        request_id = raw.get("request_id") or generate_request_id()
        response = build_final_response(
            request_id=request_id,
            decision="rejected",
            eligibility={"allowed": False, "explanation": str(exc)},
            message=f"Your request has been rejected because {exc}.",
        )
        return response, None

    return process_request(request, module_inputs)


def process_request(request, module_inputs: dict) -> Tuple[dict, dict]:
    # Execute the routed module pipeline for a validated request.
    # Build a final response from the collected module outputs.
    router_output = route_request(request, module_inputs.get("route_requested", False))

    ann_output = None
    logic_output = None
    csp_output = None
    search_output = None
    rejection_reason = ""

    if router_output.get("needs_ann"):
        try:
            ann_output = predict_priority(request, module_inputs.get("ann_features", {}))
        except Exception as exc:
            rejection_reason = f"priority module error: {exc}"

    if not rejection_reason and router_output.get("needs_logic"):
        try:
            logic_output = check_eligibility(request, module_inputs.get("logic_query"))
            if request.request_type != "Eligibility_Check":
                if not logic_output.get("allowed"):
                    rejection_reason = logic_output.get("explanation", "not eligible")
        except Exception as exc:
            rejection_reason = f"eligibility module error: {exc}"

    if not rejection_reason and router_output.get("needs_csp"):
        try:
            csp_output = assign_slot(request, module_inputs.get("csp", {}))
            if csp_output.get("decision") != "accepted":
                rejection_reason = csp_output.get("notes", "no feasible assignment")
        except Exception as exc:
            rejection_reason = f"scheduling module error: {exc}"

    if not rejection_reason and router_output.get("needs_search"):
        try:
            source = request.current_location
            destination = request.destination
            if not destination and csp_output:
                destination = csp_output.get("destination")
            search_output = find_route(source, destination)
            if not search_output.get("path"):
                rejection_reason = "no valid route found"
        except Exception as exc:
            rejection_reason = f"routing module error: {exc}"

    response = compose_response(
        request,
        router_output,
        ann_output=ann_output,
        logic_output=logic_output,
        csp_output=csp_output,
        search_output=search_output,
        rejection_reason=rejection_reason,
    )

    return response, router_output
