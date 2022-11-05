import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import csv


logging.basicConfig(level=logging.INFO)


class Parser:
    def __init__(self,
                 driver_path: str,
                 site_url: str) -> None:
        self.driver_path = driver_path
        self.site_url = site_url

    def write_products_data(self, rows_list: list) -> None:
        '''Записывает данные продукта в csv файл'''
        with open('table.csv',
                  'w',
                  encoding='cp1251',
                  newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ('Product name', 'Price', 'Discount price', 'Link to shop'))
            writer.writerows(rows_list)
            file.close()

        logging.info('Write product data to csv file')

    def parse_names(self, soup: BeautifulSoup) -> list:
        '''Возвращает имена продуктов'''
        page_element = soup.find_all(
            'div', class_='product-snippet_ProductSnippet__name__1ettdy')

        product_name_list = []
        for product_name in page_element:
            product_name_list.append(product_name.text.strip())

        logging.info('Got product names')

        return product_name_list

    def parse_prices(self, soup: BeautifulSoup) -> list:
        '''Возвращает стартовые и скидочные цены продуктов'''
        page_element = soup.find_all(
            'div', class_='product-snippet_ProductSnippet__content__1ettdy')

        price_list = []
        discount_price_list = []
        for element in page_element:
            if element.find('div',
                            class_='snow-price_SnowPrice__secondXS__18x8np'):
                price = element.find(
                    'div',
                    class_='snow-price_SnowPrice__secondXS__18x8np').find(
                        'div',
                        class_='snow-price_SnowPrice__secondPrice__18x8np')
                price_list.append(price.text.strip(' руб.'))
                discount_price = element.find(
                    'div', class_='snow-price_SnowPrice__mainM__18x8np')
                discount_price_list.append(discount_price.text.strip(' руб.'))
            else:
                price = element.find(
                    'div', class_='snow-price_SnowPrice__mainM__18x8np')
                price_list.append(price.text.strip(' руб.'))
                discount_price_list.append('None')

        logging.info('Got product prices')

        return price_list, discount_price_list

    def parse_urls(self, soup: BeautifulSoup) -> list:
        '''Возвращает url продуктов'''
        page_element = soup.find_all(
            'a', class_='product-snippet_ProductSnippet__galleryBlock__1ettdy')

        full_url_list = []
        for url in page_element:
            full_url = 'https://aliexpress.ru' + url.get('href')
            full_url_list.append(full_url.strip())

        logging.info('Got product urls')

        return full_url_list

    def generate_product_data(self) -> list:
        '''Формирует в один список данные продуктов и возвращает его'''
        with open('source-page.html', 'r',
                  encoding='utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'lxml')

        product_name_list = self.parse_names(soup)
        price_list, discount_price_list = self.parse_prices(soup)
        urls_list = self.parse_urls(soup)

        file.close()

        product_data_list = []
        for item in range(len(product_name_list)):
            product_data_list.append(
                (product_name_list[item], price_list[item],
                 discount_price_list[item], urls_list[item]))

        logging.info('Product data is generated')

        return product_data_list

    def get_source_html(self) -> None:
        '''Получает html страницы'''
        driver = webdriver.Chrome(self.driver_path)

        driver.get(self.site_url)

        logging.info('Connected to the site')

        driver.implicitly_wait(3)

        while True:
            if not driver.find_elements(
                    By.CLASS_NAME,
                    'snow-no-search-results_SnowNoSearchResults__button__6qwl68'
            ):
                driver.find_element(By.TAG_NAME,
                                    'body').send_keys(Keys.CONTROL + Keys.END)
                logging.info('Page scrolled')
            else:
                with open('source-page.html', 'w',
                          encoding='utf-8') as file:
                    file.write(driver.page_source)
                    file.close()
                driver.close()
                driver.quit()
                break

        logging.info('Got html page')

    def main(self) -> None:
        try:
            self.get_source_html()
            product_data_list = self.generate_product_data()
            self.write_products_data(product_data_list)

            logging.info('End of work')
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    parser = Parser(
        driver_path=r'chromedriver.exe',
        site_url='https://aliexpress.ru/category/202001195/cellphones.html?brandValueIds=200012332&g=n&page=1&spm='
    )
    parser.main()
