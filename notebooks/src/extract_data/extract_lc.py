import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm


if __name__ == '__main__':

    URL = 'http://leitorcompulsivo.com.br/resenhas-de-livros/'

    driver = webdriver.Firefox()
    driver.get(URL)

    for _ in tqdm(range(10_000)):
        driver.execute_script('window.scrollBy(0, 1000)')
        time.sleep(0.25)

    links = driver.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in links]
    links =set([link for link in links if 'resenha-' in link])

    names_links = []
    for link in links:
        name = link.split('resenha-')[1].split('/')[0].replace('-', '_')
        names_links.append((name, link))

    for book_title, link in tqdm(names_links):
        try:
            driver.get(link)
            time.sleep(0.25)
            content = driver.find_element(By.CLASS_NAME, 'td-post-content')
            ps = content.find_elements(By.TAG_NAME, 'p')

            review = ''
            for p in ps[1:]:
                if 'Compre na Amazon' in p.text:
                    break
                review += f' {p.text}'
            review = review.replace(' Opinião: ', '')

            with open(
                    f'../../../corpus/leitor_compulsivo/{book_title}.txt',
                    'w'
            ) as f:
                f.write(review)

        except Exception as e:
            print(e)
            print(book_title, link)
