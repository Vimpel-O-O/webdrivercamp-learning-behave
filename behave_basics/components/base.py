from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions


class Base:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        element.click()

    def find_element_inlist(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element
        except selenium.common.exceptions.TimeoutException:
            return False

    def find_elements_inlist(self, locator):
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, locator)))
            return elements
        except selenium.common.exceptions.TimeoutException:
            return False

    def insert_text(self, text, locator):
        element = self.find_element_inlist(locator)
        element.send_keys(text)
        element.send_keys(Keys.RETURN)
