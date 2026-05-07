_REQUEST_COUNTER = 200


def generate_request_id() -> str:
    global _REQUEST_COUNTER
    _REQUEST_COUNTER += 1
    return f"REQ{_REQUEST_COUNTER}"
