import json
import os

DATA_DIR = 'data'

def _get_filepath(filename: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)

def load_data(filename: str, default_data: dict) -> dict:
    """Carrega os dados do JSON. Se não existir, cria com o dado padrão."""
    filepath = _get_filepath(filename)
    if not os.path.exists(filepath):
        save_data(filename, default_data)
        return default_data
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(filename: str, data: dict):
    """Salva os dados no arquivo JSON."""
    filepath = _get_filepath(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)