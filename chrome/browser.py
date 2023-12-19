from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base_browser.browser import BaseBrowser
from .proxy import setup_proxy


class ChromeBrowser(BaseBrowser):

    def __init__(self, proxy: str ="127.0.0.1:8080"):
        super().__init__()
        self.options = Options()
        if proxy is not None:
            self.options = setup_proxy(self.options, proxy)

        self.start()
        self.wait_for_proxy()
        
    def start(self) -> None:
        self.browser = webdriver.Chrome(options=self.options)

    def stop(self) -> None:
        self.browser.close()
