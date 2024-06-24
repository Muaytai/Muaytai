import requests

cookies = {
    '_gcl_au': '1.1.1890987681.1718542551',
    'language_id': 'ru',
    '_me_': 'b8zAhIw5twW75ak%2Br5WhQA',
    'tmr_lvid': 'dba1d2cddd1bfebdba1c907f38c5cd53',
    'tmr_lvidTS': '1718542550795',
    'PHPSESSID': 'c550acbf53db0f2f9c4a36258a045181',
    '_ym_uid': '1718542551412277700',
    '_ym_d': '1718542551',
    '_ym_isad': '2',
    '_ia_': '0',
    'select_guests': '%7B%22guests%22%3A%7B%22adults%22%3A2%2C%22childrens%22%3A%5B%5D%2C%22pets%22%3A%7B%22value%22%3Afalse%2C%22description%22%3A%22%22%7D%7D%7D',
    '_gid': 'GA1.2.269523282.1718542847',
    '_ym_visorc': 'b',
    'route': '1718545065.42.38.871634|cb1faa23db9e30603aef3c84465716e1',
    'domain_sid': '5D_WiwkAQZUXuCA2Za51K%3A1718545066984',
    'x-request-id': 'ea1950566aca47ba334a9e4435900895',
    'rid': 'ea1950566aca47ba334a9e4435900895',
    'calendar_dates': '%7B%22date_begin%22%3A%222024-06-27%22%2C%22date_end%22%3A%222024-06-28%22%7D',
    '_ga': 'GA1.2.1531301004.1718542551',
    '_gat_gtag_UA_2178778_2': '1',
    '_ga_B0K4L0V6J8': 'GS1.1.1718544849.2.1.1718546764.51.0.0',
    'cf_clearance': 'yh3jEdCOkbMhajUUuaiFZEacXMuHGSYwRYrPcxtBz3E-1718546764-1.0.1.1-c09z3ByaRE7zPTPFGyNrzXLk7RlxsGtjfRQEcWofN2X2S6Z8J3gkGOa9JtJl1SyXywG3yeOCOc9xvgMk9uodPg',
    'tmr_detect': '0%7C1718546766760',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_gcl_au=1.1.1890987681.1718542551; language_id=ru; _me_=b8zAhIw5twW75ak%2Br5WhQA; tmr_lvid=dba1d2cddd1bfebdba1c907f38c5cd53; tmr_lvidTS=1718542550795; PHPSESSID=c550acbf53db0f2f9c4a36258a045181; _ym_uid=1718542551412277700; _ym_d=1718542551; _ym_isad=2; _ia_=0; select_guests=%7B%22guests%22%3A%7B%22adults%22%3A2%2C%22childrens%22%3A%5B%5D%2C%22pets%22%3A%7B%22value%22%3Afalse%2C%22description%22%3A%22%22%7D%7D%7D; _gid=GA1.2.269523282.1718542847; _ym_visorc=b; route=1718545065.42.38.871634|cb1faa23db9e30603aef3c84465716e1; domain_sid=5D_WiwkAQZUXuCA2Za51K%3A1718545066984; x-request-id=ea1950566aca47ba334a9e4435900895; rid=ea1950566aca47ba334a9e4435900895; calendar_dates=%7B%22date_begin%22%3A%222024-06-27%22%2C%22date_end%22%3A%222024-06-28%22%7D; _ga=GA1.2.1531301004.1718542551; _gat_gtag_UA_2178778_2=1; _ga_B0K4L0V6J8=GS1.1.1718544849.2.1.1718546764.51.0.0; cf_clearance=yh3jEdCOkbMhajUUuaiFZEacXMuHGSYwRYrPcxtBz3E-1718546764-1.0.1.1-c09z3ByaRE7zPTPFGyNrzXLk7RlxsGtjfRQEcWofN2X2S6Z8J3gkGOa9JtJl1SyXywG3yeOCOc9xvgMk9uodPg; tmr_detect=0%7C1718546766760',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

params = {
    'from': 'mainpage',
}

response = requests.get('https://www.sutochno.ru/', params=params, cookies=cookies, headers=headers)
with open('result.html', 'w', encoding="utf-8") as file:
    file.write(response.text)
