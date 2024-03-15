import time
import pprint
from browsermobproxy import Server
from selenium import webdriver

class ProxyManager:

    __BMP = "E:/Harry/Project/har/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": True})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server
if "__main__" == __name__:
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("matchesfashion.com")
    print(client.proxy)
    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.matchesfashion.com/")    
    time.sleep(15)

    har_data1 = client.har
    pprint.pprint(client.har)
    with open("har_data1.txt", "w") as file:
            file.write(str(har_data1))
    server.stop()