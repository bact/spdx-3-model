# SPDX-License-Identifier: Apache-2.0
"""Run SPDX 3 documents through SPDX tools-java and compare extensions.

For each document: run `Verify`, run `Convert` (JSON-LD to JSON-LD), and
compare every `extension` array before and after (order-insensitive).

Usage:
    python roundtrip_tools_java.py --cp CLASSPATH --out DIR FILE...

CLASSPATH is the tools-java jar with dependencies, optionally preceded by
locally built store, library or core jars to test fixes, e.g.
    store.jar:library.jar:core.jar:tools-java-2.0.7-jar-with-dependencies.jar

Requires java on PATH, and rdflib. The RDF graphs of input and output are
always compared. If the extension objects differ in JSON but the documents
have the same RDF graph (e.g. a shared node inlined under another Element),
the result is reported as a layout change, not a failure.
Exit code is 1 if any document fails or changes the RDF graph.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import rdflib
from rdflib.compare import isomorphic


def run(cp, *args):
    result = subprocess.run(
        ["java", "-cp", cp, "org.spdx.tools.Main", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [x for x in (result.stdout + result.stderr).splitlines() if x.strip() and "SLF4J" not in x]
    return "\n".join(lines)


def extensions(doc):
    """Map each Element id to its extension objects, as a sorted list of JSON strings."""
    return {
        node.get("spdxId"): sorted(json.dumps(e, sort_keys=True) for e in node["extension"])
        for node in doc.get("@graph", [])
        if "extension" in node
    }


def check(path, cp, out_dir):
    name = Path(path).name
    verify = run(cp, "Verify", str(path))
    verdict = "pass" if "This SPDX Document is valid" in verify else "fail: " + " ".join(verify.splitlines()[:2])[:160]
    out = out_dir / name
    out.unlink(missing_ok=True)
    convert = run(cp, "Convert", str(path), str(out), "JSONLD", "JSONLD")
    if not out.exists() or out.stat().st_size == 0:
        return False, f"verify {verdict}; convert failed: {' '.join(convert.splitlines()[:2])[:160]}"
    before = extensions(json.loads(Path(path).read_text()))
    after = extensions(json.loads(out.read_text()))
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    # Compare RDF even when the JSON is unchanged: the same JSON can mean
    # something else under a different @context
    same = isomorphic(
        rdflib.Graph().parse(str(path), format="json-ld"),
        rdflib.Graph().parse(str(out), format="json-ld"),
    )
    if not same:
        where = f"extension data changed on: {', '.join(changed)}" if changed else "RDF graph changed"
        return False, f"verify {verdict}; {where}"
    if changed:
        return verdict == "pass", f"verify {verdict}; same RDF graph, extension layout changed on: {', '.join(changed)}"
    return verdict == "pass", f"verify {verdict}; extension data preserved"


def main(args):
    if not shutil.which("java"):
        sys.exit("java not found on PATH")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for path in args.files:
        ok, message = check(path, args.cp, out_dir)
        print(f"{Path(path).name}: {message}")
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--cp", required=True, help="Java classpath with tools-java and its dependencies")
    parser.add_argument("--out", required=True, help="directory to write the converted documents to")
    sys.exit(main(parser.parse_args()))
