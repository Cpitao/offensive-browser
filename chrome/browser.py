from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
from base_browser.browser import BaseBrowser
from .proxy import setup_proxy


class ChromeBrowser(BaseBrowser):

    def __init__(self, proxy: str ="127.0.0.1:8080"):
        super().__init__(proxy=proxy)
        
    def start(self) -> None:
        self.browser = webdriver.Chrome(options=self.options)

    def set_options(self, **kwargs) -> None:
        self.options = Options()

        chromium = ChromeBrowser.find_chromium()
        if chromium is None:
            if not ChromeBrowser.install_chromium():
                print("Chromium not installed. Proceeding with Chrome for Testing.")
            else:
                chromium = ChromeBrowser.find_chromium()
                self.options.binary_location = chromium

        if kwargs.get("proxy", None):
            self.options = setup_proxy(self.options, kwargs["proxy"])

        if not config.SHOW_INFOBARS:
            self.options.add_experimental_option("excludeSwitches", ['enable-automation'])

    def find_chromium():
        from shutil import which

        return which('chromium')
    
    def install_chromium() -> bool:
        prompt = input("Chrome is not installed. You can continue and use Chrome for Testing or install it. \n" \
                       "Do you want to install it now? [Y/n]")
        if prompt == "n":
            return False
        
        from os import system
        return system("sudo apt install chromium -y") == 0
        