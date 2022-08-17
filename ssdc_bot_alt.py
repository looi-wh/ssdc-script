import smtplib, ssl
import subprocess
import sys
try: # running try function during import as an attempt to auto install pip modules
    from selenium import webdriver
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
import winsound
try:
    from webdriver_manager.chrome import ChromeDriverManager # pip3 install webdriver_manager
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver_manager"])
    from webdriver_manager.chrome import ChromeDriverManager
import pickle
try:
    from fake_useragent import UserAgent
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fake_useragent"])
    from fake_useragent import UserAgent
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
try:
    import mouse
    import keyboard
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mouse"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
    import mouse
    import keyboard

# VARIABLES
# CHANGE THESE VARIABLES FOR YOUR OWN LIKING
refreshMaxCount = 45 # this will be the maximum of the day before the script gets kicked out of the system
timeToSpare = 120 # the wait time between each try
autoPurchase = 0 # set 1 to enable auto purchase function (experimental)
runChromeHeadless = 0   # 0 = run chrome as normal, good for debugging purposes
                        # 1 = run chrome in headless mode, good for do not disturb (not recommended as google captcha now exists)

username = ""
password = ""

def openPage(username=None, password=None): # [modified by looi] everything is converted to a function here
    global browser, timer1, timer2, timer3, autoPurchase
    if not username == None and not password == None:
        browser.get('https://www.ssdcl.com.sg/User/Login')
        print("[openPage] opened ssdc website")
        browser.maximize_window()
        try:
            browser.find_element(By.CLASS_NAME, 'grecaptcha-badge')
        except:
            try:
                userAgentBlacklist = pickleLoad("userAgentBlacklist")
            except:
                userAgentBlacklist = []
            userAgentBlacklist.append(str(user_agent))
            pickleSave("userAgentBlacklist", userAgentBlacklist)
            print("[openPage] the current user agent does not seem to support recaptcha")
            print("[openPage] just simply restart the script and browser. the script will generate a new user agent for you again")
            print("[openPage] userAgentBlacklist list size:", len(pickleLoad("userAgentBlacklist")))
            countdown(120)
            return 1
        try:
            idLogin = browser.find_element(By.ID, 'UserName')
            idLogin.send_keys(username)
            idLogin = browser.find_element(By.ID, 'Password')
            idLogin.send_keys(password)
            loginButton = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/div/div/form/div[5]/div/button')
            time.sleep(random.randint(timer1[0], timer1[1]))
            loginButton.click() # clicks the button login
            print("[openPage] logged in with account credentials")
        except:
            print("[openPage] loaded previous session, probably an existing cache")
    accountStatusRaw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/p[1]')))
    accountStatus = str(accountStatusRaw.text)
    print("[openPage]", str(accountStatus))
    purchaseStatusRaw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/p[2]')))
    purchaseStatus = str(purchaseStatusRaw.text)
    if not purchaseStatus == "You have no item pending payment" and autoPurchase == 1:
        print("[warning] you have items pending payment, autoPurchase is unable to function")
        print("[warning] autoPurchase has been disabled")
        autoPurchase = 0
    # Accessing the booking menu
    bookingAndCancellation = browser.find_element(By.XPATH, '//*[@id="bodyContent"]/div[2]/ul/li[4]/a')
    time.sleep(random.randint(timer1[0], timer1[1]))
    bookingAndCancellation.click()
    print("[openPage] clicked on bookingAndCancellation")
    newBooking = browser.find_element(By.XPATH, '//*[@id="btnNewBooking"]')
    time.sleep(random.randint(timer1[0], timer1[1]))
    newBooking.click()
    print("[openPage] clicked on newBooking")
    selectAgree = browser.find_element(By.XPATH, '//*[@id="chkProceed"]')
    selectAgree.click()
    if random.randint(0,100) < 10:
        print("[openPage] agreed to sell you away to pirates")
    else:
        print("[openPage] agreed to the terms and conditions")
    proceedButton = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/p[8]/a')
    time.sleep(random.randint(timer1[0], timer1[1]))
    proceedButton.click()
    print("[openPage] clicked the proceed button")
    print("[openPage] website is ready")
    return 0

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
        screenshot("purchase_receipt")
        print("[makePurchase] purchase of slot is successful")
        return 0
    except:
        print("[warning] something went wrong. please manually verify purchase")
        return 1


def convertTime(inputx):
    if os.name == 'nt':
        return (datetime.strptime(str(inputx), '%Y-%m-%d %H:%M:%S')).strftime("%#d/%#m/%Y") # windows
    else:
        try:
            return (datetime.strptime(str(inputx), '%Y-%m-%d %H:%M:%S')).strftime("%-d/%-m/%Y") # linux
        except:
            raise "[convertTime] convertTime function does not support the current method of conversion"

def pickleSave(var_name, var_input): # offers an option to save variables into a single file
    if os.path.exists("configs.p"):
        pickleRemove(var_name)
        existing_pickles = pickle.load(open("configs.p", "rb"))
    else:
        existing_pickles = [[],[]]
    existing_pickles[0].append(str(var_name))
    existing_pickles[1].append(var_input)
    pickle.dump(existing_pickles,open("configs.p", "wb"))
    del existing_pickles # clears variable as soon as it is done

def pickleRemove(var_name):
    if os.path.exists("configs.p"):
        existing_pickles = pickle.load(open("configs.p", "rb"))
        for x in range(0, len(existing_pickles[0])):
            if str(existing_pickles[0][x]) == str(var_name):
                existing_pickles[0].pop(x)
                existing_pickles[1].pop(x)
                pickle.dump(existing_pickles,open("configs.p", "wb"))
                break

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
                print("[notice] pickle file has been validated")
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
                print("\n")
                print("refresh limit of", refreshMaxCount, "has been hit for the day")
                print("you wont be able to view more slots until tomorrow")
                print("")
                print("the script will now exit in 60 seconds")
                time.sleep(999999)
                exit()
            else:
                count = int(pickleLoad("Lcount"))
                count = count + 1
                pickleSave("Lcount", count)
        else:
            print("[LcountAdd] Lcount has been reset to 1 due to different Lday")
            pickleSave("Lcount", 1) # new day = new count
            pickleSave("Lday", datetime.fromisoformat(str(datetime.now().date())))
    except:
        print("[warning] something went wrong while trying to add new count to Lcount")
        print("[warning] please verify pickle file manually")

def restartBrowser():
    global browser
    time.sleep(10)
    browser.quit()
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    openPage(username, password)

def countdown(t):
    tOri = t
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("[countdown] waiting for", timer, "(mm:ss)", end="\r")
        time.sleep(1)
        t -= 1
    mins, secs = divmod(tOri, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    print("[countdown] timer finished for", timer, "(mm:ss)")

def playsoundOverlay(sound_location):
    # there has been a new method of playing sound in the background without any consequences to delays or future playback
    # by arranging the purge to the front, we can instead purge any existing playback before starting a new one
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
        winsound.PlaySound(str(sound_location), winsound.SND_ASYNC | winsound.SND_ALIAS )
        #winsound.PlaySound(str(sound_location), winsound.SND_ASYNC)
        #time.sleep(3)
    except:
        print("[warning] audio could not be played on this device")

class Mail:
    def __init__(self):
        global emailUsername, emailPassword
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = emailUsername
        self.password = emailPassword

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()

def screenshot(comment=None):
    now = datetime.now()
    if str(comment) == None:
        dt_string = "./others/" + str(now.strftime("%d_%m_%Y %H_%M_%S") + ".png")
    else:
        dt_string = "./others/" + str(now.strftime("%d_%m_%Y %H_%M_%S") + " " + str(comment) + ".png")
    browser.save_screenshot(dt_string)
    print("[screenshot] saved as ", dt_string)
    return 0

def sendEmailNotification(emailContent=None):
    if emailUsername == "empty" and emailPassword == "empty":
        return 0
    if emailContent == None:
        emailContent = "this is a simple notification from ssdc-bot. emailContent was not provided with a content"
    try:
        mail = Mail()
        mail.send(emailUsername.split(), "ssdc-bot notification", str(emailContent))
        print("[sendEmailNotification] an email was sent to", str(emailUsername))
    except:
        print("[sendEmailNotification] an error has occured and script was unable to send an email")

def antiCaptcha(closeButtonXPATH):
    global browser
    # anti-captcha setup
    # this script relies on a browser extension that helps to solve google captchas
    # since google captcha is able to detect mouse movements, it is then better to record the user mouse movement instead
    #
    # this function will attempt to auto detect if the pop up has been closed, and will automatically record down mouse movement
    # meaning, the function is near automatic as long as the captcha has been completed once before
    try: # attempts to detect if google captcha is out
        close_button = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, closeButtonXPATH)))
    except:
        print("[antiCaptcha] google captcha does not seem to have been loaded yet")
        return 1
    print("[antiCaptcha] antiCaptcha started")
    try:
        mouseMovementCaptcha = pickleLoad("mouseMovementCaptcha") # clicking captcha and buster
        mouseMovementCaptchaFailures = pickleLoad("mouseMovementCaptchaFailures")
        #raise IndexError
        print("[antiCaptcha] existing mouse movement record has been found, simulating user interaction..")
        #browser.minimize_window()
        #browser.maximize_window()
        mouse.play(mouseMovementCaptcha,speed_factor=3, include_clicks=True, include_moves=True, include_wheel=True)
        time.sleep(1)
        try:
            close_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, closeButtonXPATH))) # ok button
            print("[antiCaptcha] failed, please solve captcha by yourself")
            pickleSave("mouseMovementCaptchaFailures", int(pickleLoad("mouseMovementCaptchaFailures")) + 1)
            if pickleLoad("mouseMovementCaptchaFailures") > 2:
                mouseMovementCaptcha = []
                mouse.hook(mouseMovementCaptcha.append)
            count = 0
            while True:
                try:
                    count += 1
                    time.sleep(1)
                    close_button = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, closeButtonXPATH)))
                    if count > 30:
                        print("[antiCaptcha] you did not manually solve the captcha. function failed")
                        mouse.unhook(mouseMovementCaptcha.append)
                        return 1
                    continue
                except:
                    mouse.unhook(mouseMovementCaptcha.append)
                    pickleSave("mouseMovementCaptcha", mouseMovementCaptcha)
                    pickleSave("mouseMovementCaptchaFailures", 0)
                    print("[antiCaptcha] mouseMovementCaptcha length:", len(mouseMovementCaptcha))
                    print("[antiCaptcha] updated mouseMovementCaptcha successfully")
                    break
        except:
            print("[antiCaptcha] captcha solved")
            pickleSave("mouseMovementCaptchaFailures", 0)
            return 0
    except:
        print("[antiCaptcha] mouseMovementCaptcha not found")
        #browser.minimize_window()
        #browser.maximize_window()
        print("[antiCaptcha] recording started")
        print("[antiCaptcha] please solve the captcha manually using the buster extension and press okay")
        # recording mouse movement
        mouseMovementCaptcha = []
        mouse.hook(mouseMovementCaptcha.append)
        count = 0
        while True:
            try:
                count += 1
                time.sleep(1)
                close_button = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, closeButtonXPATH)))
                if count > 30:
                    print("[antiCaptcha] recording failed. please try again next time")
                    mouse.unhook(mouseMovementCaptcha.append)
                    return 1
            except:
                mouse.unhook(mouseMovementCaptcha.append)
                print("[antiCaptcha] mouseMovementCaptcha length:", len(mouseMovementCaptcha))
                pickleSave("mouseMovementCaptcha", mouseMovementCaptcha)
                pickleSave("mouseMovementCaptchaFailures", 0)
                print("[antiCaptcha] mouse movement successfully recorded")
                break
        print("\n")

def convertToHS(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d%02d" % (hour, minutes)

def update_id_list(id_list, allowance=None, nightTime=None, wakeTime=None, morningSlots=None):
    # this function focuses on removing timings that might be impossible to achieve
    # this will ensure achievability of slots
    # session timing info (from 1 to 7), update if changes
    sessions = []
    sessions.append("0800")
    sessions.append("0950")
    sessions.append("1215")
    sessions.append("1405")
    sessions.append("1555")
    sessions.append("1820")
    sessions.append("2010")
    if allowance == None:
        allowance = 200 # 2 hours, 100 = 1 hour
    if nightTime == None:
        nightTime = 2200
    if wakeTime == None:
        wakeTime = 800
    if morningSlots == None: # accepts arrays
        morningSlots = [1,2] # block first two slots

    today = convertTime(datetime.fromisoformat(str(datetime.now().date())))
    today_id = []
    for x in range(0, len(id_list)):
        if str(id_list[x][2:]) == today:
            today_id.append(id_list[x])
    to_remove_id = []
    current_time = int(convertToHS(time.time() + 3600 * 8))
    for x in today_id:
        position = int(x[0]) - 1
        if (current_time + int(allowance)) > int(sessions[position]):
            to_remove_id.append(x)
    if current_time > 0000 and current_time < wakeTime:
        tomrrow = today
    else:
        tomrrow = convertTime(datetime.fromisoformat(str(datetime.now().date())) + timedelta(days = 1))
    if (current_time > nightTime) or (current_time < wakeTime):
        for x in morningSlots:
            to_remove_id.append(str(x) + "_" + str(tomrrow))
    for x in to_remove_id:
        for y in range(0, len(id_list)):
            if str(x) == str(id_list[y]):
                print("[update_id_list] removed", id_list[y], "due to time restrictions")
                id_list[y] = "removed"
    try:
        while True:
            id_list.remove("removed")
    except ValueError:
        pass
    return id_list


print("script started")
start_time = time.time()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument("--incognito")
ua = UserAgent()
try:
    userAgentBlacklist = pickleLoad("userAgentBlacklist")
except:
    userAgentBlacklist = []
    pickleSave("userAgentBlacklist", userAgentBlacklist)
while True:
    user_agent = ua.random
    temp = 0
    for x in userAgentBlacklist:
        if str(user_agent) == x:
            temp += 1
    if temp == 1:
        user_agent = ua.random
        continue
    else:
        break
print("currently user_agent:")
print(user_agent)
options.add_extension('./extension/buster.crx')
options.add_argument(f'user-agent={user_agent}')
if runChromeHeadless == 1:
    options.add_argument('headless')
    options.add_argument('window-size=1400,600')
    options.add_argument("disable-gpu")
browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
html_file = Path.cwd() / "others/index.html"
browser.get(html_file.as_uri())



# main_
timer1 = [3, 5]
timer2 = [4, 7]
timer3 = [0, 0]

print("")
try:
    if int(timeToSpare) < 60:
        print("[warning] timeToSpare variable is less than 60 seconds, which might lead to more problems")
    timer3[0] = int(timeToSpare) * 0.5
    timer3[1] = int(timeToSpare) * 2
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
            try:
                browser.find_element(By.CLASS_NAME, 'grecaptcha-badge')
            except:
                print("the current user agent does not seem to support recaptcha")
                print("please restart the script and browser and try again")
                time.sleep(999999)
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


# add email component
try:
    emailUsername = pickleLoad("emailUsername")
    emailPassword = pickleLoad("emailPassword")
    print("your gmail account has been grabbed from the pickle file")
    print("you will be notified when a slot has been found")
    print("\n")
except IndexError:
    while True:
        emailUsername = input("email username (leave blank to disable): ")
        if emailUsername == "":
            print("email notification has been disabled")
            emailUsername = "empty"
            emailPassword = "empty"
            break
        emailPassword = getpass("email password (not your default password): ")
        try:
            mail = Mail()
            content = "if you are receiving this, ssdc-bot has successfully connected to your email. you will be receiving notification when the bot is successful"
            mail.send(emailUsername.split(), "ssdc-bot notification: setup successful", str(content))
            pickleSave("emailUsername", emailUsername)
            pickleSave("emailPassword", emailPassword)
            print("account has been validated successfully")
            print("you will be receiving updates via email once a purchase is completed")
            print("\n")
            break
        except:
            print("unable to connect to your gmail account")
            print("you are suppose to put in an app specific password generated from gmail")
            continue


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

location = 0

dates = []
while True:
    date_entry = input("enter date in YYYY-MM-DD format (e.g. 2018-12-31, leave blank for today): ")
    try:
        today = datetime.fromisoformat(str(datetime.now().date()))
        if date_entry == "":
            date1 = today
        else:
            date1 = datetime.fromisoformat(date_entry)
        if date1 < today:
            print("given", str(date1), "but today is", str(today))
            print("please try again")
            continue
        break
    except:
        print("invalid date, please try again")
while True:
    look_ahead_entry = input("would you like to look ahead for 120 days (Y/n, leave blank to select 'yes'): ")
    try:
        if look_ahead_entry == "y" or "" or "Y" or "yes" or "Yes":
            for x in range(120):
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
# for x in dates: print(x) # debugging purposes


id_list = []

while True:
    try:
        x = []
        while True:
            xtemp = input("enter session number (1-7) to grab (and enter 'done' to confirm, or you can just leave blank to select all): ")
            if xtemp == "done":
                break
            if xtemp == "":
                x = [1, 2, 3, 4, 5, 6, 7]
                break
            x.append(int(xtemp))
        for a in x:
            if a < 1 or a > 7:
                print("enter valid numbers. Please try again from begining")
                continue
            elif look_ahead_entry=="n":
                id = str(a) + "_" + str(convertTime(dates[0]))
                id_list.append(id)
            else:
                for id_date in dates:
                    id = str(a) + "_" + str(convertTime(id_date))
                    id_list.append(id)
        break

    except ValueError:
        print("enter valid numbers")
        continue

id_list = update_id_list(id_list) # remove any impossible target
print("list size:", len(id_list))
print("last slot:", id_list[-1])

print("\n")
print("the list above represent the number of session the script is attempting to find")
print("input validated, issuing commands right now")
print("\n")
print("you are currently running a tester script that detects get latest instead of check availability")
print("unlike check availability, get latest does not have a hard coded limit")
print("and thus, this method can help to reduce the chances of hitting the maximum limit in a single day")
print("script is still in working phrase, so please monitor the script and not leave it alone to run")
print("\n")
print("note: running ctrl + c will make the script think it found a slot, so dont")
print("\n")
print("log:")
if runChromeHeadless == 1:
    print("[warning] chrome is running in headless mode")
    print("[warning] closing this script might not close the headless chrome itself")
    print("[warning] and so, please do not run thousand of instance of this script without thinking")
    print("[warning] or better, disable headless mode in the settings")
    print("[warning] there is a script that can be executed in windows to help kill ALL instances of chrome")

openPageAttempt = 0
try:
    while openPageAttempt < 3:
        openPageAttempt += 1
        if openPageAttempt > 1:
            print("[warning] try number", openPageAttempt)
        openPageResult = openPage(username, password)
        if openPageResult == 0:
            break
        else:
            print("[warning] openPage returned a failure warning")
except:
    browser.quit()
    print("openPage function failed. Something went wrong")
    print("please verify script")
    print("\n")
    print("this failure usually occur due to invalid programming in the openPage function")
    print("this could occur when the ssdc website receives updates")
    print("check for any latest updates, or check with the developer himself")
    time.sleep(999999)
    exit()

count = 0
while len(id_list) != 0:
    while True:
        getEarliestDateFailureCounter = 0
        id_list = update_id_list(id_list)
        while True:
            try:
                getEarliestDate = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[9]/div/div/input')
                getEarliestDate.click()
                getEarliestDateFailureCounter = 0
                break
            except:
                getEarliestDateFailureCounter += 1
                if getEarliestDateFailureCounter < 9:
                    print("[warning] getEarliestDate function failed. retrying..")
                    countdown(10)
                    continue
                elif getEarliestDateFailureCounter > 10:
                    print("[fatal] something went wrong while trying to click getEarliestDate. please restart script.")
                    time.sleep(999999)
                    exit()
                else:
                    print("[warning] restarting browser..")
                    restartBrowser()
        count = count + 1
        print("[", count, "] searching for slots")
        try: # test if website is still active
            checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]') # tester
        except: # restart website
            print("[warning] website failed to respond as expected, restarting browser")
            browser.quit()
            browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
            openPage(username, password)
            time.sleep(random.randint(timer1[0], timer1[1]))
            continue
        getEarliestDateTryCount = 0
        try:
            modalMsgContentRaw = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]')))
            modalMsgContent = str(modalMsgContentRaw.text)
        except:
             modalMsgContent = ""
             #playsoundOverlay("./others/chance.wav")
             print("[", count, "] warning, modalMsgContent taking quite awhile to respond, possible chance detected")
             break
        if not modalMsgContent == "All the slots are Fully Booked.":
            print("[", count, "] modalMsgContent is not 'All the slots are Fully Booked.'")
            if not modalMsgContent == "":
                print("[", count, "]", modalMsgContent)
            break
        elif modalMsgContent == "You have reached the daily maximum attempts.Please try again tomorrow.":
            print("maximum attempt reached")
            exit()
        else:
            closeCount = 0
            while closeCount < 5:
                try:
                    time.sleep(1)
                    closeButton = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/button')
                    closeButton.click()
                    break
                except:
                    closeCount += 1
            vwait = random.randint(timer3[0], timer3[1])
            print("[", count, "] modalMsg responded with the fully booked messsage")
            #print("[", count, "] trying again in", vwait, "seconds")
            countdown(vwait)
            try:
                closeButton = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/button')
                closeButton.click()
            except:
                pass
            continue

    # reaching here will mean getEarliestDate did not receive an expected result of fully booked
    # from this point onwards, it will be hunting down the slots we want
    # if theres a slot found but its not the date we want, the script will ignore it
    LcountAdd() # tells the system to count
    #dateValueRaw = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[3]/form/div[4]/div/input')
    #dateValue = str(dateValueRaw.get_attribute("value"))
    #print("[Lcount:", pickleLoad("Lcount"), "] earliest reported date:", str(dateValue))
    #print("[Lcount:", pickleLoad("Lcount"), "] filling in requested date")
    #date_elem = browser.find_element(By.ID, 'SelectedDate')
    #date_elem.send_keys(Keys.CONTROL + "a")
    #date_elem.send_keys(Keys.DELETE)
    #date_elem.send_keys(date1.strftime("%d %b %Y"))
    #date_elem.send_keys(Keys.RETURN)
    checkForAva = browser.find_element(By.XPATH, '//*[@id="btn_checkforava"]')
    checkForAva.click()
    print("[Lcount:", pickleLoad("Lcount"), "] checking slot via checkForAva!")
    try: # test for daily maximum attempt
        modalMsgContentRaw = WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]')))
        modalMsgContent = str(modalMsgContentRaw.text)
        if modalMsgContent == "You have reached the daily maximum attempts.Please try again tomorrow.":
            print("[warning] a limit notice has been issued to the user, max limit has been reached")
            pickleSave("Lcount", refreshMaxCount + 1)
            print("[warning] please close the script and run tomorrow instead")
            time.sleep(99999999)
    except: # ignore
        pass
        browser.execute_script("window.scrollTo(0, window.scrollY + 850)")
        screenshot("checkAvability")
    id_list_booked = []
    try:
        booking_conditions = " or ".join(["contains(@id, '%s')" % keyword for keyword in id_list])
        expression = "//*[%s]" % booking_conditions
        booking_slot = browser.find_element(By.XPATH,(expression))
        slot_id = booking_slot.get_attribute("id")
        for id in id_list:
            if id in slot_id:
                id_list.remove(id)
                id_list_booked.append(id)
                break
            else:
                pass
        WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.XPATH, expression)))
        booking_slot.click()
        modalMsgContentRaw = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]')))
        modalMsgContent = str(modalMsgContentRaw.text)
        if "The selected time-slot has been booked for you." in modalMsgContent:
            print("successfully booked", str(slot_id),"slot")
        else:
            id_list.append(slot_id)
        closeButton = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[3]/button')
        closeButton.click()
        playsoundOverlay("./others/chance.wav")
    except IndexError as error:
        print(error)
        pass
    purchaseStatusRaw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/p[2]')))
    purchaseStatus = str(purchaseStatusRaw.text)
    if not len(id_list_booked) == 0 and not purchaseStatus == "You have no item pending payment":
        print("[Lcount:", pickleLoad("Lcount"), "] successfully bought", len(id_list_booked), "slots")
        print("[Lcount:", pickleLoad("Lcount"), "] bookings made:")
        content = "purchased "
        for id_name in id_list_booked:
            print("[Lcount:", pickleLoad("Lcount"), "]", id_name)
            content = content + id_name + ", "
        content = content + "a total of " + str(len(id_list_booked)) + " slots has been booked."
        if autoPurchase == 1:
            purchaseStatusRaw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/p[2]')))
            purchaseStatus = str(purchaseStatusRaw.text)
            print("[Lcount:", pickleLoad("Lcount"), "]", str(purchaseStatus))
            print("[Lcount:", pickleLoad("Lcount"), "] autoPurchase is enabled, making purchase of slot")
            makePurchase()
            purchaseStatusRaw = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[1]/p[2]')))
            purchaseStatus = str(purchaseStatusRaw.text)
            if purchaseStatus == "You have no item pending payment":
                print("[Lcount:", pickleLoad("Lcount"), "] makePurchase is successful please login to confirm your booking")
                print("[Lcount:", pickleLoad("Lcount"), "] slot has been paid")
                content = content + " payment has been made successfully. however, please login to confirm your booking when you are free"
            else:
                print("[Lcount:", pickleLoad("Lcount"), "] makePurchase is NOT successful")
                print("[Lcount:", pickleLoad("Lcount"), "] please manually make payment instead")
                print("[Lcount:", pickleLoad("Lcount"), "] autoPurchase has been disabled")
                content = content + " payment is unsuccessful. autoPurchase will be disabled. Please login to make payment within 40 minutes"
                autoPurchase = 0
            openPage() # restarts the website for scanning
        else:
            content = content + " Please login to make payment within 40 minutes"
        sendEmailNotification(content)
    elif not len(id_list_booked) == 0 and purchaseStatus == "You have no item pending payment":
        print("[Lcount:", pickleLoad("Lcount"), "] a total of", str(len(id_list_booked)), "has been reported booked. But ssdc reported no payment pending..")
        vwait = random.randint(timer3[0], timer3[1])
        countdown(vwait)
    else:
        print("[Lcount:", pickleLoad("Lcount"), "] no wanted slots found, maybe false alarm")
        vwait = random.randint(timer3[0], timer3[1])
        countdown(vwait)
    continue # restart back to front


print("script has completed")