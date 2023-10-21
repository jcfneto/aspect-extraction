import pandas as pd

from pre_processing import reli_parser, convert_aspects, tv_parser
from utils import list_files, read_txt_file


def reli(path: str) -> pd.DataFrame:
    """Pre-processing RELI base data. Generating token-compatible

    Args:
        path: RELI base file path.

    Returns:
        Dataframe with pre-processed data.
    """
    reviews = 0
    data = pd.DataFrame()
    files = list_files(path)
    for path in files:
        author = path.split('-')[-1].split('.')[0]
        file = read_txt_file(path)
        tmp = reli_parser(file)
        tmp.review = tmp.review.apply(lambda x: x[0] + 1)
        tmp.review = tmp.review + reviews
        tmp = convert_aspects(tmp)
        tmp['author'] = author
        data = pd.concat([data, tmp])
        reviews = data.review.max()
    return data


if __name__ == '__main__':

    # Reli
    reli_data = reli(f"datasets/reli")
    reli_data.to_csv('datasets/processed/reli.csv', index=False)

    # Tv
    tv_data = tv_parser('datasets/tv/data.json')
    tv_data.to_csv('datasets/processed/tv.csv', index=False)
