# Dev: Ali Jafarbeglou - Automated Game Playing Bot
"""
This bot is written in Python and uses Selenium webdriver and DateTime. It automatically plays the Cookie game on the website to achieve the highest score.
• Automated gameplay
• High score achievement
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "Users/zilog/My Program/Development"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(By.XPATH, '//*[@id="cookie"]')

items = driver.find_elements(By.ID, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

while True:
    cookie.click()
    # Every 5 seconds:
    if time.time() > timeout:

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.ID, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        try:
            highest_price_affordable_upgrade = max(affordable_upgrades)
            print(highest_price_affordable_upgrade)
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
            driver.find_element(By.ID, to_purchase_id).click()
        except:
            pass

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text

        print(cookie_per_s)
        break
