# api_ner

Prototipo local para extraer texto y detectar entidades nombradas en documentos.

## Qué hace

- Recibe archivos `.pdf`, `.txt` y `.md` mediante una API HTTP.
- Extrae el texto de ambos formatos con Apache Tika; el módulo se denomina `text_extractor.py` porque no está limitado a PDF.
- Calcula indicadores simples de legibilidad y caracteres no alfabéticos.
- Detecta entidades con los modelos `es_core_news_lg` y `en_core_web_lg` de spaCy.

El proyecto **no realiza OCR**. Si un PDF está compuesto únicamente por imágenes, o si Tika no puede interpretar su contenido, la respuesta será `no_text_extracted`.

## Ejecución local

```bash
docker build -t api-ner-local .
docker run --rm -p 8000:8000 api-ner-local
```

La API queda disponible en `http://localhost:8000`.

```bash
curl -F "file=@documento.pdf" http://localhost:8000/process-file/
curl -F "file=@documento.txt" http://localhost:8000/process-file/
```

## Estados de respuesta

- `200 processed`: se extrajo texto y se ejecutó el análisis.
- `422 no_text_extracted`: no se obtuvo texto utilizable.
- `415`: el formato no es PDF, TXT ni MD.
- `413`: el archivo supera el límite de 50 MB.

El límite puede cambiarse con la variable `MAX_UPLOAD_BYTES`. Los archivos recibidos se guardan con un nombre temporal y se eliminan al terminar la solicitud.

## Alcance y límites

Es un prototipo para pruebas reproducibles y documentación técnica. La calidad de la extracción y de las entidades depende del documento, de Apache Tika y de los modelos de spaCy; este repositorio no incluye un conjunto anotado para medir precisión, cobertura o F1. La configuración usa un trabajador de Gunicorn para reducir el consumo de memoria durante las pruebas.

No incluye autenticación, interfaz de usuario, colas de trabajo, almacenamiento persistente ni controles propios de un servicio de producción.
