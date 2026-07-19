import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variabile d'ambiente mancante: {name}")
    return value


BOT_TOKEN = _require("BOT_TOKEN")

GROUP_CHAT_ID = int(_require("GROUP_CHAT_ID"))
MANUALI_TOPIC_ID = int(_require("MANUALI_TOPIC_ID"))

CACHE_DB_PATH = Path(os.getenv("CACHE_DB_PATH", "data/catalog_cache.sqlite3")).expanduser().resolve()
CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
