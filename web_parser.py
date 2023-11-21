from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions  import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


COOKIE_BTN_XPATH = '/html/body/div[3]/div/div[1]/div/div[2]/div/div[2]/div[2]/button'
TITLE_XPATH = '//*[@id="pdp_product_title"]'
SUBTITLE_XPATH = '/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/h2'
COLOR_XPATH = '/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div[2]/div/div/span/div/div/ul/li[1]'
STYLE_XPATH = '//*[@id="RightRail"]/div/span/div/div/ul/li[2]'
DESCRIPTION_XPATH = '//*[@id="RightRail"]/div/span/div/div/p'
PRICE_XPATH = '//*[@id="RightRail"]/div/div[1]/div/div[2]/div/div/div/div/div'
SIZES_GRID_XPATH = '//*[@id="buyTools"]/div[1]/fieldset/div'
IMG_CONTAINER_XPATH = '//*[@id="pdp-6-up"]'

class WebParser():
    def run(self, url):
        options = ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        url_load_timeout = 2

        #загрузка страницы
        driver.get(url)

        #пауза для ожидания полной загрузки страницы
        time.sleep(self.url_load_timeout)

        #принятие куки
        print('accepting cookies...')
        try:
            cookie_btn = driver.find_element(By.XPATH, COOKIE_BTN_XPATH)
            cookie_btn.click()
            print('cookie accept successful')

        except WebDriverException:
            print('cookie accept fail')

        product = {}

        # получение наименования
        product['title'] = driver.find_element(By.XPATH, TITLE_XPATH).get_attribute('innerHTML')

        # получение типа
        product['subtitle'] = driver.find_element(By.XPATH, SUBTITLE_XPATH).get_attribute('innerHTML')

        # получение бренда
        product['vendor'] = product['title'].split()[0]

        # получение цвета
        c = driver.find_element(By.XPATH, COLOR_XPATH).get_attribute('innerHTML')
        product['color'] = c[c.find(':') + 2:]

        # получение стиля
        s = driver.find_element(By.XPATH, STYLE_XPATH).get_attribute('innerHTML')
        product['style'] = s[s.find(':') + 2:]

        # получение описания
        product['description'] = driver.find_element(By.XPATH, DESCRIPTION_XPATH).get_attribute('innerHTML')

        # получение цены
        product['price'] = driver.find_element(By.XPATH, PRICE_XPATH).get_attribute('innerHTML').replace(',', '').replace('฿','')

        # получение доступных размеров
        sizes = []
        for sizes_cell in driver.find_element(By.XPATH, SIZES_GRID_XPATH).find_elements(By.TAG_NAME, 'div'):
            if sizes_cell.find_element(By.TAG_NAME, 'input').get_attribute('disabled') is None:
                sizes.append(sizes_cell.find_element(By.TAG_NAME, 'label').get_attribute('innerHTML'))
        product['sizes'] = sizes

        # получение ссылок на фото
        img_container = driver.find_element(By.XPATH, IMG_CONTAINER_XPATH)
        imgs = img_container.find_elements(By.TAG_NAME, 'img')
        photo_links = []
        for img in imgs:
            photo_links.append(img.get_attribute('src'))
        product['photo_links'] = photo_links

        driver.quit()
        return product
