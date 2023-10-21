# TV

Este conjunto de dados foi coletado e anotado pelos autores do trabalho 
(CARDOSO; PEREIRA, 2020) e contém revisões de usuários sobre um modelo de 
televisão. O conjunto conta com marcações dos aspectos explícitos e implícitos,
bem como as marcações de opinião referente a estes aspectos. A seguir, um 
exemplo de revisão presente no conjunto:

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

Ao todo, o conjunto conta com 1.091 revisões, 989 destas com pelo menos um 
aspecto explícito.

# ReLi

O ReLi (Freitas et al., 2012) é um conjunto de dados de resenhas de livros de 7
autores diferentes. Além das marcações de aspectos, o conjunto conta com as 
informações de POS (Part of Speech), opinião e polaridade. A seguir, um exemplo
de revisão presente no conjunto:

```json
        {
            "word": "[Um, livro, muito, bom, que, retrata, a, cruel, realidade, de, os, garotos, de, rua, de, a, Bahia, de, a, década, de, 30, .]",
            "pos": "[ART, N, ADV, ADJ, PRO-KS-REL, V, ART, ADJ, N, PREP, ART, N, PREP, N, PREP, ART, NPROP, PREP, ART, N, PREP, N, .]",
            "object": "[O, OBJ00, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]",
            "opinion": "[O, O, O, op00+, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O]",  
            "polarity": "[+, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +, +]"
        }
```

Ao todo, o conjunto conta co 1.600 resenhas e 12.470 sentenças.

# Processed

As revisões do conjunto foram pré-processadas para o formato ideal de entrada
para os modelos de linguagem.

O atributo `aspect_tags` a seguir corresponde ao padrão IOB2. A seguir a 
correspondência:

```python
tag_to_id = {
        "O": 0, # Outside
        "B": 1, # Begin
        "I": 2  # Inside
}
```

##### TV

As revisões do conjunto TV ficaram com o seguinte formato:

```json
        {
            "tokens": ["imagem", "ótima", "recursos", "de", "web", "bons", ",", "recomendo", "não", "vai", "se", "arrepender"],
            "aspect_tags": [1, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0]
        }
```


##### ReLi

Análogo ao conjunto TV, as revisões do conjunto ReLi ficaram com o seguinte
formato:

```json
        {
            "tokens": ["um", "livro", "muito", "bom", "que", "retrata", "a", "cruel", "realidade", "de", "os", "garotos", "de", "rua", "de", "a", "bahia", "de", "a", "década", "de", "30", "."],
            "aspect_tags": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
```

# Statified

Os conjuntos foram divididos em 10 folds, buscando manter a proporção do 
conjunto de dados originais. As estatísticas de cada um dos conjuntos podem ser
vistas no diretório `notebooks/data_stats`.

No caso do `TV`, cada registro trata-se de uma revisão, no caso do `ReLi` cada 
registro é umas sentença de uma resenha, por conta disso, as sentenças de uma
mesma resenha se encontram em um mesmo fold.

No `ReLi` existiam sentenças com apenas um único token com os seguintes
caracteres `{'"', ')', '*', '.', '3', '>', '?', ']', 'x'}`. Estes foram 
removidos do conjunto. Portanto, das métricas originais, ficamos com 1.598
resenhas e 12.429 sentenças.
