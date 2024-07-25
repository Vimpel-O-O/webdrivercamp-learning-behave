from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from components.base import Base


def before_all(context):
    PATH = "/Users/sk/Documents/Code/webdrivercamp-learning-selenium/chromedriver"
    service = Service(PATH)
    options = Options()

    context.browser = webdriver.Chrome(service=service, options=options)
    context.element = Base(context.browser)

    # make no_background off by default
    context.no_background = False


def before_tag(context, tag):
    if tag == "no_background":
        context.no_background = True


def after_scenario(context):
    context.no_background = False

# def after_all(context):
    # context.browser.quit()
