from selenium import webdriver
import time
import os

# SETUP
web = 'https://twitter.com/'
path = "D:\STUDY\STUDY\PYTHON\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
driver.get(web)
driver.maximize_window()

# Using the Login button
login = driver.find_element_by_xpath('//a[@href="/login"]')
login.click()
time.sleep(4)

# Using the username textbox
username_input = driver.find_element_by_xpath('//input[@autocomplete="username"]')
username_input.send_keys(os.environ.get("TWITTER_USER"))

next_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Next"]')
next_button.click()

time.sleep(2)

# Using the password textbox
password = driver.find_element_by_xpath('//input[@autocomplete ="current-password"]')
password.send_keys(os.environ.get("TWITTER_PASSWORD"))

# Using the login button
login_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Log in"]')
login_button.click()

# Apparently it doesn't seem related with what we receive
# in Browser, but it does in Google Chrome 
# We use the sleep function to wait for the web content
