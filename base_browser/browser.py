from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from abc import ABC, abstractmethod
import threading

from exceptions import errors, hints
import config
from .cookies.contexts import Contexts


class BaseBrowser(ABC):

    def __init__(self, proxy: str = "127.0.0.1:8080", **kwargs):
        self.__previous_url = config.DEFAULT_PAGE
        self.running = True
        self.browser = None
        self.proxy = proxy
        self.cookie_contexts = Contexts()
        self.set_options(proxy=proxy, **kwargs)
        self.start()
        self.wait_for_proxy()
        if config.DEFAULT_PAGE is not None:
            self.browser.get(config.DEFAULT_PAGE)

        self.handler_thread = threading.Thread(target=self.wait_for_condition)
        self.handler_thread.start()

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
        self.running = False
        self.handler_thread.join()
        self.browser.close()
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def set_options(self, **kwargs) -> None:
        pass

    def wait_for_condition(self):
        while self.running:
            WebDriverWait(self.browser, timeout=3600).until(EC.url_changes(self.__previous_url))
            self.handle_event(self.browser)

    def handle_event(self, browser) -> None:
        self.__previous_url = browser.current_url
        print(browser.current_url)
        # TODO save cookies before changing the URL