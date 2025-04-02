import requests
import requests_mock
from tv_screener.client import ScreenerClient

def test_mocked_metainfo():
    with requests_mock.Mocker() as m:
        m.post("https://scanner.tradingview.com/crypto/metainfo", json={"fields": {"test": {"t": "price"}}})
        client = ScreenerClient("crypto")
        response = client.fetch_metainfo()
        assert "fields" in response
        assert "test" in response["fields"]