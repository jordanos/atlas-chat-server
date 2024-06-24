def verify_user_api_response(user: dict) -> bool:
    """checks user dict keys presence and value types

    Args:
        user (dict): user returned from api
    """
    allowed_key_vals_check = {
        "username": str,
        "first_name": str,
        "last_name": str,
        "is_active": bool,
        "is_online": bool,
    }
    disallowed_key_vals_check = {"password": [str]}
    # check if all allowed key vals are present
    for k, v in allowed_key_vals_check.items():
        assert isinstance(user[k], v)
    # check if all disallowed key vals are not present
    for k in disallowed_key_vals_check.keys():
        assert user.get(k, None) is None
    return True
