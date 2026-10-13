import re

import spacy


def load_model(name):
    try:
        return spacy.load(name)
    except OSError as exc:
        raise RuntimeError(
            f"No está instalado el modelo spaCy {name}. "
            "Instálalo durante la construcción del contenedor."
        ) from exc


nlp_es = load_model("es_core_news_lg")
nlp_en = load_model("en_core_web_lg")
nlp_es.max_length = 30_000_000
nlp_en.max_length = 30_000_000


def compute_non_alpha_ratio(doc):
    if len(doc) == 0:
        return 0
    pattern = r"\b\w*[^a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]\w*\b"
    count = sum(bool(re.search(pattern, token.text)) for token in doc)
    return count / len(doc)


def compute_legible_ratio(doc):
    if len(doc) == 0:
        return 0
    return float(sum(token.pos_ != "X" for token in doc) / len(doc))


def clean_text(text):
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def entity_data(entity):
    return {
        "text": entity.text,
        "label": entity.label_,
        "start_token": entity.start,
        "start_char": entity.start_char,
        "end_token": entity.end,
        "end_char": entity.end_char,
    }


def detect_entities(text):
    if not text:
        return []

    entities = [entity_data(entity) for entity in nlp_es(text).ents]
    entities.extend(
        entity_data(entity)
        for entity in nlp_en(text).ents
        if entity.label_ in {"DATE", "TIME"}
    )
    return entities


def compute_document(text):
    text = clean_text(text)
    doc = nlp_es(text)
    return (
        text,
        compute_legible_ratio(doc),
        compute_non_alpha_ratio(doc),
        len(doc),
        detect_entities(text),
    )
