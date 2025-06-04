from functools import lru_cache
from transformers import pipeline

@lru_cache
def pipe():
    return pipeline("text-classification", model="iit-tu-berlin/xlm-roberta-base-goemotions-tr", top_k=None, device=-1)

def detect(text:str):
    best=max(pipe()(text, truncation=True)[0], key=lambda x:x["score"])
    return best["label"], float(best["score"])
