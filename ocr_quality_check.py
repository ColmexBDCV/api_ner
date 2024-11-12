#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:01:27 2023

@author: rod
"""

import spacy
from collections import defaultdict
import re


# Carga los modelo de lenguaje
while True:
    try:
        nlp_es = spacy.load('es_core_news_lg')
        nlp_en = spacy.load('en_core_web_lg')
        # load tagger
        break
    except OSError:
        import subprocess

        cmd = f"python -m spacy download es_core_news_lg"
        subprocess.check_call(cmd, shell=True)
        cmd = f"python -m spacy download en_core_web_lg"
        subprocess.check_call(cmd, shell=True)

        
    


nlp_es.max_length = 30000000  # por ejemplo, para establecer el límite en 30,000,000 caracteres
nlp_en.max_length = 30000000  # por ejemplo, para establecer el límite en 30,000,000 caracteres

def compute_non_alpha_ratio(doc):
    # Encuentra todas las palabras con caracteres no alfabéticos en medio
    words_with_non_alpha = [token.text for token in doc if re.search(r'\b\w*[^a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]\w*\b', token.text)]
    # print(words_with_non_alpha)
    
    if len(doc) == 0: 
        return 0
    # Calcula y retorna el ratio
    return len(words_with_non_alpha) / len(doc)


    
def compute_legible_ratio(doc):
    # Procesamiento del texto
       
    if len(doc) == 0:
        return 0

    # Contador de palabras legibles
    legible_count = 0

    # Revisión de cada palabra
    for token in doc:
        if token.pos_ != 'X':
            # print(token.text, token.pos_)
            legible_count += 1

    # Cálculo del ratio de palabras legibles
    legible_ratio = legible_count / len(doc)

    return float(legible_ratio)

def clean_text(text):
    text = re.sub(r'\s*\n\s*', ' ', text)  # Eliminar saltos de línea y espacios adicionales
    text = re.sub(r'\s{2,}', ' ', text)    # Eliminar espacios dobles
    return text.strip()


def detect_entities(text):
    if text == "":
        return ""
    
    entities = []
    entity = {}
    
    doc = nlp_es(text)
   
    for ent in doc.ents:
 
        entity = { 
                "text": ent.text,
                "label": ent.label_,
                "start_token": ent.start,
                "start_char": ent.start_char,
                "end_token": ent.end,
                "end_char": ent.end_char
                
            }
        
        entities.append(entity) 
        
    doc = nlp_en(text)
    
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            
            entity = { 
                    "text": ent.text,
                    "label": ent.label_,
                    "start_token": ent.start,
                    "start_char": ent.start_char,
                    "end_token": ent.end,
                    "end_char": ent.end_char
                    
                }
            entities.append(entity) 
            
    return entities

# # Ejemplo de texto de entrada en español
# text = "Esto es un texto de ejemplo con algunas paabras mal escr\itas."

def compute_document(text):
    
    text = clean_text(text)
    
    doc = nlp_es(text)
    
    
    legible_ratio_es = compute_legible_ratio(doc)
    
    # print(f"Ratio de palabras reconocidas: {legible_ratio_es}")
    
    # Cálculo del ratio de palabras con caracteres no alfabéticos
    non_alpha_ratio = compute_non_alpha_ratio(doc)
    
    detected_entities = detect_entities(text)

    # print(f"Ratio de palabas con carácteres no alfanúmericos: {non_alpha_ratio}")

    return text, legible_ratio_es, non_alpha_ratio, len(doc), detected_entities


if __name__ == "__main__":
    
    from pdf_handler import get_ocr
            
    text = get_ocr('1910.11470v1.pdf')
    clean_text, legible_ratio_es, non_alpha_ratio, num_tokens, detected_entities = compute_document(text)
    