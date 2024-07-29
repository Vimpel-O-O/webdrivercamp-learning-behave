from behave import *
import time
from  selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.common.by import By


@step('Print the current url')
def step_impl(context):
    print(f"Current url - {context.browser.current_url}")


@step('Navigate to {url}')
def step_impl(context, url):
    if context.no_background:
        return
    context.browser.get(url)

    context.execute_steps('''
            Then Print the current url
        ''')


@step('Search for {search_item}')
def step_impl(context, search_item):
    # paste search item into search bar
    context.element.insert_text(search_item, "//input[@type='search']")


@step('Wait {num} sec')
def step_impl(context, num):
    context.browser.execute_script("window.scrollBy(0, 250)")
    time.sleep(int(num))


@step("Verify header of the page contains {search_item}")
def step_impl(context, search_item):
    locator = f"//h1[text()='Gift Ideas'] | //h2/following-sibling::span[contains(text(), '{search_item}')]"
    if not context.element.find_element(locator):
        raise "Element not found!"


@step('Select {option} in {section} section')
def step_impl(context, option, section):
    locator = f"//span[text()='{section}']//ancestor::div/following-sibling::ul//span[text()='{option}']"
    (context.element.find_element_inlist(locator)).click()


@step('Collect all items on the first page into {var}')
@step('Collect all items on the first page into {var} on the {level} level')
def step_impl(context, var, level=None):
    var = []
    time.sleep(1)

    # scrolling the whole page to preload all elements
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += 8
        context.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = context.browser.execute_script("return document.body.scrollHeight")

    # grabbing all card items in one list and getting details of each
    card_xpath = '//div[@data-test="@web/site-top-of-funnel/ProductCardWrapper"]'
    items = context.element.find_elements_inlist(card_xpath)
    data = []
    for item in items:
        title = item.find_element(By.XPATH, './/a[@data-test="product-title"]').text
        price = item.find_element(By.XPATH, './/span[@data-test="current-price"]').text
        try:
            shipment = item.find_element(By.XPATH, './/span[text()="Ships free"]')
        except NoSuchElementException:
            shipment = None
        data.append((title, price, shipment))

    if level == 'feature':
        context.feature.collected_items = data
    else:
        context.collected_items = data


@step("Verify all collected results' {param} is {condition}")
def step_impl(context, param, condition):
    if hasattr(context.feature, 'collected_items'):
        data = context.feature.collected_items
    else:
        data = context.collected_items

    for title, price, shipment in data:
        try:
            if param == "price":
                if condition[0] == "<":
                    if not float(price[1:]) < int(condition[-3:]):
                        print(f"{title} wiht {price} does not satisfy condition - {condition}!")
                elif condition[0] == ">":
                    if not float(price[1:]) > int(condition[-3:]):
                        print(f"{title} with {price} does not satisfy condition - {condition}!")
                elif condition[0] == "=":
                    if not float(price[1:]) == int(condition[-3:]):
                        print(f"{title} with {price} does not satisfy condition - {condition}!")

            elif param == "shipment":
                if shipment is None:
                    print(f"NOT with free shipping - \"{title}\"")

        # if price shows in range (ex $4-$20)
        except ValueError:
            if str(price):
                print(f"See price in cart for - {title}")
            else:
                try:
                    biggest_cost = float(price[-5:])
                except ValueError:
                    biggest_cost = float(price[-2:])

                if condition[0] == "<":
                    if not biggest_cost < int(condition[-3:]):
                        print(f"{title} with {biggest_cost} biggest price does not satisfy condition - {condition}!")
                elif condition[0] == ">":
                    if not biggest_cost > int(condition[-3:]):
                        print(f"{title} with {biggest_cost} biggest price does not satisfy condition - {condition}!")
                elif condition[0] == "=":
                    if not biggest_cost == int(condition[-3:]):
                        print(f"{title} with {biggest_cost} biggest price does not satisfy condition - {condition}!")
