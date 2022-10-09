from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import math
import urllib.request
import time
import math
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from autoscraper import AutoScraper
import pandas as pd

#Set up profile for chrome driver
opp = Options()
opp.add_argument('--profile-directory=Profile 5')
opp.add_argument('user-data-dir=/Users/wwy/Library/Application Support/Google/Chrome')
driver = webdriver.Chrome(executable_path= "/Users/wwy/Downloads/chromedriver",chrome_options= opp)

#Open Grailed
driver.get('https://www.grailed.com/DMC99')
time.sleep(4)

def price_range(low, high):
    #Set Price range, filter out feeds
    price_bottom = driver.find_element(by = By.XPATH, value = '//*[@id="wardrobe"]/div/div[3]/div[2]/div[1]/div/div[6]/div[1]/div')
    price_bottom.click()

    #min
    min_price = driver.find_element(by = By.XPATH, value = '//*[@id="wardrobe"]/div/div[3]/div[2]/div[1]/div/div[6]/div[2]/div/div/div[1]/input')
    #max
    max_price = driver.find_element(by = By.XPATH, value = '//*[@id="wardrobe"]/div/div[3]/div[2]/div[1]/div/div[6]/div[2]/div/div/div[2]/input')

    min_price.send_keys(low)
    max_price.send_keys(high)




price_range(901, 1800)

time.sleep(2)

#Scroll to bottom
SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

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


#get the total number of feeds
feeds = driver.find_elements_by_xpath('//*[@id="wardrobe"]/div/div[3]/div[2]/div[2]/div/div')
feed_num = len(feeds)

print('++++++++++++++++++++++++++')
print('Total {} listings found'.format(feed_num))
print('++++++++++++++++++++++++++')

def lts(s):
       
    # initialize an empty string
    str1 = " "
   
    # return string 
    return (str1.join(s))

def openitem(xpath):
    item =  driver.find_element(by = By.XPATH, value = xpath)
    url = item.get_attribute('href')
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window('secondtab')
    driver.get(url)


def info():

    #Image div
    imgdiv = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[1]/div/section/div[2]/div/div')

    num = len(imgdiv)
    print('++++++++++++++++++++++++')
    print('total of {} images found'.format(num))

    srcs = []
    for i in range(num):
            imgpath = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[1]/div/section/div[2]/div/div[{}]/div/img'.format(i+1))
            src = imgpath.get_attribute('src')
            print(src)
            srcs.append(src)
            nextbutton = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[1]/div/section/div[4]/button')
            nextbutton.click()
            time.sleep(1)
            


    #Handle and Title

    title_path = driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[2]')

    title = str(title_path.text)
    print(title)

    handle = title.lower().replace(' ','-')
    print(handle)

    #Vendor

    vendor_path = driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[1]/a')

    vendor = str(vendor_path.text)
    print(vendor)

    #Type
    cat_path =  driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/nav/ol/li[3]/a')

    Custom_Product_Type = str(cat_path.text)


    Custom_Product_Type = Custom_Product_Type.replace('{}'.format(vendor), '')

    print(Custom_Product_Type)


    #Option1_Name: Size

    Option1_Name = 'Size'

    size_path = driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[3]')

    Option1_Value = str(size_path.text)

    all_words = Option1_Value.split()

    Option1_Value = lts(all_words[1:])

    print(Option1_Value)

    #Option2_Name: Color
    Option2_Name = 'Color'

    color_path =  driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[4]')

    Option2_Value = str(color_path.text)

    all_words = Option2_Value.split()

    Option2_Value = lts(all_words[1:])

    print(Option2_Value)

    #Option3_Name: Condition

    Option3_Name = 'Condition'

    condition_path = driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[5]')

    Option3_Value = str(condition_path.text)

    all_words = Option3_Value.split()

    Option3_Value = lts(all_words[1:])

    print(Option3_Value)

    #Variant Price

    price_path = driver.find_element(by = By.XPATH, value = '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[3]/span')

    Variant_Price = str(price_path.text).replace('$', '')

    Variant_Price = int(int(Variant_Price)*0.93)

    print(Variant_Price)
    print('++++++++++++++++++++++++++')


    #CSVi

    df = pd.read_csv('/Users/wwy/Desktop/gproject/gproduct.csv', index_col='Handle')
    #remoce body html
    df.loc[0,'Body (HTML)'] = None


    #Upload handle and pictures
    for i in range(num):

        df.loc[i,'Handle'] = handle

        df.loc[i,'Image Src'] = srcs[i]

        df.loc[i,'Image Position'] = int(i+1)


    #ELSE

    df.loc[0,'Published'] = 'TRUE'
    df.loc[0,'Variant Grams'] = '0.0'
    df.loc[0,'Variant Inventory Tracker'] = 'shopify'
    df.loc[0,'Variant Inventory Qty'] = '1'
    df.loc[0,'Variant Inventory Policy'] = 'deny'
    df.loc[0,'Variant Fulfillment Service'] = 'manual'
    df.loc[0,'Variant Requires Shipping'] = 'TRUE'
    df.loc[0,'Variant Taxable'] = 'FALSE'
    df.loc[0,'Gift Card'] = 'FALSE'
    df.loc[0,'Variant Weight Unit'] = 'lb'
    df.loc[0,'Status'] = 'active'


    #Title

    df.loc[0,'Title'] = title

    #Vendor

    df.loc[0,'Vendor'] = vendor

    #Custom Product Type

    df.loc[0,'Type'] = Custom_Product_Type

    #Options

    df.loc[0,'Option1 Name'] = Option1_Name
    df.loc[0,'Option1 Value'] = Option1_Value

    df.loc[0,'Option2 Name'] = Option2_Name
    df.loc[0,'Option2 Value'] = Option2_Value

    df.loc[0,'Option3 Name'] = Option3_Name
    df.loc[0,'Option3 Value'] = Option3_Value

    #Variant Price

    df.loc[0,'Variant Price'] = Variant_Price

    #ser handle as index
    df = df.set_index('Handle')


    #old csv
    old_df = pd.read_csv('/Users/wwy/Desktop/gproject/gtest.csv',index_col='Handle')

    frames = [old_df,df]
  
    result = pd.concat(frames)

    result = result[result.index.notnull()]
    result.to_csv(path_or_buf = '/Users/wwy/Desktop/gproject/gtest.csv')





for i in range(feed_num):
    print('++++++++++Now Handling Number {}/{}++++++++'.format(i,feed_num))
    item_xpath = ('//*[@id="wardrobe"]/div/div[3]/div[2]/div[2]/div/div[{}]/a[1]'.format(i+1))
    #open the item info page
    openitem(item_xpath)
    time.sleep(3)
    #get info
    info()
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print('++++++++++Number {}/{} Extraction Completed++++++++'.format(i,feed_num))
    








