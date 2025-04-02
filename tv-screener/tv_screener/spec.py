from typing import Dict, Any
from .utils import build_field_map
from .config import BASE_URL

def build_path_item(market: str, route: str, tag: str, summary: str, schema: Dict[str, Any], example: Dict[str, Any] = None) -> Dict[str, Any]:
    media_type = {"application/json": {"schema": schema}}
    if example:
        media_type["application/json"]["example"] = example
    parameters = [
        {"name": "market", "in": "path", "required": True, "schema": {"type": "string"}, "description": "Market type (e.g., 'crypto')"},
        {"name": "X-API-Key", "in": "header", "required": False, "schema": {"type": "string"}, "description": "Optional API Key"}
    ]
    item = {
        "post": {
            "tags": [tag],
            "summary": summary,
            "description": f"{summary} operation for {market} market.",
            "operationId": f"{market}_{route}_post",
            "externalDocs": {"description": "Official UI", "url": "https://www.tradingview.com/screener/"},
            "parameters": parameters,
            "responses": {
                "200": {"description": f"Success: {summary}", "content": media_type},
                "400": {"$ref": "#/components/responses/BadRequest"},
                "500": {"$ref": "#/components/responses/ServerError"}
            }
        }
    }
    if example is not None:
        item["post"]["requestBody"] = {"required": True, "content": media_type}
    return {f"/{market}/{route}": item}

def generate_openapi(market: str, fields: Dict[str, Any], scan_example: Dict[str, Any]) -> Dict[str, Any]:
    components = {
        "schemas": {
            "ScanPayload": {"type": "object"},
            "ScanResponse": {"type": "object", "example": scan_example},
            "FieldMap": build_field_map(fields)
        },
        "responses": {
            "BadRequest": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "schema": {"type": "object"},
                        "example": {"error": "Bad Request"}
                    }
                }
            },
            "ServerError": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "schema": {"type": "object"},
                        "example": {"error": "Server Error"}
                    }
                }
            }
        },
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        }
    }
    return {
        "openapi": "3.1.0",
        "info": {
            "title": f"TradingView Screener API ({market})",
            "version": "1.0.0",
            "description": f"Comprehensive OpenAPI 3.1.0 spec for TradingView Screener: {market}",
            "termsOfService": "https://www.tradingview.com/terms/",
            "contact": {"name": "TradingView", "url": "https://www.tradingview.com", "email": "support@tradingview.com"},
            "license": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
        },
        "servers": [{"url": BASE_URL}],
        "security": [{"ApiKeyAuth": []}],
        "tags": [
            {"name": "Metainfo", "description": "Indicator metadata"},
            {"name": "Scan", "description": "Filtering & scanning endpoint"}
        ],
        "paths": {
            **build_path_item(market, "metainfo", "Metainfo", "Get metainfo", build_field_map(fields)),
            **build_path_item(market, "scan", "Scan", "Perform scan", {"$ref": "#/components/schemas/ScanPayload"}, scan_example)
        },
        "components": components
    }