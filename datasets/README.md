# TV

This dataset was collected and annotated by the authors of the work (CARDOSO; PEREIRA, 2020) and contains user reviews about a TV model. The dataset includes explicit and implicit aspects and opinion markings regarding these aspects. Below is an example of a review present in the dataset:

```json
        {
            "review": "Imagem ótima recursos de web bons , recomendo não vai se arrepender",
            "tokens": "[Imagem, ótima, recursos, de, web, bons, ,, recomendo, não, vai, se, arrepender]",
            "explicit aspects": ["imagem", "recursos de web"],
            "explicit opinion": ["ótima", "bons"],
            "implicit aspects": ["produto"],
            "implicit opinion": ["recomendo"],
            "is_suggestion": "",
            "explicit aspects positions": [[0, 1], [2, 5]],
            "explicit opinion positions": [[1, 2], [5, 6]]
        }
```

The dataset contains 1,091 reviews, 989 of which have at least one explicit aspect.


# ReLi

The ReLi (Freitas et al., 2012) is a dataset of book reviews from 7 different authors. In addition to aspect markings, the dataset includes POS (Part of Speech) information, opinion, and polarity. Below is an example of a review present in the dataset:

```json
        {
            "word": "[Um, livro, muito, bom, que, retrata, a, cruel, realidade, de, os, garotos, de, rua, de, a, Bahia, de, a, década, de, 30, .]",
            "pos": "[ART, N, ADV, ADJ, PRO-KS-REL, V, ART, ADJ, N, PREP, ART, N, PREP, N, PREP, ART, NPROP, PREP, ART, N, PREP, N, .]",
            "object": "[O, OBJ00, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]",
            "opinion": "[O, O, O, op00+, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]",  
            "polarity": "[+, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +]"
        }
```

In total, the dataset contains 1,600 reviews and 12,470 sentences.

# Processed

The reviews in the dataset have been pre-processed into the ideal input format for language models.

The `aspect_tags` attribute corresponds to the IOB2 pattern. The mapping is as follows:

```python
tag_to_id = {
        "O": 0, # Outside
        "B": 1, # Begin
        "I": 2  # Inside
}
```

##### TV

The reviews in the TV dataset are formatted as follows:

```json
        {
            "tokens": ["imagem", "ótima", "recursos", "de", "web", "bons", ",", "recomendo", "não", "vai", "se", "arrepender"],
            "aspect_tags": [1, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0]
        }
```


##### ReLi

Similar to the TV dataset, the reviews in the ReLi dataset are formatted as follows:

```json
        {
            "tokens": ["um", "livro", "muito", "bom", "que", "retrata", "a", "cruel", "realidade", "de", "os", "garotos", "de", "rua", "de", "a", "bahia", "de", "a", "década", "de", "30", "."],
            "aspect_tags": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
```

# Statified

The datasets have been divided into 10 folds, maintaining the proportion of the original datasets. The statistics of each set can be found in the `notebooks/data_stats` directory.

In the case of the `TV` dataset, each record is a review, whereas in the ReLi dataset, each record is a sentence from a review. Thus, the sentences from the same review are found in the same fold.

In the ReLi dataset, there were sentences with only a single token consisting of the following characters: `{'"', ')', '*', '.', '3', '>', '?', ']', 'x'}`. These were removed from the dataset. Therefore, from the original metrics, we are left with 1,598 reviews and 12,429 sentences.
