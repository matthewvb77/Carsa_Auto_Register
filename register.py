from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime

# Global Variables
days = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekends = ["Saturday", "Sunday"]
weekday_times = ["6:00 AM - 7:45 AM", "8:00 AM - 9:45 AM", "10:00 AM - 11:45 AM", "12:00 PM - 1:45 PM",
                 "2:00 PM - 3:45 PM", "4:00 PM - 5:45 PM", "6:00 PM - 7:45 PM", "8:00 PM - 9:45 PM",
                 "10:00 PM - 11:00 PM"]
weekend_times = ["7:00 AM - 8:45 AM", "9:00 AM - 10:45 AM", "11:00 AM - 12:45 PM", "1:00 PM - 2:45 AM",
                 "3:00 PM - 4:45 PM", "5:00 PM - 6:45 PM", "7:00 PM - 8:45 PM"]


def register(username, password, day_r, time_r, headless):
    if headless:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome()

    driver.get("https://activeliving.uvic.ca/Program/GetProducts?classification=f3a12a34-c536-4b62-b9dc-c1f09c41e8b0")

    # accept cookie popup
    driver.find_element(By.ID, 'gdpr-cookie-accept').click()

    # click 'login' button
    driver.find_element(By.ID, 'loginLink').click()

    # click 'netlink id' option
    netlink_btn_xpath = '//div/button[@title="Sign In for UVic Students, Faculty & Staff"]'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, netlink_btn_xpath)))
    driver.find_element(By.XPATH, netlink_btn_xpath).click()

    # enter credentials and log in
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'form-submit').click()

    # click which day
    driver.find_element(By.XPATH, f'//div[@id="list-group"]/a[{days[day_r]}]').click()

    # click register (if button exists)
    try:
        driver.find_element(By.XPATH,
                            f'//section[@class="list-group"]/div/div/div[@data-instance-times="{time_r}"]/div/div/button').click()
    except:
        print("Section has no spots available")
        driver.close()
        exit(0)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="TopBarRight"]/div[2]/a/span[2]')))

    # go to cart
    driver.get("https://activeliving.uvic.ca/Cart")

    # click checkout
    driver.find_element(By.ID, 'checkoutButton').click()

    # confirm checkout
    driver.find_element(By.ID, '//*[@id="CheckoutModal"]/div/div/div/button[text()="Checkout"]').click()

    driver.close()


def main():

    # Input Details START
    netlinkid = "example_netlink"
    password = "example-password"
    day_r = "Friday"
    date_r = "dd-mm-yyyy"
    time_r = "10:00 PM - 11:00 PM"
    # Switch to False to see the bot work
    headless = True
    # Input Details END

    # User Input Error Handling
    if day_r not in days.keys():
        print("Invalid day!")
        exit(0)
    if (day_r in weekdays and time_r not in weekday_times) or (day_r in weekends and time_r not in weekend_times):
        print("Invalid time!")
        exit(0)

    # add 0 padding to time
    if time_r[2] == ":":
        time_r = "0" + time_r

    # format datetime
    datetime_str = date_r + " " + time_r[0:8]

    # convert to datetime object
    slot_time = datetime.strptime(datetime_str, "%d-%m-%Y %I:%M %p")

    # find time to register (3 days before slot)
    register_time = slot_time.timedelta(hours=72)

    # wait until reset with 30 second buffer
    seconds_to_wait = (register_time - datetime.now()).total_seconds()
    if seconds_to_wait > 0:
        time.sleep(seconds_to_wait + 30)
    else:
        # slots are already open!
        pass

    # register!
    register(netlinkid, password, day_r, time_r, headless)


if __name__ == '__main__':
    main()
