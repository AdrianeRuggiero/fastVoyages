from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    #For open the page
    driver.get("http://127.0.0.1:5000/login")

    #Waiting for the appearance of login form elements
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    #login et password
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")

    email_input.send_keys("tkapluk@gmail.com")
    password_input.send_keys("qwe")

    #Pressing the button to log in
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
        
    #Waiting for the appearance of flight search form elements.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "origin"))
    )

    #Example of filling in the fields for flight search
    origin_input = driver.find_element(By.ID, "origin")
    max_price_input = driver.find_element(By.ID, "budget")
    departure_date_input = driver.find_element(By.ID, "departure_date")

    origin_input.send_keys("MAD")
    max_price_input.send_keys("300")
    departure_date_input.send_keys("08.08.2024")

    #Pressing the button for search the flight
    search_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    search_button.click()

    #Waiting the results of the search
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "ul"))
    )

    #Print results
    search_results = driver.find_element(By.TAG_NAME, "ul")
    print(search_results.text)

finally:
    #Closed our browser after the test
    driver.quit()
