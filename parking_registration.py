from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox") # Bypass OS security model
# chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
chrome_options.add_argument("--window-size=1440,900") # Setup window size
# chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

inputs = {}
# List of input data corresponding to each field's name attribute
with open('config.json', 'r') as config_file:
    inputs = json.load(config_file)

# Update inputs dictionary with environment variables if empty or missing
inputs['token'] = inputs.get('token') or os.getenv('TOKEN') or os.getenv('token')
inputs['email'] = inputs.get('email') or os.getenv('EMAIL') or os.getenv('email')
inputs['tel'] = inputs.get('tel') or os.getenv('TEL') or os.getenv('tel')

# Set up WebDriver
driver = webdriver.Chrome(options=chrome_options)
try:
    #Navigate to the page and interact as needed
    driver.get("https://boulevard.parkingattendant.com/1hchtwjdt95fd4zyxvqmdmeve0/permits/temporary/new?policy=k10g06m5yd15n7bbep5x0qncmm")

    # Fill in each input field
    for field_name, input_value in inputs.items():
        if (field_name != "duration"): 
            # Wait up to 10 seconds unitl the element is visible and interactable
            wait = WebDriverWait(driver, 300)
            field_element = wait.until(EC.element_to_be_clickable((By.NAME, field_name)))

            # field_element = driver.find_element(By.NAME, field_name)
            field_element.send_keys(input_value)

    # XPath for select and radio buttons
    select_xpath = "//fieldset[@class='valid duration']//select[@class='duration']"
    radio_xpath = f"//fieldset[@class='valid duration']//label[span[text()='{inputs['duration']}']]//input[@type='radio'][@name='duration']"
    # Wait for <select> or <input type="radio"> to be located
    element = WebDriverWait(driver, 3600, poll_frequency=2).until(
        EC.presence_of_element_located((By.XPATH, f"{select_xpath} | {radio_xpath}")))

    # Perform actions based on the type of element found
    if element.tag_name == "select":
        # Perform selection
        select = Select(element)
        select.select_by_visible_text(inputs["duration"])
        logging.info("Selected value from <select>")
    elif element.tag_name == "input" and element.get_attribute("type") == "radio":
        # Click radio button
        element.click()
        logging.info("Selected value from <input>")

    # Find and click the submit button
    submit_button = WebDriverWait(driver, 600, poll_frequency=2).until(
        EC.element_to_be_clickable((By.XPATH, "//fieldset[@class='control']//button[@type='submit']")))
    submit_button.click()

    logging.info(driver.page_source)

    response_message = WebDriverWait(driver, 600).until(EC.visibility_of_element_located((By.XPATH, "//time[@class='relative']")))
    logging.info("Guest parking valid until: " + response_message.text)
except TimeoutException:
    print("The element did not appear within the time limit.")
except Exception as e:
    logging.info("An error occurred: %s", str(e))
    logging.info(driver.page_source)
finally:
    driver.quit()


'''
Notes:
EC.presence_of_all_elements_located: 
    This returns a list of all elements that match the given locator. 
    It's used when you want to wait until any number of elements (at least one) are present on the DOM and visible. 
    It's helpful when you're dealing with multiple elements of the same type and need to interact with all of them 
    or verify their presence.
EC.presence_of_element_located: 
    Similar to the above but returns only the first WebElement that matches the given locator. 
    This is used when you are interested in a specific element and it suffices to find just one.
EC.element_to_be_clickable: 
    This returns a single WebElement that is both visible and enabled, making it ready for user interaction like clicking.
    This is used when you need to interact with a specific element, ensuring it is ready for such interactions.
'''