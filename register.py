from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

# Global Variables
days = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekends = ["Saturday", "Sunday"]
weekday_times = ["6:00 AM - 7:45 AM", "8:00 AM - 9:45 AM", "10:00 AM - 11:45 AM", "12:00 PM - 1:45 PM",
                 "2:00 PM - 3:45 PM", "4:00 PM - 5:45 PM", "6:00 PM - 7:45 PM", "8:00 PM - 9:45 PM",
                 "10:00 PM - 11:00 PM"]
weekend_times = ["7:00 AM - 8:45 AM", "9:00 AM - 10:45 AM", "11:00 AM - 12:45 PM", "1:00 PM - 2:45 AM",
                 "3:00 PM - 4:45 PM", "5:00 PM - 6:45 PM", "7:00 PM - 8:45 PM"]


def wait_and_click(driver, id_type, id_path):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((id_type, id_path)))
    driver.find_element(id_type, id_path).click()


def wait_until(instant, buffer=0):
    seconds_to_wait = (instant - datetime.now()).total_seconds()
    if seconds_to_wait > 0:
        time.sleep(seconds_to_wait + buffer)
    else:
        # instant already passed!
        pass


def main():
    # Input Details START
    netlinkid = "example_netlinkid"
    password = "example_password"
    day_r = "Thursday"              # day of time slot
    date_r = "dd-mm-yyyy"           # date of time slot
    time_r = "8:00 PM - 9:45 PM"    # time slot
    headless = True                 # Switch to False to see the bot work
    # Input Details END

    # tkinter must have root window, ours immediately dissapears
    root = Tk()
    root.withdraw()

    # User Input Error Handling
    if day_r not in days.keys():
        messagebox.showerror('Error', f'Invalid Day: {day_r}')
        exit(0)
    if (day_r in weekdays and time_r not in weekday_times) or (day_r in weekends and time_r not in weekend_times):
        messagebox.showerror('Error', f'Invalid Timeslot: {time_r}')
        exit(0)

    messagebox.showinfo('Success!', 'Inputted date and time slot check out.')
    # add 0 padding to time
    if time_r[1] == ":":
        datetime_str = date_r + " " + "0" + time_r[0:7]
    else:
        datetime_str = date_r + " " + time_r[0:8]

    # convert to datetime object
    slot_time = datetime.strptime(datetime_str, "%d-%m-%Y %I:%M %p")

    # find time to register (3 days before slot)
    register_time = slot_time - timedelta(hours=72)

    # wait until 30 sec before registering
    wait_until(register_time, buffer=-30)

    # start registering!
    if headless:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome()

    driver.get("https://activeliving.uvic.ca/Program/GetProducts?classification=f3a12a34-c536-4b62-b9dc-c1f09c41e8b0")

    # accept cookie popup
    wait_and_click(driver, By.ID, 'gdpr-cookie-accept')

    # click 'login' button
    wait_and_click(driver, By.ID, 'loginLink')

    # click 'netlink id' option
    wait_and_click(driver, By.XPATH, '//div/button[@title="Sign In for UVic Students, Faculty & Staff"]')

    # enter credentials and log in
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'username').send_keys(netlinkid)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    driver.find_element(By.ID, 'password').send_keys(password)
    wait_and_click(driver, By.ID, 'form-submit')

    # click which day
    wait_and_click(driver, By.XPATH, f'//div[@id="list-group"]/a[{days[day_r]}]')

    # wait until registration time, then refresh
    wait_until(register_time, buffer=1)
    driver.refresh()

    # click register (if button exists)
    try:
        wait_and_click(driver, By.XPATH,
                       f'//section[@class="list-group"]/div/div/div[@data-instance-times="{time_r}"]/div/div/button')

    except:
        print("No spots available")
        driver.quit()
        exit(0)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="TopBarRight"]/div[2]/a/span[2]')))

    # go to cart
    driver.get("https://activeliving.uvic.ca/Cart")

    # click checkout
    wait_and_click(driver, By.ID, 'checkoutButton')
    wait_and_click(driver, By.XPATH, '//*[@id="CheckoutModal"]/div/div/div/button[text()="Checkout"]')

    # click add to cart
    wait_and_click(driver, By.XPATH, '//form/div/button[@type="submit"]')

    wait_and_click(driver, By.ID, 'checkoutButton')
    
    # At this point the slot is reserved, wait 3 min for server request storm to calm down
    time.sleep(180)

    wait_and_click(driver, By.XPATH, '//div[@class="modal-footer"]/button[text()="Checkout"]')

    driver.quit()


if __name__ == '__main__':
    main()
