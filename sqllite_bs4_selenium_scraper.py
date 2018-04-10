## This code will search for items in Morton Williams website and print the item on Sale.

import sqlite3
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display

ZIP = "10017"
input = "eggs"

ZIP_URL = "https://fetchquick.com/"

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1366x768")
#driver = webdriver.Chrome(executable_path="/home/ubuntu/mw_scrape/chromedriver", chrome_options=chrome_options)

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def main():

    driver.get(ZIP_URL)
    time.sleep(3)
    # type text
    text_area = driver.find_element_by_id('edit-store-enter-zip-code--2')
    text_area.send_keys(ZIP)

    # click submit button
    submit_button = driver.find_element_by_id('edit-submit')
    submit_button.click()

    time.sleep(3)

    text_search = driver.find_element_by_id('q')
    text_search.send_keys(input)


    #try:
    #    driver.find_element_by_link_text('All Departments').click()
    #except:
    #    print('naah')

    #menu_button.click()
    # Scrape url
    #skip_link = driver.find_element_by_id('skip-link')
    #skip_link.click()
    #find the first Product
    #print(driver.current_url)
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    #print(last_height)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source

    time.sleep(3)

    #html = urlopen(url, context=ctx).read()
    #print(html)
    # html.parser is the HTML parser included in the standard Python 3 library.
    # information on other HTML parsers is here:
    # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags=soup.find_all("div", class_="ais-infinite-hits--item")
    #print(tags[10])
    #print(tags[0])
    #print(tags[10:20])
    items = []
    for tag in tags:
        try:
            desc=tag.find("div", {"class": "product-name"}).text
            print(desc)
            main_price=tag.find("span", {"class": "main_price"}).text
            print(main_price)
            try:
                sell_price=tag.find("span", {"class": "sell_price"}).text
                promo=tag.find("div", {"class": "save_price"}).text
            except:
                sell_price=main_price
                promo='Not on sale'
            print(sell_price)
            print(promo)
        except:
            continue
    #print(items[0])
    #conn = sqlite3.connect('itemsdb.sqlite')
    #cur = conn.cursor()

    #cur.execute('DROP TABLE IF EXISTS items_table')

    #cur.execute('''
    #CREATE TABLE items_table (item TEXT, price TEXT, promo TEXT)''')
    #for (item, price, promo) in items:
        #print(item)
    #    cur.execute('''INSERT INTO items_table (item, price, promo)
    #            VALUES (?, ?, ?)''', (item, price, promo))
    #conn.commit()

if __name__ == '__main__':
    main()
