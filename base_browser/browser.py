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
        self.cookie_contexts = Contexts(self)
        self.set_options(proxy=proxy, **kwargs)
        self.start()
        self.wait_for_proxy()
        if config.DEFAULT_PAGE is not None:
            self.browser.get(config.DEFAULT_PAGE)

        self.register_handlers()
        self.start_handlers()

    def register_handlers(self):
        self.handlers = [threading.Thread(target=self.cookie_change_handler)]
    
    def start_handlers(self):
        for handler in self.handlers:
            handler.start()

    def stop_handlers(self):
        for handler in self.handlers:
            handler.join()

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
        self.stop_handlers()
        self.browser.close()
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def set_options(self, **kwargs) -> None:
        pass

    def cookie_change_handler(self):
        while self.running:
            new_cookies = WebDriverWait(self.browser, timeout=3600).until(CookieChanged(self.browser.get_cookies()))
            if new_cookies:
                self.cookie_contexts.update_cookies(new_cookies)

    def get_all_cookies(self):
        return self.cookie_contexts.get_cookies()
    
    def roll_cookies(self, cookies):
        print("Rolling cookies")
        self.browser.delete_all_cookies()
        for c in cookies:
            self.browser.add_cookie(c)
    

class CookieChanged(object):
    def __init__(self, cookies):
        self.cookies = cookies

    def __call__(self, driver):
        new_cookies = driver.get_cookies()
        for c in new_cookies:
            if c not in self.cookies:
                return new_cookies
        return False