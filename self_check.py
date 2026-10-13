from pathlib import Path
import tempfile

from app import process_document


with tempfile.TemporaryDirectory() as directory:
    text_file = Path(directory) / "entrada.txt"
    text_file.write_text("María viajó a Guadalajara en 2024.", encoding="utf-8")
    result = process_document(str(text_file), "entrada.txt")
    assert result["status"] == "processed"
    assert result["num_tokens"] > 0
    assert "clean_txt" in result
    assert "clean_txt," not in result

    empty_file = Path(directory) / "vacio.txt"
    empty_file.write_text("", encoding="utf-8")
    empty_result = process_document(str(empty_file), "vacio.txt")
    assert empty_result["status"] == "no_text_extracted"

print("self-check: OK")
