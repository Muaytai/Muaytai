import requests

cookies = {
    'language_id': 'ru',
    '_ga': 'GA1.1.727336349.1719149264',
    '_gcl_au': '1.1.378220593.1719149264',
    '_ym_uid': '1719149266992563231',
    '_ym_d': '1719149266',
    'PHPSESSID': 'af6962f1bd08e310a1fcc1781706481d',
    '_me_': 'b8zAhIw5twW75ak%2Br5WhQA',
    '_ia_': '0',
    'cf_clearance': 'MlHJD5xtLvZozkmQURHLgRM7NXOXKOaPt_I_b.oXvz8-1719499766-1.0.1.1-NfkiMrAJDxwCFPnVLbz9L5MOpL9EpmOGCzqmXAkUcQQGwUOQhroGQvRlv4V.agOJwMJrTeqdg268N3cayHyijA',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_gcl_aw': 'GCL.1719499789.CjwKCAjwm_SzBhAsEiwAXE2Cv9FvkGo1Jd5mWaHuFKCzgQ6nGEynrU6WW86qat7jQVpR1nvJrk-MERoCtKEQAvD_BwE',
    '_gcl_gs': '2.1.k1$i1719499783',
    'x-request-id': '759b1616bbc743c3448a03a7aa5c4242',
    'rid': '759b1616bbc743c3448a03a7aa5c4242',
    '_ga_B0K4L0V6J8': 'GS1.1.1719499764.3.1.1719499850.59.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'language_id=ru; _ga=GA1.1.727336349.1719149264; _gcl_au=1.1.378220593.1719149264; _ym_uid=1719149266992563231; _ym_d=1719149266; PHPSESSID=af6962f1bd08e310a1fcc1781706481d; _me_=b8zAhIw5twW75ak%2Br5WhQA; _ia_=0; cf_clearance=MlHJD5xtLvZozkmQURHLgRM7NXOXKOaPt_I_b.oXvz8-1719499766-1.0.1.1-NfkiMrAJDxwCFPnVLbz9L5MOpL9EpmOGCzqmXAkUcQQGwUOQhroGQvRlv4V.agOJwMJrTeqdg268N3cayHyijA; _ym_isad=2; _ym_visorc=b; _gcl_aw=GCL.1719499789.CjwKCAjwm_SzBhAsEiwAXE2Cv9FvkGo1Jd5mWaHuFKCzgQ6nGEynrU6WW86qat7jQVpR1nvJrk-MERoCtKEQAvD_BwE; _gcl_gs=2.1.k1$i1719499783; x-request-id=759b1616bbc743c3448a03a7aa5c4242; rid=759b1616bbc743c3448a03a7aa5c4242; _ga_B0K4L0V6J8=GS1.1.1719499764.3.1.1719499850.59.0.0',
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

response = requests.get('https://sutochno.ru/votes', cookies=cookies, headers=headers)

with open('../frontend/src/pages/ReviewsPage.js', 'w', encoding="utf-8") as file:
    file.write(response.text)
