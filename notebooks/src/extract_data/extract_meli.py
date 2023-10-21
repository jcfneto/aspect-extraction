import os
import re
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from tqdm import tqdm

produto = "tv smart"

driver = webdriver.Firefox()
driver.get("https://www.mercadolivre.com.br/")
time.sleep(0.25)

search_bar = driver.find_element(By.ID, "cb1-edit")
search_bar.clear()
search_bar.send_keys(produto)
search_bar.send_keys(Keys.RETURN)
time.sleep(2)

css = '.andes-pagination__link.shops__pagination-link.ui-search-link'
next_page = driver.find_element(By.CSS_SELECTOR, css)
urls = [next_page.get_attribute('href')]

for i in range(40):
    re_pattern = re.search(r'_Desde_(\d+)', urls[-1])
    new_numbet = int(re_pattern.group(1)) + 48
    new_url = re.sub(r'_Desde_(\d+)', f'_Desde_{new_numbet}', urls[-1])
    urls.append(new_url)

for url in tqdm(urls):

    try:
        body = requests.get(url).text
        soup = BeautifulSoup(body, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'smart-tv' in href:
                links.append(href)

        links = list(set(links))
        for link in links[1:]:

            try:
                driver.get(link)
                time.sleep(2)

                esc = driver.find_element(By.TAG_NAME, 'body')
                esc.send_keys(Keys.ESCAPE)                

                try:
                    cookie_css = "button.cookie-consent-banner-opt-" \
                        "out__action:nth-child(2)"
                    cookie = driver.find_element(
                        By.CSS_SELECTOR,
                        cookie_css
                    )
                    cookie.click()
                    time.sleep(2)

                    cookie = driver.find_element(
                        By.CSS_SELECTOR,
                        ".cookie-consent-banner-opt-out__action"
                    )
                    cookie.click()
                    time.sleep(2)
                    print('Cookie aceito')
                except:
                    time.sleep(2)

                button = driver.find_element(
                    By.CSS_SELECTOR,
                    '[data-testid="see-more"]'
                )
                button.click()
                time.sleep(2)

                reviews_div = driver.find_element(
                    By.CLASS_NAME,
                    'infinite-scroll-component'
                )

                reviews_div = reviews_div.find_elements(By.TAG_NAME, 'p')
                reviews = [
                    review.text
                    for review in reviews_div
                    if not review.text.isnumeric()
                ]

                output_filename = 'meli_tv_reviews.txt'
                if not os.path.exists(output_filename):
                    with open(output_filename, 'w') as f:
                        f.write('')

                with open(output_filename, 'a') as f:
                    f.write('\n'.join(reviews))

                time.sleep(2)

            except Exception as e:
                print(f'Erro ao acessar a página {link}: {e}')

    except Exception as e:
        print(f'Erro ao acessar a página: {e}')
