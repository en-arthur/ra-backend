def error_response(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}
