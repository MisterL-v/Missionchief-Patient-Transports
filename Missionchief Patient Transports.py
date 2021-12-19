""""
#   Missionchief patient transports
#!  MAKE SURE you DOWNLOADED the CHROME DRIVE and also installed CHROME
#   Download links:
#   -   Google Chrome:  https://www.google.de/chrome/?brand=FKPE&gclid=CjwKCAiAqIKNBhAIEiwAu_ZLDlssyRHAGslyxjokZ8S3gKrC4Gkgkf7efZ622vxaiy-eg18UJM9efxoClWQQAvD_BwE&gclsrc=aw.ds
#   -   Chromedriver:   https://chromedriver.chromium.org/downloads
"""
# -------------------------PLEASE UPDATE THIS INFORMATIONS-----------------------------------
PATH = r"C:\Users\...\chromedriver.exe"    # Path where you have downloaded the chromedriver.exe
user_email = ""
user_password = ""
# -------------------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
import time

try:
      driver =  webdriver.Chrome(PATH)
except Exception:
    print("Browser could not be opened. Make sure you changed all information and met all requirements.")

actions = ActionChains(driver)

def printAlert(mission_id, unit_id, unit_type):
    print("Alert [Mission-ID: " + mission_id + " | Vehicle ID: " + unit_id + " | Unit type: " + unit_type +"]")

mission_ids = []
missions_completed = 0

driver.get("https://www.leitstellenspiel.de/users/sign_in")

username = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")

username.send_keys(user_email)
password.send_keys(user_password)

button = driver.find_element_by_name("commit")

button.click()

if driver.current_url != "https://www.leitstellenspiel.de/" or user_email == "" or user_password == "":
    print("Login was unsuccessful. Please make sure that you have entered your login information correctly.")
else:
    print("Successfully logged in.")
    jobs = driver.find_elements_by_xpath("//*[@mission_type_id='147']")
    if jobs:
        for job in jobs:
            id = job.get_attribute('mission_id')
            class_type = driver.find_element_by_xpath("//*[@id='mission_panel_" +  id + "']").get_attribute('class')
            if "mission_panel_red" in class_type:
                mission_ids.append(id)
        
        if len(mission_ids) > 0:
            print("Required patient transports: " + str(len(mission_ids)))
        else:
            print("Currently no new patient transports are available.")

        while len(mission_ids) > 0:
            driver.get("https://www.leitstellenspiel.de/missions/" + mission_ids[0])

            use_ktw = True
            use_rtw = False
            
            try:
                car_ktw = driver.find_element_by_xpath('//*[@ktw="1" and @class="vehicle_checkbox"]')
            except Exception:
                use_ktw = False

            if  use_ktw == True:
                printAlert(mission_ids[0], car_ktw.get_attribute('value'), "patient transport vehicle")
                driver.execute_script("arguments[0].scrollIntoView();", car_ktw)
                car_ktw.click()
                button = driver.find_element_by_name("commit")
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                missions_completed += 1
            elif use_ktw == False:
                try:
                    car_rtw = driver.find_element_by_xpath('//*[@rtw="1" and @class="vehicle_checkbox"]')
                except Exception:
                    print("Currently no emergency Verhicle is available")

                printAlert(mission_ids[0], car_rtw.get_attribute('value'), "mobile intensive car unit")
                driver.execute_script("arguments[0].scrollIntoView();", car_rtw)
                car_rtw.click()
                button = driver.find_element_by_name("commit")
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                missions_completed += 1
            else:
                print("Critical Error while searching for a free patient transport car.")
            
            mission_ids.pop(0)
            driver.get("https://www.leitstellenspiel.de")

driver.quit()
print("Completed " + str(missions_completed) + " patient transports successfully.")
time.sleep(5)