from pathlib import Path
import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from text_quality_check import compute_document
from text_extractor import extract_text


app = FastAPI()
UPLOAD_DIR = "./uploads"
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(50 * 1024 * 1024)))
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    file_path = None
    try:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise HTTPException(status_code=415, detail="Solo se aceptan archivos PDF, TXT o MD")
        with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, suffix=suffix, delete=False) as temporary:
            file_path = temporary.name
            size = 0
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="El archivo supera el límite permitido")
                temporary.write(chunk)

        result = process_document(file_path, file.filename or "archivo")
        status_code = 422 if result["status"] == "no_text_extracted" else 200
        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        if file_path:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass


def process_document(file_path, original_filename=None):
    text = extract_text(file_path)
    filename = original_filename or Path(file_path).name
    if not text.strip():
        return {
            "filename": filename,
            "status": "no_text_extracted",
            "details": "No se pudo extraer texto del archivo",
        }

    clean_txt, legible_ratio_es, non_alpha_ratio, num_tokens, detected_entities = compute_document(text)
    return {
        "filename": filename,
        "legible_ratio_es": legible_ratio_es,
        "non_alpha_ratio": non_alpha_ratio,
        "num_tokens": num_tokens,
        "clean_txt": clean_txt,
        "detected_entities": detected_entities,
        "status": "processed",
        "details": "Archivo procesado exitosamente",
    }
