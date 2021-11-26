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
import time

mission_ids = []
missions_completed = 0

try:
      driver =  webdriver.Chrome(PATH)
except Exception:
    print("Browser could not be opened. Make sure you changed all information and met all requirements.")

driver.get("https://www.leitstellenspiel.de/users/sign_in")

username = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")

username.send_keys(user_email)
password.send_keys(user_password)

driver.find_element_by_name("commit").click()

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
        
        print("Required patient transports: " + str(len(mission_ids)))

        while len(mission_ids) > 0:
            driver.get("https://www.leitstellenspiel.de/missions/" + mission_ids[0])

            use_ktw = True
            use_rtw = False
            
            try:
                car_ktw = driver.find_element_by_xpath('//*[@ktw="1" and @class="vehicle_checkbox"]')
            except Exception:
                use_rtw = True
                use_ktw = False

            try:
                car_rtw = driver.find_element_by_xpath('//*[@rtw="1" and @class="vehicle_checkbox"]')
            except Exception:
                use_rtw = False

            if  use_ktw == True:
                print("Alert [Mission-ID: " + mission_ids[0] + " | Vehicle ID: " + car_ktw.get_attribute('value') + " | Unit type: KTW]")
                car_ktw.click()
                driver.find_element_by_name("commit").click()
                missions_completed += 1
            elif use_rtw == True:
                print("Alert [Mission-ID: " + mission_ids[0] + " | Vehicle ID: " + car_rtw.get_attribute('value') + " | Unit type: RTW]")
                car_rtw.click()
                driver.find_element_by_name("commit").click()
                missions_completed += 1
            elif use_ktw == False and use_rtw == False:
                print("Currently no emergency Verhicle is available")
            mission_ids.pop(0)
            driver.get("https://www.leitstellenspiel.de")

driver.quit()
print("Completed " + str(missions_completed) + " patient transports successfully.")
time.sleep(5)