import pandas as pd

from collections import defaultdict
from utils import json_to_dataframe, split


def tv_parser(path: str) -> pd.DataFrame:
    """Pre-processing TV base data. Generating token-compatible
    sequences with aspects.

    Args:
        path: TV base file path.

    Returns:
        Dataset with pre-processed data.
    """
    df = json_to_dataframe(path)
    data = {'tokens': [], 'aspect_tags': []}
    for idx, row in df.iterrows():
        tokens = split(row.tokens)
        labels = [0] * len(tokens)
        for start, end in row['explicit aspects positions']:
            for i in range(end - start):
                tag = 1 if i == 0 else 2
                labels[start + i] = tag
        data['tokens'].append(tokens)
        data['aspect_tags'].append(labels)
    df['tokens'] = data['tokens']
    df['aspect_tags'] = data['aspect_tags']
    return df


def extract_tokens_and_aspects(data: pd.DataFrame) -> pd.DataFrame:
    """Extracts tokens and aspects from the dataset.

    Args:
        data: Dataframe with reviews.

    Returns:
        Dataframe with tokens and aspects.
    """
    review = 0
    tokens_aspects = []
    for _, row in data.iterrows():
        review += 1
        for sentences in row['phrases']:
            curr_tokens = []
            curr_aspects = []
            for word in sentences['words']:
                curr_tokens.append(word['plain'])
            for aspect in sentences['aspects']:
                curr_aspects.append(aspect['index'])
            tokens_aspects.append((
                curr_tokens, curr_aspects, review, row['author']
            ))
    return pd.DataFrame(
        tokens_aspects,
        columns=['tokens', 'aspect_tags', 'review', 'author'])


def reli_parser(file: list) -> pd.DataFrame:
    """Parses the data from the RELI dataset.

    Args:
        file: RELI dataset file.

    Returns:
        Dataframe with the parsed data.
    """
    i = 0
    reviews = []
    review_number = 0
    while i < len(file):
        if file[i].startswith('#Título_'):
            j = i + 1
            sentence = defaultdict(list)
            features = ('tokens',
                        'pos',
                        'aspect_tags',
                        'opinion',
                        'polarity',
                        'help')
            while j < len(file) and not file[j].startswith('#Título_'):
                if (len(file[j]) > 0) & (not file[j].startswith('#')):
                    splited_line = file[j].split('\t')
                    for k in range(len(features)):
                        sentence[features[k]].append(splited_line[k])
                elif (len(file[j]) == 0) and (len(sentence) > 0):
                    sentence['review'].append(review_number)
                    reviews.append(sentence)
                    sentence = defaultdict(list)
                j += 1
            review_number += 1
        i += 1
    return pd.DataFrame(reviews)


def convert_aspects(data: pd.DataFrame) -> pd.DataFrame:
    """Converts the aspects from the RELI dataset from string to numbers.

    Args:
        data: Dataframe with the RELI dataset.

    Returns:
        Dataframe with the converted aspects.
    """
    aspects = []
    for i, r in data.iterrows():
        curr_aspects = r['aspect_tags']
        new_aspect = [0] * len(curr_aspects)
        last = ''
        for j in range(len(curr_aspects)):
            if curr_aspects[j].startswith('OBJ'):
                new_aspect[j] = 1 if curr_aspects[j] != last else 2
            last = curr_aspects[j]
        aspects.append(new_aspect)
    data['aspect_tags'] = aspects
    return data
