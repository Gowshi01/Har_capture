import pprint
from browsermobproxy import Server
from selenium import webdriver
import time

class ProxyManager:

    __BMP = "D:/HAR/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": True, "captureContent": True})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server

def enable_preserve_log(driver):
    logging_prefs = {
        'performance': 'ALL',
        'browser': 'ALL',
    }
    driver.capabilities['goog:loggingPrefs'] = logging_prefs

if __name__ == "__main__":
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("westernunion.com")
    print(client.proxy)

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-popup-blocking')

    # Create Chrome WebDriver without using 'with' statement
    driver = webdriver.Chrome(options=options)

    try:
        # Enable "Preserve log"
        enable_preserve_log(driver)

        # Introduce a 15-second delay before navigating to the URL
        time.sleep(15)
        driver.get("https://www.westernunion.com/au/en/send-money-to-india-v2.html?src=PaidSearch___&utm_content=%7Cdm_pcrid__mt__kw_&eng_ids=GG_20729514120___&gclsrc=aw.ds&")

        # Additional actions or processing if needed
        time.sleep(45)
        # Get all entries from the HAR log
        har_entries = client.har['log']['entries']


        # Print or save the details of each entry
        for entry in har_entries:
            pprint.pprint(entry)
            # You can save the details to a file or process them further as needed

    finally:
        # The browser window will remain open due to the experimental option
        # Stop BrowserMob Proxy server
        server.stop()
        driver.quit()
