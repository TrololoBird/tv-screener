import json
import os
import logging
from typing import Dict, Any

import requests
from requests_cache import CachedSession
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import BASE_URL, HEADERS, LOCAL_META_PATH

logger = logging.getLogger(__name__)
session = CachedSession("tv_cache", expire_after=3600)

class ScreenerClient:
    def __init__(self, market: str):
        self.market = market

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch_metainfo(self) -> Dict[str, Any]:
        local_file = LOCAL_META_PATH / f"{self.market}.json"
        if local_file.exists():
            logger.info(f"Loading metainfo from local file: {local_file}")
            return json.loads(local_file.read_text(encoding="utf-8"))
        logger.info(f"Fetching metainfo from remote API for market: {self.market}")
        resp = session.post(f"{BASE_URL}/{self.market}/metainfo", headers=HEADERS)
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch_scan_example(self) -> Dict[str, Any]:
        payload = self.scan_payload_template()
        resp = session.post(f"{BASE_URL}/{self.market}/scan", headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()

    def scan_payload_template(self, columns=None, volume_threshold=1000) -> Dict[str, Any]:
        return {
            "columns": columns or ["close", "volume"],
            "filter": [{"left": "volume", "operation": "greater", "right": volume_threshold}],
            "range": [0, 5],
            "markets": [self.market],
            "symbols": {"query": {"types": [self.market]}}
        }