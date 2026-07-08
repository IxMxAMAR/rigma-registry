"""Validate every registry data file against its schema. Exit 1 on any error."""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    errors = 0
    checks = [(ROOT / "gpus.json", load(ROOT / "schema/gpu.schema.json"))]
    checks += [(f, load(ROOT / "schema/model.schema.json"))
               for f in sorted((ROOT / "models").glob("*.json"))]
    checks += [(f, load(ROOT / "schema/combo.schema.json"))
               for f in sorted((ROOT / "combos").rglob("*.json"))]
    model_slugs = {load(f)["slug"] for f in (ROOT / "models").glob("*.json")}
    for path, schema in checks:
        data = load(path)
        for err in Draft202012Validator(schema).iter_errors(data):
            print(f"{path.relative_to(ROOT)}: {err.json_path}: {err.message}")
            errors += 1
        if "combos" in str(path):
            if data.get("model") not in model_slugs:
                print(f"{path.relative_to(ROOT)}: model '{data.get('model')}' "
                      f"has no models/*.json entry")
                errors += 1
            quants = None
            for mf in (ROOT / "models").glob("*.json"):
                m = load(mf)
                if m["slug"] == data.get("model"):
                    quants = {g["quant"] for g in m["ggufs"]}
            if quants is not None and data.get("quant") not in quants:
                print(f"{path.relative_to(ROOT)}: quant '{data.get('quant')}' "
                      f"not in model's gguf list")
                errors += 1
    print(f"{'FAIL' if errors else 'OK'}: {len(checks)} files, {errors} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
