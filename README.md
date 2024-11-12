# api_ner
Implmentación de una API quen detecta entidades en español con spaCy

Despliegue:

Esta aplicación cuenta con una receta docker para su rápido despliegue a producción, solo se debe tener docker instalado y ejecutar deploy.sh

Descripción:
Esta API permite procesar archivos PDF y obtener un análisis detallado en formato JSON, que incluye:
- Texto limpio extraído del PDF.
- Proporción de texto legible y no alfabético.
- Número de tokens procesados.
- Entidades nombradas detectadas dentro del texto.

