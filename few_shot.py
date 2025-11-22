import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Dict, List
from transformers import AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from custom_prompt import USER_PROMPT


SOLAR_PRO_TOKENIZER = AutoTokenizer.from_pretrained(
    "upstage/solar-pro2-tokenizer", 
    dtype="auto"
)

TRAIN_DF = pd.read_csv("./data/train_dataset.csv")
TOKENIZED_ORIGINAL_SENTENCES = [SOLAR_PRO_TOKENIZER.encode(sent, add_special_tokens=False)
                           for sent in TRAIN_DF["original_sentence"].array]


def construct_fewshot(dataset, tokenized_sentences, text, topk=10, chat_fewshot=True):
    tokenized_text = SOLAR_PRO_TOKENIZER.encode(text, add_special_tokens=False)
    sentences = [tokenized_text] + tokenized_sentences

    vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False, token_pattern=None)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    topk_idxs = np.argsort(similarity[0])[::-1][:topk]
    fewshot = [(dataset.iloc[idx]["original_sentence"], dataset.iloc[idx]["answer_sentence"]) for idx in topk_idxs]
    if chat_fewshot:
        chat_fewshot = []
        for user_sentence, assistant_sentence in fewshot:
            chat_fewshot.append({"role": "user", "content": USER_PROMPT.format(text=user_sentence)})
            chat_fewshot.append({"role": "assistant", "content": assistant_sentence})
        fewshot = chat_fewshot
    return fewshot


def random_fewshot(dataset, topk=10, seed=None, chat_fewshot=True):
    if seed is not None:
        np.random.seed(seed)
    rand_idxs = np.random.choice(len(dataset), size=topk)
    fewshot = [(dataset.iloc[idx]["err_sentence"], dataset.iloc[idx]["cor_sentence"]) for idx in rand_idxs]
    if chat_fewshot:
        chat_fewshot = []
        for user_sentence, assistant_sentence in fewshot:
            chat_fewshot.append({"role": "user", "content": user_sentence})
            chat_fewshot.append({"role": "assistant", "content": assistant_sentence})
        fewshot = chat_fewshot
    return fewshot