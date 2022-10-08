import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


os.environ['PATH'] += r"C:\Users\bolar\PycharmProjects\SeleniumDriver"
driver = webdriver.Chrome()
driver.get("https://www.sportybet.com/ng/sport/tennis")
driver.implicitly_wait(5)

# username = input("Enter your phone number here: +234 ")
# password = input("Enter password: ")
username = 7017643255
password = "leopapa123"


def clear_box(web_element):
    web_element.send_keys(Keys.CONTROL + "a")
    web_element.send_keys(Keys.BACKSPACE)


def sporty_login(phone, psd):
    input1 = driver.find_element(By.XPATH, "//input[@name='phone' and @placeholder='Mobile Number']")
    clear_box(input1)
    input1.send_keys(phone)
    time.sleep(2)
    input2 = driver.find_element(By.XPATH, "//input[@type='password' or @placeholder='Password']")
    clear_box(input2)
    input2.send_keys(psd)
    time.sleep(2)
    login_btn = driver.find_element(By.XPATH, "//button[@name='logIn' and .='Login']")
    login_btn.click()


def check_simulated(name):
    if 'simulated' in name.lower():
        return True
    else:
        return False


sporty_login(username, password)
time.sleep(10)

t_leagues = len(driver.find_elements(By.CSS_SELECTOR, "div.match-league"))
print(f"There are {t_leagues} league available.")
t_match_clicked = 0
for lg_post in range(1, t_leagues+1):
    league_name = driver.find_element(By.XPATH, f"(//div[@class='match-league'])[{lg_post}]/div[@class='league-title']/span[@class='text']").text
    # print(league_name)
    if check_simulated(league_name):
        pass
    else:
        try:
            match_per_league = len(driver.find_elements(By.XPATH, f"(//div[@class='match-league'])[{lg_post}]//div[contains(@class, 'match-row')]"))
            # print(match_per_league)
            for m_post in range(1, match_per_league+1):
                match_H = driver.find_element(By.XPATH, f"(//div[@class='match-league'])[{lg_post}]//div[contains(@class, 'match-row')][{m_post}]//div["
                                                        f"contains("
                                                        "@class, 'm-market')][1]/div[@class='m-outcome'][1]")
                match_H_oc = float(match_H.text)
                if match_H_oc < 1.12:
                    match_H.click()
                    t_match_clicked += 1
        except NoSuchElementException:
            pass
    if t_match_clicked > 3:
        break

print(f"{t_match_clicked} matches clicked.")

# ENTER BET AMOUNT
betslip = driver.find_element(By.CSS_SELECTOR, "input[placeholder='min. 10']")
clear_box(betslip)
time.sleep(5)
betslip.send_keys("10")

actions = ActionChains(driver)
wait = WebDriverWait(driver, 30)
# PLACE BET
place_bet = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.af-button")))
time.sleep(5)
actions.double_click(place_bet).perform()

try:
    driver.find_element(By.XPATH, "//span[text()='Accept Changes']")
    time.sleep(2)
except NoSuchElementException:
    pass

confirm_bet = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.af-button.af-button--primary:nth-child(2)")))
confirm_bet.click()

time.sleep(15)
time_stamp = time.strftime("%b%d")
driver.save_screenshot(fr"C:\Users\bolar\Documents\Automated_Bets\Tennis{time_stamp}.png")

time.sleep(10)
driver.close()
