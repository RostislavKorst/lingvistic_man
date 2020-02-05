import collections
import re

import numpy as np

TOKEN_RE = re.compile(r'[\w]+')
""" TOKENIZE_RE = re.compile(r'[а-яА-ЯёЁ]+|-?\d*[.,]?\d+|\S', re.I) """

def tokenize_text_simple_regex(txt, min_token_size=4):
    txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_token_size]


def tokenize_corpus(texts, tokenizer=tokenize_text_simple_regex, **tokenizer_kwargs):
    return [tokenizer(text, **tokenizer_kwargs) for text in texts]


def build_vocabulary(tokenized_texts, max_size=1000000, max_doc_freq=0.8, min_count=5, pad_word=None):
    word_counts = collections.defaultdict(int)
    # количество документов, в которых встречается данное слово
    doc_n = 0

    # посчитать количество документов, в которых употребляется каждое слово
    # а также общее количество документов
    for txt in tokenized_texts:
        doc_n += 1
        unique_text_tokens = set(txt)
        for token in unique_text_tokens:
            word_counts[token] += 1

    # убрать слишком редкие и слишком частые слова
    word_counts = {word: cnt for word, cnt in word_counts.items()
                   if cnt >= min_count and cnt / doc_n <= max_doc_freq}

    # отсортировать слова по убыванию частоты
    sorted_word_counts = sorted(word_counts.items(),
                                key=lambda pair: (pair[1], pair[0]))

    # добавим несуществующее слово с индексом 0 для удобства пакетной обработки
    if pad_word is not None:
        sorted_word_counts = [(pad_word, 0)] + sorted_word_counts

    # если у нас по прежнему слишком много слов, оставить только max_size самых частотных
    if len(word_counts) > max_size:
        sorted_word_counts = sorted_word_counts[:max_size]

    # нумеруем слова
    word2id = {word: i for i, (word, _) in enumerate(sorted_word_counts)}

    # нормируем частоты слов
    word2freq = np.array([cnt / doc_n for _, cnt in sorted_word_counts], dtype='float32')

    return word2id, word2freq


"""
Казнить нельзя, помиловать. Нельзя наказывать.

Казнить, нельзя помиловать. Нельзя освободить.

Нельзя не помиловать.

Обязательно освободить.
"""

text = ["азбука Казнить нельзя, помиловать. Нельзя наказывать ясельки.", "Казнить, нельзя помиловать ясельки. Нельзя освободить.", "Нельзя не помиловать ясельки.", "Обязательно освободить."]

tokenized_list_of_docs = tokenize_corpus(text, min_token_size=1)

# print(tokenized_list_of_docs)

word_id = build_vocabulary(tokenized_list_of_docs, max_doc_freq=1, min_count=1)
print(word_id)
# уже отсортировано по алфавиту и по частоте
word_id = list(zip(list(word_id[0].keys()), list(word_id[1])))
print(word_id)
word_id = sorted(word_id, key=lambda x: (x[1], x[0]))
print(word_id)

print(' '.join(list(map(lambda x: x[0], word_id))))
print(' '.join(list(map(lambda x: str(x[1]), word_id))))
"""print(' '.join(list(word_id[0].keys())))
print(list(word_id[1]))
a = list(word_id[1])
a = list(map(lambda x: str(x), a))
print(' '.join(a))"""
