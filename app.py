from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import traceback
import time
from datetime import datetime, timedelta
import calendar
import threading
import json

url = "https://theracentre.my.site.com/#/app/program/calendar/DIV-002/?cat1=Badminton%20Court%20Bookings"

with open("credentials.json", "r") as f:
    creds = json.load(f)

USERNAME = creds["username"]
PASSWORD = creds["password"]

PROGRAM_START = time.time()
print(f"[PROGRAM START] {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
browser1 = webdriver.Chrome()
browser2 = webdriver.Chrome()
browser1.get(url)
browser2.get(url)

class Days():
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY  = 4
    SATURDAY = 5
    SUNDAY = 6

def weekView(browser):
    try:
        # time.sleep(10)
        week_btn = WebDriverWait(browser, 360).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Week']"))
        )
        week_btn.click()
        print("Clicked the week button.")
    except Exception as e:
        print("Could not find or click the week button.")

def nextWeek(browser):  
    try: 
        next_link = WebDriverWait(browser, 360).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-next-button"))
        )
        next_link.click()
        print("Switched to next week.")
    except Exception as e:
        print("Could not switch to next week.")

def selectCourt(browser): 
    if not hasattr(browser, "start_attempt_time"):
        browser.start_attempt_time = time.time()    

    today = datetime.today()
    days_until_sunday = (Days.SUNDAY - today.weekday()) % 7
    next_week = today + timedelta(days=days_until_sunday or 7)

    day_number = next_week.day
    week_day = calendar.day_name[next_week.weekday()]
    month = next_week.strftime("%b")

    date = f"{week_day}  {month} {day_number}"
    
    court1 = f"//a[contains(@title, '*Badminton Court 6 - {date} - 2:00 PM')]"
    court2 = f"//a[contains(@title, '*Badminton Court 6 - {date} - 3:00 PM')]"
    print(f"Looking for court on {date}")
    try:
        if (browser is browser1) :
            court_link = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, court1))
            )
            court_link.click()

            click_time = time.time()
            total_time = click_time - browser.start_attempt_time
            program_elapsed = click_time - PROGRAM_START

            print(f"Clicked link at {time.strftime('%H:%M:%S')}")
            print("Selected first court.")
            print(f"CLICKED at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            print(f"Time searching: {total_time:.3f} seconds")
            print(f"Time since program started: {program_elapsed:.3f} seconds")
            return True
        else:
            court_link = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, court2))
            )
            court_link.click()
            
            click_time = time.time()
            total_time = click_time - browser.start_attempt_time
            program_elapsed = click_time - PROGRAM_START

            print("Selected second court.")
            print(f"CLICKED at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            print(f"Time searching: {total_time:.3f} seconds")
            print(f"Time since program started: {program_elapsed:.3f} seconds")
            return True
    except Exception as e:
        print(f"Could not find or select court, refreshing the page. Current Time: {time.strftime('%H:%M:%S')}")
        # browser.refresh()
        return False

def waitForCourt(browser):
    while True:
        weekView(browser)
        nextWeek(browser)
        time.sleep(1)
        if selectCourt(browser):
            break

def loginToRegister(browser):
    try:
        login_btn = WebDriverWait(browser, 30).until(
            lambda d: next(
                (btn for btn in d.find_elements(By.XPATH, "//a[contains(@class, 'btn-info') and .//span[text()='Register']]")
                if btn.is_displayed() and 'ng-hide' not in btn.get_attribute('class')),
                None
            )
        )
        
        browser.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(1) 

        try:
            login_btn.click()
            print("Clicked login button.")
        except Exception:
            print("Selenium click() failed, trying JS click")
            browser.execute_script("arguments[0].click();", login_btn)
            print("Clicked login button.")

    except Exception as e:
        print("Could not find or click the login button.")

def clickLogin(browser):
    try:
        login_iframe = WebDriverWait(browser, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class, 'loginFrame')]"))
        )
        print("Switched into login iframe.")

        username_input = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='j_id0:j_id5:loginComponent:loginForm:username']"))
        )
        username_input.clear()
        username_input.send_keys(USERNAME)
        print("Entered username.")

        password_input = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='j_id0:j_id5:loginComponent:loginForm:password']"))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("Entered password.")

        submit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        submit_btn.click()
        print("Login submitted successfully.")

    except Exception as e:
        print("Login form not found or failed to submit.")
        traceback.print_exc()
    finally:
        browser.switch_to.default_content()
        print("Back to main document.")

def chooseIndividual(browser):
    try:
        select_button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Select']]"))
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", select_button)

        time.sleep(1)
        select_button.click()
        print("Clicked select button")
    except Exception as e:
        print("Could not click the select button.")

def addToCart(browser):
    try:
        cart_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add to Cart']"))
        )
        cart_link.click()
        print("Clicked the add to cart button.")
    except Exception as e:
        print("Could not click the add to cart button.")

def checkout(browser):
    try:
        checkout_link = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Proceed to Checkout']"))
        )
        checkout_link.click()
        print("Clicked the first checkout button.")
    except Exception as e:
        print("Could not click the first checkout button.")

    try:
        checkout_link2 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Proceed to Checkout']]"))
        )
        checkout_link2.click()
        print("Clicked the second checkout button.")
    except Exception as e:
        print("Could not click the second checkout button.")

def completeOrder(browser):
    try:
        complete_link = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Complete Order']]"))
        )
        complete_link.click()
        print("Completed Order.")
    except Exception as e:
        print("Could not click the complete order button.")

def bookCourt1(browser):
    print("Booking first court.")
    waitForCourt(browser1)
    loginToRegister(browser1)
    clickLogin(browser1)
    chooseIndividual(browser1)
    addToCart(browser1)
    checkout(browser1)
    # completeOrder(browser1)

def bookCourt2(browser):
    print("Booking second court.")
    waitForCourt(browser2)
    loginToRegister(browser2)
    clickLogin(browser2)
    chooseIndividual(browser2)
    addToCart(browser2)
    checkout(browser2)
    # completeOrder(browser2)

court1 = threading.Thread(target=bookCourt1, args=(browser1,))
court2 = threading.Thread(target=bookCourt2, args=(browser2,))
court1.start()
time.sleep(1)
court2.start()
court1.join()
court2.join()

#Keep the browser open for additional time
time.sleep(100000)
