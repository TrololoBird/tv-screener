import yaml
from openapi_spec_validator import validate_spec

def test_openapi_spec():
    with open("openapi.yaml", "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    validate_spec(spec)