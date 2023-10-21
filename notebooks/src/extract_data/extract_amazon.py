import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from tqdm import tqdm

produto = "televisão"

driver = webdriver.Firefox()
driver.get("https://www.amazon.com.br")
time.sleep(0.25)

search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
search_bar.send_keys(produto)

search_button = driver.find_element(By.ID, "nav-search-submit-button")
search_button.click()

time.sleep(2)

last_page = driver.find_element(
    By.XPATH,
    '//span[@class="s-pagination-item s-pagination-disabled"]'
)

last_page = int(last_page.text)

next_page = driver.find_element(
    By.XPATH,
    '//a[@class="s-pagination-item s-pagination-button"]'
)

urls = [driver.current_url, next_page.get_attribute('href')]
for i in range(3, last_page + 1):
    url = urls[1].split('page=')
    url = url[0] + f'page={i}' + url[1][1:]
    url = url.split('ref=')[0] + f'ref=sr_pg_{i}'
    urls.append(url)


for url in tqdm(urls):
    try:
        driver.get(url)
        time.sleep(1)
        products = driver.find_elements(
            By.XPATH,
            '//a[@class="a-link-normal s-underline-text s-underline-link-' \
                'text s-link-style a-text-normal"]'
        )
        products = [product.get_attribute('href') for product in products]
        for product in products:
            try:
                driver.get(product)
                time.sleep(1)
                review_link = driver.find_element(
                    By.XPATH,
                    '//a[@data-hook="see-all-reviews-link-foot"]'
                )
                review_link.click()
                time.sleep(1)
                reviews = []
                for i in range(200):
                    curr_reviews = driver.find_elements(
                            By.XPATH,
                            '//span[@data-hook="review-body"]'
                        )
                    reviews.extend([review.text for review in curr_reviews])
                    try:
                        button = driver.find_element(
                            By.XPATH,
                            '//ul[@class="a-pagination"]/li[@class="a-last"]/a'
                        )
                        button.click()
                        time.sleep(1)
                    except Exception as e:
                        break
                with open('amazon_reviews.txt', 'a') as f:
                    f.write('\n'.join(reviews))
            except Exception as e:
                print(f'Erro ao acessar a página {product}: {e}')
                time.sleep(5)
    except Exception as e:
        print(f'Erro ao acessar a página {url}: {e}')
        time.sleep(5)
