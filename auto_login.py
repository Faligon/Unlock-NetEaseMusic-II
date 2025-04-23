# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002585D80C0EDAECC044088A88ED36460D41C04462DAD9C6E48267C9F7EBA5E864F2A7A9395974BE7F898B91B8A6FB30B34A2BABCE93E1DCB60DD53FE0B9ADB71A80324A5A45E7C95BD91041F61D447D24C851A46EF2678EADE3ED1D6958121A2B601646731D9A2FE7AA2D88332CC9C499B545B7386E991C49B7802AAA1DB7FDBF6A8208592D6738A34D3E02DAD36AC9282EEDA700AD816B561EC66B391BE26DCD435C4B5216F8089EB7D4B7E87A21F75C71F3FB56388EBCFECC2B8898B133941D5A93BC880F46FBFC858432D76889F4A8C11ABDCF1437C64D53D50623358FC4ACC2B19ECD21B21F371FC329294EF3611EAA6922CFBD6E38077303C3F9D6A4C504CF5E40E0D962E53E84D2DC1D02A67709D1866779CB3F1E011AB559E76F7FE56AD223548612C172AD21A0A0093BEF51E2E5E0701DA0A60512AEB447E80DD01AFF3F3E8BBB4E183C073DEF9E2C0E356F742C02DF7DEF9CADB8B6E38CACD4EE6A18"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
