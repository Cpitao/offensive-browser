from selenium.common.exceptions import WebDriverException


PROXY_FAIL = "unknown error: net::ERR_PROXY_CONNECTION_FAILED"


def is_error(e1: WebDriverException, e2: str):
    return e1.msg.startswith(e2)