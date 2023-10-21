import re
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode


class TitleParser:
    """Parse the title of the book from the HTML page."""

    def _get_book_title(self, text: str) -> str:
        """Extract the book title from the text of the page."""
        match = re.search(r'^.*?(?=[\u2014\u2013-])', text)
        if match:
            text = match.group(0)
        return text

    def _text_normalizer(self, text: str) -> str:
        """Normalize the text of the page."""
        return unidecode(text[:-1]).lower().replace(' ', '_')

    def _remove_punctuation(self, text: str) -> str:
        """Remove special characters from the text."""
        text = re.sub(r'[\(\)\#\,\:\.]', '', text)
        return text

    def get_title(self, text) -> str:
        """Get the title of the book from the url."""
        title = self._get_book_title(text)
        title = self._text_normalizer(title)
        return  self._remove_punctuation(title)


if __name__ == '__main__':

    # Paths
    ROOT = '../../../corpus'
    URL = 'https://www.minhavidaliteraria.com.br/por-titulo/'

    # Get the HTML page
    curr_page = requests.get(URL)
    soup = BeautifulSoup(curr_page.text, 'html.parser')
    article = soup.find('article')
    lis = article.find_all('li')

    # Get the title of the book and the url
    links = []
    title_parser = TitleParser()
    for li in lis:
        links.append((
            title_parser.get_title(li.text),
            li.a['href']
        ))

    print('Number of books:', len(links))

    for book_title, link in tqdm(links):
        try:

            # Get the page
            cur_page = requests.get(link)
            soup = BeautifulSoup(cur_page.text, 'html.parser')

            # Get the review
            article = soup.find('article')

            # Remove unnecessary tags
            for remove in ('blockquote', 'div'):
                for tag in article.find_all(remove):
                    tag.decompose()

            # Save the review
            with open(
                    f'{ROOT}/minha_vida_literaria/{book_title}.txt',
                    'w'
            ) as f:
                f.write(article.text)

        except Exception as e:
            print(e)