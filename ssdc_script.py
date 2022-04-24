import subprocess
import sys
try: # running try function during import as an attempt to auto install pip modules
    from selenium import webdriver
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
try:
    from webdriver_manager.chrome import ChromeDriverManager # pip3 install webdriver_manager
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
    from webdriver_manager.chrome import ChromeDriverManager
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path
import time
import random
import os


start_time = time.time()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--incognito")
browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
html_file = Path.cwd() / "others/index.html"
browser.get(html_file.as_uri())

# VARIABLES
# CHANGE THESE VARIABLES FOR YOUR OWN LIKING
refreshMaxCount = 45 # this will be the maximum of the day before the script gets kicked out of the system
timeToSpare = 300 # minimum time between intervals in seconds
autoPurchase = 0 # set 1 to enable auto purchase function (experimental)




def openPage(username, password): # [modified by looi] everything is converted to a function here
    global browser
    browser.get('https://www.ssdcl.com.sg/User/Login')
    browser.maximize_window()
    idLogin = browser.find_element(By.ID, 'UserName')
    idLogin.send_keys(username)
    idLogin = browser.find_element(By.ID, 'Password')
    idLogin.send_keys(password)
    loginButton = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/div/div/form/div[5]/div/button')
    time.sleep(random.randint(timer1[0], timer1[1]))
    loginButton.click() # clicks the button login
    # Accessing the booking menu
    bookingAndCancellation = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/ul/li[4]/a')
    time.sleep(random.randint(timer1[0], timer1[1]))
    bookingAndCancellation.click()
    newBooking = browser.find_element(By.XPATH, '//*[@id="btnNewBooking"]')
    time.sleep(random.randint(timer1[0], timer1[1]))
    newBooking.click()
    selectAgree = browser.find_element(By.XPATH, '//*[@id="chkProceed"]')
    selectAgree.click()
    proceedButton = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/p[8]/a')
    time.sleep(random.randint(timer1[0], timer1[1]))
    proceedButton.click()

def makePurchase():
    global browser
    browser.get('https://www.ssdcl.com.sg/User/Payment/ConfirmPurchase')
    try:
        purchasePriceRaw = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form[1]/div[2]/table/tbody/tr/td[5]/span')
        purchasePrice = float(purchasePriceRaw.text)
        print("slot price is", str(purchasePrice))
        availableMoneyRaw = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form[1]/div[2]/table/tfoot/tr[4]/td[2]/strong')
        availableMoney = float(availableMoneyRaw.text)
        print("you have", str(availableMoney), "in your account")
        if not purchasePrice > availableMoney:
            print("[warning] you do not have enough money in your account to purchase this slot")
            print("[warning] please manually purchase slot")
            return 1
        confirmPurchase = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form[1]/div[2]/table/tfoot/tr[5]/td[1]/a')
        confirmPurchase.click()
        printReceipt = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/div[1]/table/tbody/tr/td/a')
        return 0
    except:
        print("[warning] something went wrong. please manually verify purchase")
        return 1


def convertTime(inputx):
    try:
        return (datetime.strptime(str(inputx), '%Y-%m-%d %H:%M:%S')).strftime("%#d/%#m/%Y") # windows
    except:
        try:
            return (datetime.strptime(str(inputx), '%Y-%m-%d %H:%M:%S')).strftime("%-d/%-m/%Y") # linux
        except:
            raise "convertTime function does not support the current method of conversion"

def pickleSave(var_name, var_input): # offers an option to save variables into a single file
    if os.path.exists("configs.p"):
        existing_pickles = pickle.load(open("configs.p", "rb"))
        for x in range(0, len(existing_pickles[0])):
            if str(existing_pickles[0][x]) == str(var_name):
                existing_pickles[0].pop(x)
                existing_pickles[1].pop(x)
                pickle.dump(existing_pickles,open("configs.p", "wb"))
        existing_pickles = pickle.load(open("configs.p", "rb"))
    else:
        existing_pickles = [[],[]]
    existing_pickles[0].append(str(var_name))
    existing_pickles[1].append(var_input)
    pickle.dump(existing_pickles,open("configs.p", "wb"))
    del existing_pickles # clears variable as soon as it is done

def pickleLoad(var_name):
    if os.path.exists("configs.p"):
        existing_pickles = pickle.load(open("configs.p", "rb"))
        for x in range(0, len(existing_pickles[0])):
            if str(existing_pickles[0][x]) == str(var_name):
                return existing_pickles[1][x]
    raise IndexError

def pickleVerify():
    # 0: pickle file has been verified successfully
    # 1: pickle does not exists
    # 2: pickle file has been corrupted but its fixable
    # 3: pickle file has been corrupted but its no longer fixable
    if not os.path.exists("configs.p"):
        print("[warning] pickle file cannot be found")
        return 1
    try:
        existing_pickles = pickle.load(open("configs.p", "rb"))
        if len(existing_pickles) == 2:
            if len(existing_pickles[0]) == len(existing_pickles[1]):
                return 0
            else:
                print("[warning] pickle len of 0 and 1 does not match")
                return 3
        else:
            print("[warning] pickle file len is", len(existing_pickles))
            return 3
    except:
        print("[warning] an exception has occured")
        return 3

def LcountAdd():
    try:
        today = datetime.fromisoformat(str(datetime.now().date()))
        if pickleLoad("Lday") == today:
            if int(pickleLoad("Lcount")) >= refreshMaxCount:
                print("refresh limit of", refreshMaxCount, "has been hit for the day")
                print("you wont be able to view more slots until tomorrow")
                print("")
                print("the script will now exit in 60 seconds")
                time.sleep(60)
                exit()
            else:
                count = int(pickleLoad("Lcount"))
                count = count + 1
                pickleSave("Lcount", count)
        else:
            pickleSave("Lcount", 1) # new day = new count
            pickleSave("Lday", datetime.fromisoformat(str(datetime.now().date())))
    except:
        print("[warning] something went wrong while trying to add new count to Lcount")
        print("[warning] please verify pickle file manually")

# main_
timer1 = [3, 5]
timer2 = [4, 7]
timer3 = [0, 0]
print("")
try:
    if int(timeToSpare) < 60:
        timer3 = [60, 60*2]
    else:
        if int(timeToSpare) >= 60:
            timer3[0] = int(timeToSpare)
            timer3[1] = timer3[0] + 60
        else:
            timer3 = [60, 60*2]
except ValueError:
        print("timeToSpare variable is invalid")
        time.sleep(60)
        exit()

try:
    username = pickleLoad("username")
    password = pickleLoad("password")
    print("your login credentials has been grabbed from an insecure file")
    print("to remove this file, please delete 'configs.p' from the local directory")
    print("")
except IndexError:
    while True:
        username = input("account username: ")
        password = getpass("account password (hidden): ")
        print("testing credentials.. please wait..")
        try:
            browser.get('https://www.ssdcl.com.sg/User/Login')
            idLogin = browser.find_element(By.ID, 'UserName')
            idLogin.send_keys(username)
            idLogin = browser.find_element(By.ID, 'Password')
            idLogin.send_keys(password)
            loginButton = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/div/div/form/div[5]/div/button')
            time.sleep(random.randint(timer1[0], timer1[1]))
            loginButton.click() # clicks the button login
            bookingAndCancellation = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/ul/li[4]/a')
            browser.get(html_file.as_uri()) # switches back to index.html
            print("credentials tested successfully")
            print("")
            print("this script can use pickle to save your password for you")
            print("but it will not be encrypted and will be stored locally")
            savePassword = input("so would you like to save login credentials insecurely (y/n): ")
            if savePassword == "y" or savePassword == "yes" or savePassword == "Y" or savePassword == "YES" or savePassword == "Yes":
                pickleSave("username", username)
                pickleSave("password", password)
                print("a pickle file has been created for you!")
            break
        except:
            browser.get(html_file.as_uri()) # switches back to index.html
            print("invalid login credentials, please try again")
            print("")


# caching variables in order to count existing tries to better improve the script experience
try:
    today = datetime.fromisoformat(str(datetime.now().date()))
    if pickleLoad("Lday") == today:
        if not str(pickleLoad("Lusername")) == str(username):
            overwriteLusername = input("[warning] by using a different username in this script, you are going to overwrite existing Lcount limit for today. Continue? (y/N): ")
            if overwriteLusername == "y" or overwriteLusername == "yes" or overwriteLusername == "Y" or overwriteLusername == "YES" or overwriteLusername == "Yes":
                pickleSave("Lusername", str(username))
                pickleSave("Lcount", 0)
            else:
                print("you specified 'n'. Counter will be set to 0 as default")
    else:
        pickleSave("Lday", today) # save as today
        pickleSave("Lusername", str(username))
        pickleSave("Lcount", 0)
except:
    # pickle file didnt contain anything about previous counts
    # so we will have to create a new variable inside the pickle file for future purposes
    today = datetime.fromisoformat(str(datetime.now().date()))
    pickleSave("Lday", today) # save as today
    pickleSave("Lusername", str(username))
    pickleSave("Lcount", 0)

if not pickleVerify() == 0:
    print("[fatal] pickle file is invalid")
    print("[fatal] here are the contents of pickle file for debugging purposes:", pickle.load(open("configs.p", "rb")))
    time.sleep(60)
    exit()

while True:
    dates = []
    date_entry = input("enter date in YYYY-MM-DD format (e.g. 2018-12-31): ")
    look_ahead_entry = input("look ahead for 7 days enable (y/n): ")
    try:
        today = datetime.fromisoformat(str(datetime.now().date()))
        date1 = datetime.fromisoformat(date_entry)
        if date1 < today:
            print("given", str(date1), "but today is", str(today))
            print("please try again")
            continue
        if look_ahead_entry == "y":
            for x in range(7):
                dates.append((date1 + timedelta(days = x)))
            break
        elif look_ahead_entry == "n":
            dates.append(date1)
            break
        else:
            print("look ahead is invalid")
            print("please try again")
            continue
    except ValueError:
        print("something went wrong")
        print("please try again")

while True:
    try:
        location = int(input("Enter 0 for Woodlands, 1 for Ang Mo Kio: "))
        if location < 0 or location > 1:
            print("Please enter a number")
            continue
        else:
            break
    except ValueError:
        print("Please enter either '0' or '1'")

id_list = []


while True:
    try:
        x = []
        xtemp = "empty"
        while True:
            xtemp = input("enter session number (1-7) to grab (enter 'done' to confirm): ")
            if xtemp == "done":
                break
            x.append(int(xtemp))
        for a in x:
            if a < 1 or a > 7:
                print("Enter valid numbers. Please try again from begining")
                continue
            elif look_ahead_entry=="n":
                id = str(a) + "_" + str(convertTime(dates[0]))
                id_list.append(id)
            elif look_ahead_entry=="y":
                for id_date in dates:
                    id = str(a) + "_" + str(convertTime(id_date))
                    id_list.append(id)
            else:
                pass
        break

    except ValueError:
        print("Enter valid numbers")
        continue

for h in id_list:
    print(h)

print("\n")
print("input validated, issuing commands right now")
try:
    openPage(username, password)
except:
    browser.quit()
    print("openPage function failed. Something went wrong")
    print("Please restart script")
    time.sleep(60)
    exit()

if location == 1:
    loc = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[5]/div/select/option[2]')
    loc.click()
date_elem = browser.find_element(By.ID, 'SelectedDate')
date_elem.send_keys(Keys.CONTROL + "a")
date_elem.send_keys(Keys.DELETE)
date_elem.send_keys(date1.strftime("%d %b %Y"))
date_elem.send_keys(Keys.RETURN)


while len(id_list) != 0:
    LcountAdd()
    try:
        checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]')
        checkForAva.click()
        time.sleep(random.randint(timer1[0], timer1[1]))
        checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]') # tester
    except:
        try:
            recaptchaFailure = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/button')
            time.sleep(random.randint(timer1[0], timer1[1]))
            recaptchaFailure.click()
            newBooking = browser.find_element(By.XPATH, '//*[@id="btnNewBooking"]')
            time.sleep(random.randint(timer1[0], timer1[1]))
            newBooking.click()
            selectAgree = browser.find_element(By.XPATH, '//*[@id="chkProceed"]')
            selectAgree.click()
            proceedButton = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/p[8]/a')
            time.sleep(random.randint(timer1[0], timer1[1]))
            proceedButton.click()
            if location == 1:
                loc = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[5]/div/select/option[2]')
                loc.click()
            date_elem = browser.find_element(By.ID, 'SelectedDate')
            date_elem.send_keys(Keys.CONTROL + "a")
            date_elem.send_keys(Keys.DELETE)
            date_elem.send_keys(date1.strftime("%d %b %Y"))
            date_elem.send_keys(Keys.RETURN)
            checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]')
            time.sleep(random.randint(timer1[0], timer1[1]))
            checkForAva.click()
        except:
            browser.quit()
            browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
            openPage(username, password)
            time.sleep(random.randint(timer1[0], timer1[1]))
            if location == 1:
                loc = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[5]/div/select/option[2]')
                loc.click()
            date_elem = browser.find_element(By.ID, 'SelectedDate')
            date_elem.send_keys(Keys.CONTROL + "a")
            date_elem.send_keys(Keys.DELETE)
            date_elem.send_keys(date1.strftime("%d %b %Y"))
            date_elem.send_keys(Keys.RETURN)
            checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]')
            time.sleep(random.randint(timer1[0], timer1[1]))
            checkForAva.click()
            continue
    try:
        browser.execute_script("window.scrollTo(0, window.scrollY + 900)")
        booking_conditions = " or ".join(["contains(@id, '%s')" % keyword for keyword in id_list])
        expression = "//*[%s]" % booking_conditions
        #print(id_list)
        booking_slot = browser.find_element(By.XPATH,(expression))
        slot_id = booking_slot.get_attribute("id")
        for id in id_list:
            if id in slot_id:
                id_list.remove(id)
            else:
                pass
        WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH, expression)))
        booking_slot.click()
        if autoPurchase == 1:
            makePurchase()
            browser.quit()
            browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
            openPage(username, password)
            time.sleep(random.randint(timer1[0], timer1[1]))
            if location == 1:
                loc = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[5]/div/select/option[2]')
                loc.click()
            date_elem = browser.find_element(By.ID, 'SelectedDate')
            date_elem.send_keys(Keys.CONTROL + "a")
            date_elem.send_keys(Keys.DELETE)
            date_elem.send_keys(date1.strftime("%d %b %Y"))
            date_elem.send_keys(Keys.RETURN)
            checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]')
            time.sleep(random.randint(timer1[0], timer3[1]))
            checkForAva.click()
            LcountAdd()
        else:
            print("A class of id", str(slot_id), "has been booked, please login to confirm your booking within 40 mins")
        close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='modal-footer']/button[1]")))
        close_button.click()
        continue
    except:
        time.sleep(random.randint(timer3[0], timer3[1]))
        continue

print("script has completed")