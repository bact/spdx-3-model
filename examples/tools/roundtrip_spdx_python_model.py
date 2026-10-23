# SPDX-License-Identifier: Apache-2.0
"""Read and write SPDX 3 documents with spdx-python-model and compare extensions.

For each document: read it, write it back to JSON-LD, and compare every
`extension` array before and after. Reports whether reading or writing
fails, and which extension objects changed.

Usage:
    python roundtrip_spdx_python_model.py [--out DIR] FILE...

Requires spdx-python-model (https://github.com/spdx/spdx-python-model).
Documents must be SPDX 3.0.1; others are skipped. Exit code is 1 if any
document fails to read or write, or loses or changes extension data.
"""

import argparse
import io
import json
import sys
from pathlib import Path

from spdx_python_model import v3_0_1 as spdx

CONTEXT = "https://spdx.org/rdf/3.0.1/spdx-context.jsonld"
KEYWORDS = {"@id", "@value", "@type", "@language", "spdxId"}


def extensions(doc):
    """Map each Element id to its extension array, normalized for comparison."""
    result = {}
    for node in doc.get("@graph", []):
        if "extension" in node:
            result[node.get("spdxId", node.get("@id"))] = node["extension"]
    return result


def normalize(value):
    # The serializer writes every extension property value as a list.
    # Keywords and their aliases are never lists.
    if isinstance(value, dict):
        return {
            k: v if k in KEYWORDS or k == "type" else normalize(v if isinstance(v, list) else [v])
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [normalize(v) for v in value]
    return value


def roundtrip(path, out_dir):
    with open(path, "rb") as f:
        original = json.load(f)
    if original.get("@context") != CONTEXT:
        return None, "skipped: not SPDX 3.0.1"
    objset = spdx.SHACLObjectSet()
    try:
        with open(path, "rb") as f:
            spdx.JSONLDDeserializer().read(f, objset)
    except Exception as e:  # noqa: BLE001 - report any library failure as a result
        return False, f"read failed: {type(e).__name__}: {e}"
    buf = io.BytesIO()
    try:
        spdx.JSONLDSerializer().write(objset, buf, indent=2)
    except Exception as e:  # noqa: BLE001
        return False, f"write failed: {type(e).__name__}: {e}"
    written = json.loads(buf.getvalue())
    if out_dir:
        (out_dir / Path(path).name).write_text(json.dumps(written, indent=2) + "\n")
    before, after = extensions(original), extensions(written)
    changed = [k for k in before.keys() | after.keys() if normalize(before.get(k)) != normalize(after.get(k))]
    if changed:
        return False, "extension data changed on: " + ", ".join(sorted(changed))
    return True, "ok, extension data preserved"


def main(args):
    out_dir = Path(args.out) if args.out else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for path in args.files:
        ok, message = roundtrip(path, out_dir)
        print(f"{Path(path).name}: {message}")
        failed += ok is False
    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--out", help="directory to write the round-tripped documents to")
    sys.exit(main(parser.parse_args()))
