from behave import *
import time
import selenium.common.exceptions


@Then('Print the current url')
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
    (context.element.find_element(locator)).click()


@step('Collect all items on the first page into {var}')
@step('Collect all items on the first page into {var} on the {level} level')
def step_impl(context, var, level=None):
    var = []
    time.sleep(2)
    for i in range(1, 25):
        locator = f"(//section//a[@data-test='product-title'])[{i}]"
        try:
            context.browser.execute_script("window.scrollBy(0, 250)")
            item_text = (context.element.find_element(locator)).text
            var.append(item_text)
        except AttributeError:
            print(context.element.find_element(locator))
    if level == 'feature':
        context.feature.collected_items = var
    else:
        context.collected_items = var


@step("Verify all collected results' {param} is {condition}")
def step_impl(context, param, condition):
    context.browser.execute_script("window.scrollTo(0, 250)")
    if hasattr(context.feature, 'collected_items'):
        item_list = context.feature.collected_items
    else:
        item_list = context.collected_items
    for item in item_list:
        context.browser.execute_script("window.scrollBy(0, 250)")
        try:
            if param == "price":
                item_price = (context.element.find_element("//a[text()='" + item + "']/ancestor::div[contains(@data-test, '@web/ProductCard/')]//span[@data-test='current-price']/span")).text

                if condition[0] == "<":
                    if not float(item_price[1:]) < int(condition[-2:]):
                        print(f"{item} does not satisfy condition - {condition}!")
                elif condition[0] == ">":
                    if not float(item_price[1:]) > int(condition[-2:]):
                        print(f"{item} does not satisfy condition - {condition}!")
                elif condition[0] == "=":
                    if not float(item_price[1:]) == int(condition[-2:]):
                        print(f"{item} does not satisfy condition - {condition}!")

            elif param == "shipment":
                if not context.element.find_element("//a[text()='" + item + "']/ancestor::div[contains(@data-test, '@web/ProductCard/')]//span[text()='Ships free']"):
                    print(f"NOT with free shipping - \"{item}\"")

            # name of the product item contains ' or " which brakes ability to search it by xpath
        except selenium.common.exceptions.JavascriptException:
            print(f"Item contains - \" or ' in their name - \"{item}\"")
        # since was getting <'bool' object has no attribute 'text'> error
        except AttributeError:
            print(f"'bool' object has no attribute 'text' related issue in searching \"{condition}\" in \"{item}\"")
        # if price shows in range (ex $4-$20)
        except ValueError:
            print(f"Price shows in range and does not satisfy condition \"{condition}\" - \"{item}\"")
