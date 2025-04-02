from pathlib import Path

BASE_URL = "https://scanner.tradingview.com"
HEADERS = {"Content-Type": "application/json"}
DEFAULT_MARKET = "crypto"
LOCAL_META_PATH = Path("/mnt/data/TradingView-Screener-docs (1)/TradingView-Screener-docs/data/metainfo")

TYPE_MAP = {
    "price": {"type": "number"},
    "percent": {"type": "number", "minimum": 0, "maximum": 100},
    "number": {"type": "number"},
    "bool": {"type": "boolean"},
    "text": {"type": "string"},
    "map": {"type": "object", "nullable": True},
    "interface": {"type": "object", "nullable": True},
    "set": {"type": "array", "items": {"type": "string"}},
    "time": {"type": "string", "format": "date-time"},
    "time-yyyymmdd": {"type": "string", "format": "date"},
    "fundamental_price": {"type": "number"},
}

REQUIRED = {
    "orjson": "3.10.7",
    "requests": "2.32.3",
    "requests-cache": "1.2.1",
    "tenacity": "9.0.0",
    "openapi-spec-validator": "0.7.1",
    "pyyaml": "6.0.2"
}

from dotenv import load_dotenv
load_dotenv()

import os

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
