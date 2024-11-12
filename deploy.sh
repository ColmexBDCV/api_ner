#!/bin/bash
docker build -t api-ner-image:latest .
docker run -d --name API-NER -p 8000:8000 api-ner-image



