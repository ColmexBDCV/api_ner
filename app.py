from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from pdf_handler import get_ocr
from ocr_quality_check import compute_document

app = FastAPI()

# Directorio donde se almacenarán temporalmente los archivos
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ruta GET para recibir el archivo y procesarlo
@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    try:
        # Guardar el archivo en el sistema temporalmente
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Aquí debes insertar el código de procesamiento del archivo
        # Supongamos que ya tienes una función llamada `process_document`
        # que toma el archivo y regresa los resultados en JSON
        result = process_document(file_path)

        # Eliminar el archivo temporal después del procesamiento
        os.remove(file_path)

        # Regresar el resultado del procesamiento como un JSON
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Función que procesa el archivo y regresa un JSON
# Aquí deberías implementar tu lógica de procesamiento
def process_document(file_path):
    # Supongamos que este es el proceso que ya tienes
    # Esta función debe retornar un diccionario o lista que será convertido a JSON
    
    text = get_ocr(file_path)
    clean_txt, legible_ratio_es, non_alpha_ratio, num_tokens, detected_entities = compute_document(text)
    return {
        "filename": os.path.basename(file_path),
        "legible_ratio_es": legible_ratio_es,
        "non_alpha_ratio": non_alpha_ratio, 
        "num_tokens": num_tokens,
        "clean_txt,": clean_txt,
        "detected_entities": detected_entities,
        "status": "Processed",
        "details": "Archivo procesado exitosamente"
    }

