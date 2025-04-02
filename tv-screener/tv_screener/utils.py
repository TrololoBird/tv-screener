import sys
import subprocess
import importlib.metadata
from typing import Dict, Any
import logging

from .config import REQUIRED, TYPE_MAP

logger = logging.getLogger(__name__)

def ensure_deps():
    for pkg, ver in REQUIRED.items():
        try:
            installed = importlib.metadata.version(pkg)
            if installed != ver:
                logger.info(f"Reinstalling {pkg} to version {ver} (current: {installed})")
                subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg}=={ver}", "--force-reinstall"])
        except importlib.metadata.PackageNotFoundError:
            logger.info(f"Installing missing package: {pkg}=={ver}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg}=={ver}"])

def convert_field(name: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    typ = raw.get("t", "string")
    schema = TYPE_MAP.get(typ, {"type": "string"})
    field = dict(schema)
    field["nullable"] = raw.get("nullable", False)
    if "format" in raw:
        field["format"] = raw["format"]
    field["description"] = raw.get("description", f"Field: {name} (type: {typ})")
    values = raw.get("r", [])
    if values:
        field["enum"] = values
    return field

def build_field_map(raw_fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            key: convert_field(key, raw_fields[key])
            for key in sorted(raw_fields)
        },
        "additionalProperties": False
    }