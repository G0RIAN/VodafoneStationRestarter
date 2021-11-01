import hassapi as hass
import datetime
from time import sleep
import pytz

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class VodafoneStationRestarter(hass.Hass):

    driver = None
    timeout = 10
    time_step = 0.01
    password = None
    router_ip = "192.168.0.1"
    restart_time = "05:00:00"
    chrome_options = None
    tz = "Europe/Berlin"

    def initialize(self):

        self.driver = None
        self.timeout = self.args.get("timeout", self.timeout)
        self.time_step = self.args.get("time_step", self.time_step)

        self.password = self.args.get("password")
        if self.password is None:
            self.log("Password not set in app.yaml", log='error_log')
            self.terminate()
        self.router_ip = self.args.get("router_ip", self.restart_time)
        self.restart_time = self.args.get("restart_time", self.restart_time).split(":")
        if len(self.restart_time) == 2:
            self.restart_time.append("00")
        self.tz = self.config.get("time_zone", self.tz)

        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--ignore-certificate-errors")

        time = datetime.time(int(self.restart_time[0]), int(self.restart_time[1]), int(self.restart_time[2]), pytz.timezone(self.tz))

        self.log("Scheduling restart of Vodafone Station at " + str(time), log='main_log')
        self.run_daily(self.run_daily_callback, time)

    def terminate(self):
        if self.driver is not None:
            self.driver.quit()

    def run_daily_callback(self, kwargs):
        self.restart()

    def restart(self):

        self.log("Trying to restart the router", log='main_log')

        try:
            self.driver = webdriver.Chrome("chromedriver", options=self.chrome_options)

            self.driver.delete_cookie(self.router_ip)
            self.driver.get("http://" + self.router_ip)
            self.driver.find_element_by_id("Password").send_keys(self.password)
            self.driver.find_element_by_id("LoginBtn").click()
            try:
                if self.driver.find_element_by_id("InvalidMsg").is_displayed():
                    self.log("Wrong password", log='main_log')
                    return
                self.driver.find_elements_by_xpath("//input[@type='button' and @value='OK']")[0].click()
                self.driver.find_elements_by_xpath("//input[@type='button' and @value='No']")[0].click()
            except WebDriverException:
                pass
            WebDriverWait(self.driver, self.timeout).until(
                expected_conditions.presence_of_element_located((By.ID, "userModeSelect"))
            )
            self.log("Login successful", log='main_log')
            self.driver.get("http://" + self.router_ip + "/?status_restart&mid=StatusRestart")
            self.log("Restart page loaded", log='main_log')
            WebDriverWait(self.driver, self.timeout).until(
                expected_conditions.presence_of_element_located((By.ID, "PAGE_RESTART_RESTART"))
            )
            restart_button = self.driver.find_elements_by_xpath(
                "//input[@type='button' and @id='PAGE_RESTART_RESTART']"
            )
            timeout_restart = self.timeout
            while len(restart_button) == 0:
                if timeout_restart < 0:
                    raise TimeoutError("Could not find \"Restart\" button")
                sleep(self.time_step)
                timeout_restart -= self.time_step
                restart_button = self.driver.find_elements_by_xpath(
                    "//input[@type='button' and @id='PAGE_RESTART_RESTART']"
                )
                self.log(restart_button, log='main_log')
            restart_button[0].click()
            self.log("Found restart button", log='main_log')
            apply_button = self.driver.find_elements_by_xpath(
                "//input[@type='button' and @id='PAGE_RESTART_POPUP_APPLY1']"
            )
            timeout_apply = self.timeout
            while len(apply_button) == 0:
                if timeout_apply < 0:
                    raise TimeoutError("Could not find \"Apply\" button")
                sleep(self.time_step)
                timeout_apply -= self.time_step
                apply_button = self.driver.find_elements_by_xpath(
                    "//input[@type='button' and @id='PAGE_RESTART_POPUP_APPLY1']"
                )
            apply_button[0].click()
            self.log("Restart successful!", log='main_log')
        except Exception as e:
            self.log(e, log='error_log')
        finally:
            self.driver.quit()
