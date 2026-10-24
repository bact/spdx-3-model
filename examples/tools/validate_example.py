# SPDX-License-Identifier: Apache-2.0
"""Validate the documents of an SPDX 3 extension example and compare with expectations.

Each JSON document in the example's documents/ and known-issues/ directories
is checked twice:

- spdx3-validate: the document against the SPDX model;
- extension SHACL: the document against the example's own *.ttl shapes
  (with pySHACL, the shapes also used as the ontology graph).

If the example has an expected.json, results are compared with it:

    {
      "documents/valid-minimal.spdx3.json": {"spdx3-validate": "pass", "extension-shacl": "pass"},
      ...
    }

Usage:
    python validate_example.py EXAMPLE_DIR [--spdx-version auto]

Requires spdx3-validate (next to this Python, or on PATH) and pyshacl.
Exit code is 1 if any result differs from expected.json, or if a document and
expected.json do not list the same files. A spdx3-validate run that fails
without reporting a validation failure or an unknown @context (crash,
network error) is an error, not a "fail".
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from pyshacl import validate as shacl_validate
from rdflib import Graph


def find_spdx3_validate():
    local = Path(sys.executable).parent / "spdx3-validate"
    return str(local) if local.exists() else shutil.which("spdx3-validate")


def run_spdx3_validate(exe, doc, version):
    result = subprocess.run(
        [exe, "--quiet", "-s", version, "-j", str(doc)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return "pass"
    output = (result.stdout + result.stderr).lower()
    # spdx3-validate rejects a document whose @context is not a known SPDX
    # context URL before validating it
    if "validation failed" in output or "unknown version @context" in output:
        return "fail"
    raise RuntimeError(f"spdx3-validate did not run on {doc}:\n{result.stderr or result.stdout}")


def run_extension_shacl(doc, shapes):
    data = Graph().parse(doc, format="json-ld")
    conforms, _, _ = shacl_validate(data, shacl_graph=shapes, ont_graph=shapes)
    return "pass" if conforms else "fail"


def main(args):
    exe = find_spdx3_validate()
    if not exe:
        sys.exit("spdx3-validate not found")
    example = Path(args.example)
    shapes = Graph()
    for ttl in sorted(example.glob("*.ttl")):
        shapes.parse(ttl)
    expected_file = example / "expected.json"
    expected = json.loads(expected_file.read_text()) if expected_file.exists() else {}

    docs = sorted(example.glob("documents/*.json")) + sorted(example.glob("known-issues/*.json"))
    mismatches = 0
    print(f"{'document':<55} {'spdx3-validate':<15} {'extension-shacl':<15}")
    for doc in docs:
        key = doc.relative_to(example).as_posix()
        got = {
            "spdx3-validate": run_spdx3_validate(exe, doc, args.spdx_version),
            "extension-shacl": run_extension_shacl(doc, shapes),
        }
        want = expected.get(key, {})
        cells = []
        for check in ("spdx3-validate", "extension-shacl"):
            mark = ""
            if check in want and want[check] != got[check]:
                mark = f" (expected {want[check]})"
                mismatches += 1
            cells.append(f"{got[check] + mark:<15}")
        print(f"{key:<55} {' '.join(cells)}")

    keys = {doc.relative_to(example).as_posix() for doc in docs}
    for key in sorted(keys ^ expected.keys() if expected else set()):
        print(f"{key}: missing from {'the documents' if key in expected else 'expected.json'}")
        mismatches += 1

    if expected:
        print(f"{mismatches} result(s) differ from expected.json.")
    return 1 if mismatches else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("example", help="example directory, e.g. examples/Extension/SyntheticData")
    parser.add_argument("--spdx-version", default="auto", help="3.0.0, 3.0.1 or auto (from each document)")
    sys.exit(main(parser.parse_args()))
