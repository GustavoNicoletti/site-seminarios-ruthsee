import json
import os
import tempfile
from copy import deepcopy
from json import JSONDecodeError
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'


def _get_filepath(filename: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR / filename


def load_data(filename: str, default_data: Any) -> Any:
    """Carrega um JSON da pasta data e recria o arquivo se ele não existir."""
    filepath = _get_filepath(filename)

    if not filepath.exists():
        data = deepcopy(default_data)
        save_data(filename, data)
        return data

    try:
        with filepath.open('r', encoding='utf-8') as f:
            return json.load(f)
    except (JSONDecodeError, OSError):
        return deepcopy(default_data)


def save_data(filename: str, data: Any) -> None:
    """Salva dados em JSON de forma atômica para reduzir risco de arquivo parcial."""
    filepath = _get_filepath(filename)

    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=DATA_DIR, delete=False) as temp_file:
        json.dump(data, temp_file, indent=4, ensure_ascii=False)
        temp_file.write('\n')
        temp_path = Path(temp_file.name)

    os.replace(temp_path, filepath)
