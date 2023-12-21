from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base_browser.browser import BaseBrowser
from .proxy import setup_proxy


class ChromeBrowser(BaseBrowser):

    def __init__(self, proxy: str ="127.0.0.1:8080"):
        super().__init__(proxy=proxy)
        
    def start(self) -> None:
        self.browser = webdriver.Chrome(options=self.options)

    def set_options(self, **kwargs) -> None:
        self.options = Options()
        if kwargs.get("proxy", None):
            self.options = setup_proxy(self.options, kwargs["proxy"])
