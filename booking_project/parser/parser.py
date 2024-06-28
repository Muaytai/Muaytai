import asyncio
import csv
import logging
import random
import time

import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver

# Константы
BOOKING_URL = "https://www.booking.com/"
CITY = "Berlin"
CSV_FILE = "hotels.csv"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0'}


# Функция для получения HTML-кода страницы с помощью Selenium
async def get_page_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск браузера в фоновом режиме
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Имитация поведения пользователя
    random_pause = random.uniform(2, 5)
    time.sleep(random_pause)

    # Скролл страницы
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()
    return html


# Функция для получения HTML-кода страниц с результатами поиска
async def get_search_results_html(pages_count: int) -> list:
    search_results_html = []
    async with aiohttp.ClientSession() as session:
        for page in range(1, pages_count + 1):
            url = BOOKING_URL.format(CITY) + f"&page={page}"
            html = await get_page_html(url)
            search_results_html.append(html)

    return search_results_html


# Функция для извлечения ссылок на страницы отелей
def get_hotel_links(htmls: list) -> list:
    hotel_links = []

    for html in htmls:
        soup = BeautifulSoup(html, "html.parser")
        search_results = soup.find("div", class_="sr_rooms_table_block")
        if search_results:
            hotel_link_elements = search_results.find_all("a", class_="hotel_name_link")
            for link_element in hotel_link_elements:
                hotel_link = link_element.get("href")
                hotel_links.append(hotel_link)
        else:
            logging.warning("Не удалось найти блок с результатами поиска")

    return hotel_links


# Функция для извлечения информации об отелях
def get_hotel_info(hotel_links: list) -> list:
    hotel_info = []
    for link in hotel_links:
        html = get_page_html(link)
        soup = BeautifulSoup(html, "html.parser")

        # Поиск названия отеля
        name_element = soup.find("h2", class_="hp__hotel-name")
        name = name_element.text.strip() if name_element else "Неизвестно"

        # Поиск цены
        price_element = soup.find("span", class_="bui-price-display__value")
        price = price_element.text.strip() if price_element else "Неизвестно"

        # Поиск рейтинга
        rating_element = soup.find("div", class_="hp__hotel-rating")
        rating = rating_element.text.strip() if rating_element else "Неизвестно"

        # Поиск описания
        description_element = soup.find("div", class_="hp_desc_important_facilities")
        description = description_element.text.strip() if description_element else "Неизвестно"

        # Поиск фотографий
        photo_elements = soup.find_all("img", class_="hotel_image")
        photos = [photo.get("src") for photo in photo_elements]

        hotel = {
            "name": name,
            "price": price,
            "rating": rating,
            "description": description,
            "photos": photos
        }

        hotel_info.append(hotel)

    return hotel_info


# Функция для сохранения информации об отелях в CSV-файл
def save_to_csv(hotel_info: list):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "price", "rating", "description", "photos"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for hotel in hotel_info:
            writer.writerow(hotel)

    print(f"Информация об отелях сохранена в файл {CSV_FILE}")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("booking_parser.log"),
            logging.StreamHandler()
        ]
    )

    search_results_html = await get_search_results_html(pages_count=2)
    hotel_links = get_hotel_links(search_results_html)
    hotel_info = get_hotel_info(hotel_links)
    save_to_csv(hotel_info)


if __name__ == "__main__":
    asyncio.run(main())
