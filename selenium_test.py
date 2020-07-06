import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

def pokemon_searcher(mon):
    driver = webdriver.Chrome()
    driver.get("https://bulbapedia.bulbagarden.net/wiki/Main_Page")
    box = driver.find_element_by_name('search')
    box.send_keys(mon)
    box.send_keys(Keys.ENTER)
    return

def twitch_buystock(stock, amount):
    d = webdriver.Chrome()
    d.get("https://twitchstocks.com/")
    account = d.find_element_by_id("mat-input-0")
    account.send_keys(stock)
    account.click()
    return

def marketwatch_game(stock):
    d = webdriver.Chrome()
    d.get("https://bit.ly/318moOT")
    user = d.find_element_by_id("username")
    passw = d.find_element_by_id("password")
    time.sleep(2)

    user.send_keys("rishabhv@hotmail.com")
    passw.send_keys("***********")
    passw.send_keys(Keys.ENTER)
    time.sleep(2)

    #d.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    d.get("https://www.marketwatch.com/game/stockbottester")
    time.sleep(2)
    search = d.find_element_by_css_selector("is.mw-autocomplete")
    search.send_keys(stock)
    #button = d.find_element_by_class_name("btn btn--primary join-game")
    #button.click()
    return
