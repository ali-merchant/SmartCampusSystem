_REQUEST_COUNTER = 200


def generate_request_id() -> str:
    # Generate a simple sequential request id.
    # Keeps identifiers readable for demo use.
    global _REQUEST_COUNTER
    _REQUEST_COUNTER += 1
    return f"REQ{_REQUEST_COUNTER}"
