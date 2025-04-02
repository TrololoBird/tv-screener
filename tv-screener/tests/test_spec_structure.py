import yaml

def test_fields_schema():
    with open("openapi.yaml", "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    field_map = spec["components"]["schemas"]["FieldMap"]
    assert field_map["type"] == "object"
    assert "properties" in field_map