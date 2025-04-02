# TradingView Screener

[![CI](https://github.com/your-org/tv-screener/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/tv-screener/actions)

Modular OpenAPI 3.1.0 spec + SDK generator for TradingView Screener API.

## Features

- OpenAPI 3.1 generation
- SDK generation (Python, TS)
- HTML documentation (Swagger, Redoc)
- CLI via Typer
- CI/CD + testing

## CLI Examples

```bash
make install
make openapi
make sdk
make html
make test
```

## Generated Docs

- [Swagger UI](docs/swagger.html)
- [ReDoc](docs/redoc.html)

## Project Structure

```
tv_screener/
├── cli.py
├── client.py
├── config.py
├── sdk.py
├── spec.py
├── utils.py
```