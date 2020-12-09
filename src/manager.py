import threading

from fake_useragent import UserAgent
from selenium import webdriver


class Manager:
    def __init__(self, browser, TOGGLE_BR):
        # self.threadLocal = threading.local()

        if browser == "firefox":
            useragent = UserAgent()
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", useragent.random)
            self.wd = webdriver.Firefox(profile)
        elif browser == "chrome":
            # self.wd = getattr(self.threadLocal, 'driver', None)
            chrome_options = webdriver.ChromeOptions()
            # ua = UserAgent()
            # user_agent = ua.random
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.79")
            if TOGGLE_BR == 'off':
                chrome_options.add_argument("--headless")
            self.wd = webdriver.Chrome(chrome_options=chrome_options)
            self.wd.set_window_size(1600, 1030)
            # setattr(self.threadLocal, 'driver', self.wd)
        else:
            raise ValueError("Unrecognized browser %s" % browser)

    def get_html(self, BASE_URL):
        wd = self.wd
        wd.get(BASE_URL)


    def destroy(self):
        self.wd.quit()
