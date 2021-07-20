from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup

class faceBroswer:
    def __init__(self, db):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.browser.get("https://www.facebook.com")
        self.db = db

    def loginbrowser(self, usr, pwd):
        print(usr + " --- " + pwd)
        self.browser.find_element_by_id("email").send_keys(usr)
        self.browser.find_element_by_id("pass").send_keys(pwd)
        self.browser.find_element_by_name("login").click()
        sleep(2)
        try:
            if self.browser.find_element_by_name("login"):
                return 0
        except NoSuchElementException:
            return 1

    def getfriendlist(self):
        info_list = []
        self.browser.get("https://www.facebook.com/me/friends")
        sleep(2)
        self.scrollpage(2)
        bsoup = BeautifulSoup(self.browser.page_source, "lxml")
        tabfriend = bsoup.findAll("div", {"class": "buofh1pr hv4rvrfc"})
        for friend in tabfriend:
            mfrd = 0
            link = friend.findAll("a")
            for l in link:
                if "mutual" in l.get("href"):
                    mtext = l.text
                    ar = mtext.split()
                    mfrd = ar[0]
                else:
                    email = l.get("href")
                    name = l.text
            print("Name: " + name + " --- Link : " + email + " --- Ban chung: " + str(mfrd))
            info_list.append([name, email, mfrd])
        self.db.insert(info_list)

    def unfriend_by_email(self, email_list):
        for email in email_list:
            self.browser.get(email)
            sleep(1.5)
            try:
                self.browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/div/div/div").click()
                sleep(1.5)
                self.browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[4]").click()
                sleep(1.5)
                self.browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[1]/div[1]/div").click()
                sleep(0.5)
            except:
                pass

    def scrollpage(self, time):
        wait_time = time
        cur_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(wait_time)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == cur_height:
                break
            cur_height = new_height
        sleep(1)

