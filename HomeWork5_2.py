#  Написать программу, которая собирает товары «В тренде»
#  с сайта техники mvideo и складывает данные в БД.


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
from pymongo import MongoClient

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)

driver.get('https://www.mvideo.ru/')

assert "М.Видео" in driver.title
while True:  #листаем вниз пока не появится кнопка "В тренде"
    ActionChains(driver).scroll_by_amount(0, 500).perform() # scroll_by_amount(delta_x, delta_y)
    sleep(3)
    try:
        button = driver.find_element(By.XPATH, '//button[@class="tab-button ng-star-inserted"]')
        break
    except NoSuchElementException as e:
        pass
button.click()   # переходим на тренды

# получаем из тредов в списки names и prices
carusel = driver.find_element(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]')
names = carusel.find_elements(By.CLASS_NAME, 'product-mini-card__name')
prices = carusel.find_elements(By.CLASS_NAME, 'product-mini-card__price')

# подключаемя с mongodb
mongo_address = 'mongodb://localhost:27017'
client = MongoClient(mongo_address)
db = client.mvideo
collect_trend = db.trend

# пробегаемя по спискам с данными и заносим наименование продукат, цену, ссылку, и дату занесения в БД.
for i in range(len(names)):
    dat = {}
    dat['name'] = names[i].text
    main_price = prices[i].find_element(By.CLASS_NAME, 'price__main-value')
    dat['price'] = int(''.join(main_price.text.split()[:-1]))
    dat['link'] = names[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
    dat['date'] = datetime.now().strftime('%Y.%d.%m %H:%M:%S')
    collect_trend.insert_one(dat)

driver.close()
