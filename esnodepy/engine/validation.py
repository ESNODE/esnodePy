from typing import Any, Dict, cast
import json
from pathlib import Path

import jsonschema


class ValidationError(Exception):
    pass


def _load_schema() -> Dict[str, Any]:
    # Locate the schema file relative to this package root
    schema_path = Path(__file__).resolve().parents[2] / ".github" / "esnode_report.schema.json"
    if not schema_path.exists():
        raise ValidationError(f"Schema file not found: {schema_path}")
    return cast(Dict[str, Any], json.loads(schema_path.read_text(encoding="utf-8")))


def validate_scan_report(data: Dict[str, Any]) -> None:
    """Validate scan report using jsonschema.

    Raises `ValidationError` with jsonschema message on failure.
    """
    schema = _load_schema()
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as ve:
        raise ValidationError(str(ve)) from ve
