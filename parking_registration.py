from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
from selenium.webdriver.chrome.service import Service
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--verbose")
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox") # Bypass OS security model
# chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
chrome_options.add_argument("--window-size=1440 x 900")

inputs = {}
# List of input data corresponding to each field's name attribute
with open('config.json', 'r') as config_file:
    inputs = json.load(config_file)

# Add sensitive data from environment variables
inputs['token'] = os.getenv('TOKEN')
inputs['email'] = os.getenv('EMAIL')
inputs['tel'] = os.getenv('TEL')

service = Service('/usr/bin/chromedriver', log_path='chromedriver.log')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set up WebDriver
# driver = webdriver.Chrome(options=chrome_options)
try:
    #Navigate to the page and interact as needed
    #driver.get("https://boulevard.parkingattendant.com/1hchtwjdt95fd4zyxvqmdmeve0/permits/temporary/new?policy=k10g06m5yd15n7bbep5x0qncmm")
    driver.get("https://boulevard.parkingattendant.com/boulevard/services")

    # Click a link by its text
    logging.info(driver.page_source)
    # Use WebDriverWait to wait until the link is visible
    link = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'register vehicle'))
    )
    logging.info(driver.page_source)
    link.click()
    # logging.info(driver.page_source)

    # Fill in each input field
    for field_name, input_value in inputs.items():
        if (field_name != "duration"): 
            # Wait up to 10 seconds unitl the element is visible and interactable
            wait = WebDriverWait(driver, 10)
            field_element = wait.until(EC.element_to_be_clickable((By.NAME, field_name)))

            # field_element = driver.find_element(By.NAME, field_name)
            field_element.send_keys(input_value)
    
    
    logging.info(driver.page_source)
    # Locate the <select> element by its name attribute and interact with it
    select_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
        By.XPATH, "//fieldset[@class='valid duration']//label[@class='duration value']//select[@class='duration']")))
    
    logging.info("FAIL TO GET SELECT ELEMENT")

    # Check if the element is indeed a 'select' tag
    if select_element.tag_name != 'select':
        raise UnexpectedTagNameException(f"Expected 'select' tag, got '{select_element.tag_name}' tag.")
    
    # Perform selection
    select = Select(select_element)
    select.select_by_visible_text(inputs["duration"])

    # Find and click the submit button
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//fieldset[@class='control']//button[@type='submit']")))
    submit_button.click()

    response_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//time[@class='relative']")))
    logging.info("Guest parking valid until: " + response_message.text)
except Exception as e:
    logging.info("An error occurred: %s", str(e))
finally:
    driver.quit()