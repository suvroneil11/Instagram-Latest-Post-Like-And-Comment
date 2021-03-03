from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from json import dumps
import random
import emoji
import time
import os

#Set your username and password as environment variable
username_ig = os.environ.get('IG_USER')
password_ig = os.environ.get('IG_PASS')

#Replace this list with any list of comments you want to post
comments = ['Please stop looking so hot every time!', 'Definitely the most beautiful woman on the planet', 'Okay, I’m sorry but I’m pretty sure it’s illegal to look this good :P',
            'I tried many combinations of words to praise you well, every time I ended up dissatisfied!', 'Beauty is for children and you are much more than that B!',
            'Are you a driver because you’re driving me crazy with your beauty! ;)','Your beauty is full of endless possibilities B!'
           ]
#Chrome Option parameters
def chrome_opt():
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    return chrome_options

#Download Chromedriver and keep the the exe file in the D drive
driver = webdriver.Chrome(chrome_options=chrome_opt(),executable_path="D:\chromedriver.exe")

#Replace xyz with the username of the profile where you want to run the script
driver.get("https://www.instagram.com/xyz")
time.sleep(2)

#Login Form
username =driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
username.send_keys(username_ig)
password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
password.send_keys(password_ig)
password.send_keys(Keys.RETURN)
time.sleep(3)

#For selecting not now when IG asks if you want to save login info
driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
time.sleep(5)

#For getting the span which contains number of posts
get_post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
post = get_post.text
post = int(post)

#This loop runs until script is stopped manually or there is no internet connection
while True:
    time.sleep(5)
    get_post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
    posts = get_post.text
    posts= int(posts)

    #To get the latest post if someone deletes posts from there account
    if posts<post:
        post = posts

    #When someone uploads a new picture
    if post < posts:
        comment = random.choice(comments) #randomly getting a comment from the comment list
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]').click() #Opening the latest photo
        time.sleep(5)
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()           #Liking the photo
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[2]/button').click()           #Clicking the comment button
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea').send_keys(emoji.emojize("{} :red_heart:".format(comment),variant="emoji_type")) #Posting the comment
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea').send_keys(Keys.RETURN)
        print("Commented Successfully!")
        comments.remove(comment)  #Removing the comment posted from the comment list
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[5]/div[3]/button').click()  #closing the photo
        post = posts
    time.sleep(300)
    driver.refresh()
