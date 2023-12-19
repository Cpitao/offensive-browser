from selenium.common.exceptions import WebDriverException
import logging
from exceptions import errors, hints
import config


class BaseBrowser:

    def __init__(self):
        self.browser = None

    def wait_for_proxy(self):
        while not self.verify_proxy():
            input("Press Enter to try again... ")

    def verify_proxy(self):
        try:
            self.browser.get(config.DEFAULT_PAGE)
        except WebDriverException as e:
            logging.error("%s", e.msg)
            if errors.is_error(e, errors.PROXY_FAIL):
                print("hint: %s" % hints.PROXY_FAIL_HINT)
            return False
        return True
    
    def __getattr__(self, name):
        return self.browser.__getattribute__(name)