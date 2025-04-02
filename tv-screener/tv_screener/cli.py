import typer
import yaml
import orjson
from pathlib import Path
from openapi_spec_validator import validate_spec

from .utils import ensure_deps
from .client import ScreenerClient
from .spec import generate_openapi
from .sdk import generate_sdk, generate_models_from_json
from .config import DEFAULT_MARKET

app = typer.Typer()
import logging

@app.command()
def generate(
    market: str = typer.Option(DEFAULT_MARKET, help="Market type (e.g. crypto, coin)"),
    out: Path = typer.Option(Path("openapi.yaml"), help="Output YAML file"),
    json_out: bool = typer.Option(False, "--json", help="Also write JSON file")
):
    ensure_deps()
    client = ScreenerClient(market)
    fields = client.fetch_metainfo().get("fields", {})
    example = client.fetch_scan_example()
    spec = generate_openapi(market, fields, example)
    out.write_text(yaml.dump(spec, allow_unicode=True), encoding="utf-8")
    typer.echo(f"✅ YAML OpenAPI saved to {out}")
    if json_out:
        json_path = out.with_suffix(".json")
        json_path.write_bytes(orjson.dumps(spec, option=orjson.OPT_INDENT_2))
        typer.echo(f"✅ JSON OpenAPI saved to {json_path}")

@app.command()
def validate(file: Path):
    spec = yaml.safe_load(file.read_bytes())
    validate_spec(spec)
    typer.echo("✅ OpenAPI spec is valid.")

@app.command()
def sdk(spec: Path, languages: list[str] = typer.Option(None, help="Languages for SDK generation")):
    generate_sdk(str(spec), languages=languages)
    typer.echo("✅ SDK generated.")

@app.command("generate-models")
def generate_models(input_json: Path):
    generate_models_from_json(str(input_json))
    typer.echo("✅ Models generated from JSON.")

if __name__ == "__main__":
    app()

@app.command("generate-html")
def generate_html(
    yaml_file: Path = typer.Argument(..., help="Path to OpenAPI YAML file"),
    docs_dir: Path = typer.Option(Path("docs"), help="Directory to save HTML files")
):
    """Generate Swagger UI and ReDoc HTML from YAML."""
    docs_dir.mkdir(parents=True, exist_ok=True)
    swagger_path = docs_dir / "swagger.html"
    redoc_path = docs_dir / "redoc.html"

    # Генерация Swagger UI (через swagger-ui-dist)
    swagger_template = f'''
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
    <script>
      window.onload = function() {{
        SwaggerUIBundle({{
          url: "{yaml_file.name}",
          dom_id: '#swagger-ui',
          presets: [SwaggerUIBundle.presets.apis],
          layout: "BaseLayout"
        }});
      }};
    </script>
  </body>
</html>
'''
    swagger_path.write_text(swagger_template.strip(), encoding="utf-8")

    # Генерация ReDoc
    redoc_template = f'''
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <meta charset="utf-8"/>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  </head>
  <body>
    <redoc spec-url="{yaml_file.name}"></redoc>
  </body>
</html>
'''
    redoc_path.write_text(redoc_template.strip(), encoding="utf-8")
    typer.echo(f"✅ Swagger UI: {swagger_path}")
    typer.echo(f"✅ ReDoc HTML: {redoc_path}")


@app.callback()
def main(debug: bool = typer.Option(False, help="Enable debug logging")):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug mode is on.")