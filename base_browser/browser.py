from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.options import BaseOptions
import logging
from exceptions import errors, hints
import config
from abc import ABC, abstractmethod


class BaseBrowser(ABC):

    def __init__(self, proxy: str = "127.0.0.1:8080"):
        self.browser = None
        self.proxy = proxy
        self.set_options(proxy=proxy)
        self.start()
        self.wait_for_proxy()
        if config.DEFAULT_PAGE is not None:
            self.browser.get(config.DEFAULT_PAGE)

    def wait_for_proxy(self):
        if self.proxy is None:
            return
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
    
    def stop(self) -> None:
        self.browser.close()
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def set_options(self, **kwargs) -> None:
        pass
