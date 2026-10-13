import logging
from tika import parser

logger = logging.getLogger("tika")
logger.setLevel(logging.ERROR)

def extract_text(file_path):
    parsed_data = parser.from_file(file_path)
    content = parsed_data.get('content')
    text = content.strip() if content else ""
    return text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()
