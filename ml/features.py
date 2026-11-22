"""
Hand-crafted linguistic features for readability prediction.

Every feature here is also implemented in backend/readability_analyzer.js
(same tokenisation, same syllable rule), so a model trained in Python can be
exported as plain coefficients and run inside the Node.js backend.
If you change something here, change it there too and re-run
ml/check_js_parity.py.
"""
import math
import re

# Small list of very common English function words. We use it to measure how
# "everyday" the vocabulary of a passage is. Kept short and fixed on purpose so
# that the JS side can carry an identical copy.
COMMON_WORDS = set("""
a about after all also an and any are as at be because been but by can could
did do does for from had has have he her him his how i if in into is it its
just like make many me more most my no not now of on one only or other our out
over said she so some than that the their them then there these they this time
to two up us very was we were what when which who will with would you your
""".split())

WORD_RE = re.compile(r"[A-Za-z]+")
SENT_SPLIT_RE = re.compile(r"[.?!]+")

FEATURE_NAMES = [
    "n_words",
    "n_sentences",
    "n_paragraphs",
    "avg_sentence_len",
    "sd_sentence_len",
    "max_sentence_len",
    "avg_word_len",
    "avg_syllables",
    "pct_long_words",
    "pct_complex_words",
    "pct_monosyllabic",
    "type_token_ratio",
    "root_ttr",
    "pct_common_words",
    "commas_per_sentence",
    "semicolons_colons",
    "quote_density",
    "flesch_reading_ease",
    "flesch_kincaid_grade",
]


def count_syllables(word: str) -> int:
    """Same heuristic as the JS countSyllables() in the backend."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", word)
    word = re.sub(r"^y", "", word)
    groups = re.findall(r"[aeiouy]{1,2}", word)
    return max(1, len(groups)) if groups else 1


def extract_features(text: str) -> dict:
    text = text if isinstance(text, str) else ""
    words = WORD_RE.findall(text)
    n_words = max(1, len(words))

    sentences = [s for s in SENT_SPLIT_RE.split(text) if s.strip()]
    n_sent = max(1, len(sentences))
    sent_lens = [len(WORD_RE.findall(s)) for s in sentences] or [0]
    mean_len = sum(sent_lens) / len(sent_lens)
    sd_len = math.sqrt(sum((x - mean_len) ** 2 for x in sent_lens) / len(sent_lens))

    paragraphs = [p for p in re.split(r"\n\s*\n|\n", text) if p.strip()]

    syl = [count_syllables(w) for w in words] or [1]
    lower = [w.lower() for w in words]
    uniq = len(set(lower))

    asl = n_words / n_sent
    asw = sum(syl) / n_words

    return {
        "n_words": float(n_words),
        "n_sentences": float(n_sent),
        "n_paragraphs": float(max(1, len(paragraphs))),
        "avg_sentence_len": asl,
        "sd_sentence_len": sd_len,
        "max_sentence_len": float(max(sent_lens)),
        "avg_word_len": sum(len(w) for w in words) / n_words,
        "avg_syllables": asw,
        "pct_long_words": sum(1 for w in words if len(w) > 6) / n_words,
        "pct_complex_words": sum(1 for s in syl if s >= 3) / n_words,
        "pct_monosyllabic": sum(1 for s in syl if s == 1) / n_words,
        "type_token_ratio": uniq / n_words,
        "root_ttr": uniq / math.sqrt(n_words),
        "pct_common_words": sum(1 for w in lower if w in COMMON_WORDS) / n_words,
        "commas_per_sentence": text.count(",") / n_sent,
        "semicolons_colons": (text.count(";") + text.count(":")) / n_sent,
        "quote_density": (text.count('"') + text.count("“") + text.count("”")) / n_words,
        "flesch_reading_ease": 206.835 - 1.015 * asl - 84.6 * asw,
        "flesch_kincaid_grade": 0.39 * asl + 11.8 * asw - 15.59,
    }


def feature_frame(texts):
    import pandas as pd
    return pd.DataFrame([extract_features(t) for t in texts], columns=FEATURE_NAMES)


# --- small sklearn helpers (kept here so saved pipelines can be re-loaded) ---
from sklearn.base import BaseEstimator, TransformerMixin  # noqa: E402


class HandFeatures(BaseEstimator, TransformerMixin):
    """Turns raw passages into the 19 features above inside a Pipeline."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return feature_frame(list(X)).values


def select_fkgl(X):
    return X[:, [FEATURE_NAMES.index("flesch_kincaid_grade")]]


def down_weight_sparse(X):
    """Scaled features are multiplied by 0.35 so they don't drown out TF-IDF."""
    from scipy.sparse import csr_matrix
    return csr_matrix(X * 0.35)
