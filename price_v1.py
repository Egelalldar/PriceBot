from random import randint
from time import sleep as pause
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import re
from mysql import take_users_and_urls, take_price
from secrets import secrets

def take_price_on_url(driver):
#    """ Парсит страницу товара по ссылке."""
    url = take_users_and_urls()
    price_list = []
    row_users = secrets['row_users_user']
    row_url = secrets['row_items_url']
    for user_id in url:
        user = str(user_id.get(row_users))
        list2 = user_id[row_url]
        for urls in list2:
            driver.get(urls)
            pause(randint(7, 11))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            price = (soup.find('div', class_="product-buy__price").get_text())
            nums = re.findall(r'\d+', price)
            nums = [int(f) for f in nums]
            nums = ''.join(map(str, nums))
            take_price(nums, user, urls)
            price_list.append(nums)
    return price_list

def main():
    driver = uc.Chrome()
    print(take_price_on_url(driver))

if __name__ == '__main__':
    main()
    print('yee')