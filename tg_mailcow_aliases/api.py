import os
import requests


DEFAULT_DOMAIN = os.getenv("DEFAULT_DOMAIN", "error")
DEFAULT_EMAIL = os.getenv("DEFAULT_EMAIL", "error")
SERVER_URL = os.getenv("SERVER_URL", "error")
X_API_KEY = os.getenv("X_API_KEY", "error")

GET_ALIAS = "/api/v1/get/alias"
ADD_ALIAS = "/api/v1/add/alias"
DELETE_ALIAS = "/api/v1/delete/alias"
ALL_ALIAS = "/all"
HEADER = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": X_API_KEY,
}


def add_alias(new_alias, goto=DEFAULT_EMAIL, domain=DEFAULT_DOMAIN, active=1):
    """add new alias for DEFAULT_EMAIL
    add new alias for goto address
    Args:
            new_alias: left part of new alias
            goto: goto email address
            domain: right part of new alias

    Returns:
            Returns - tuple (status_code, request data)
    """
    add_alias_json = {
        "active": active,
        "address": f"{new_alias}@{domain}",
        "goto": goto,
    }
    re = requests.post(
        f"{SERVER_URL}{ADD_ALIAS}", json=add_alias_json, headers=HEADER
    )
    return (re.status_code, re.json())


def delete_alias(alias_id):
    """delete alias by id

    Args:
            alias_id: alias id

    Returns:
            Returns - tuple (status_code, request data)

    """
    re = requests.post(
        f"{SERVER_URL}{DELETE_ALIAS}", json=[alias_id], headers=HEADER
    )
    return (re.status_code, re.json())
