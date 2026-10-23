# SPDX-License-Identifier: Apache-2.0
"""Validate a document that declares its extensions with ExtensionDefinition.

Prototype of the consumer behavior proposed in finding M-1
(https://github.com/bact/spdx-3-model/tree/extension-definition): for each
ExtensionDefinition in the document,

1. fetch the definition from its locationHint (or from a local file given
   with --location URL=FILE),
2. verify it against its verifiedUsing hashes,
3. check that every custom extension type in the document is in a declared
   extensionNamespace,

then validate the document with SHACL against the SPDX model shapes plus the
declared definitions.

Usage:
    python validate_declared_extensions.py --context CONTEXT --model MODEL \\
        [--context-url URL] [--location URL=FILE ...] DOCUMENT

CONTEXT and MODEL are the SPDX JSON-LD context and model (OWL + SHACL) the
document is written against, as local files; for the proposal, generate them
from the extension-definition branch with spec-parser. --context-url is the
@context URL used in the document (default: the one in the document), which
is replaced by CONTEXT. Exit code is 1 if any check fails.
"""

import argparse
import hashlib
import json
import sys
import urllib.request

import rdflib
from pyshacl import validate as shacl_validate
from rdflib.namespace import RDF

HASH_ALGORITHMS = {"sha256": "sha256", "sha384": "sha384", "sha512": "sha512", "sha1": "sha1"}


def load_bytes(location, locations):
    if location in locations:
        with open(locations[location], "rb") as f:
            return f.read()
    with urllib.request.urlopen(location) as f:
        return f.read()


def main(args):
    with open(args.context, encoding="utf-8") as f:
        context = json.load(f)["@context"]
    with open(args.document, encoding="utf-8") as f:
        doc = json.load(f)
    if args.context_url and doc.get("@context") != args.context_url:
        sys.exit(f"document @context is not {args.context_url}")
    doc["@context"] = context

    data = rdflib.Graph().parse(data=json.dumps(doc), format="json-ld")
    model = rdflib.Graph().parse(args.model)
    # The "spdx" prefix of the context is the SPDX terms namespace
    terms = context["spdx"]["@id"] if isinstance(context["spdx"], dict) else context["spdx"]
    core, ext = terms + "Core/", terms + "Extension/"

    locations = dict(item.split("=", 1) for item in args.location)
    shapes = rdflib.Graph() + model
    errors = 0

    namespaces = []
    for definition in data.objects(None, rdflib.URIRef(core + "extensionDefinition")):
        namespace = str(data.value(definition, rdflib.URIRef(ext + "extensionNamespace")))
        location = data.value(definition, rdflib.URIRef(core + "locationHint"))
        namespaces.append(namespace)
        if location is None:
            print(f"{namespace}: no locationHint, definition not checked")
            continue
        content = load_bytes(str(location), locations)
        for method in data.objects(definition, rdflib.URIRef(core + "verifiedUsing")):
            algorithm = str(data.value(method, rdflib.URIRef(core + "algorithm"))).rsplit("/", 1)[-1]
            expected = str(data.value(method, rdflib.URIRef(core + "hashValue")))
            if algorithm not in HASH_ALGORITHMS:
                print(f"{namespace}: hash algorithm {algorithm} not supported here")
                continue
            actual = hashlib.new(HASH_ALGORITHMS[algorithm], content).hexdigest()
            if actual != expected:
                print(f"{namespace}: {algorithm} mismatch for {location}: expected {expected}, got {actual}")
                errors += 1
            else:
                print(f"{namespace}: {location} verified ({algorithm})")
        shapes.parse(data=content, format="turtle")

    for value in data.objects(None, rdflib.URIRef(core + "extension")):
        for typ in data.objects(value, RDF.type):
            t = str(typ)
            if t.startswith(terms):
                continue
            if not any(t.startswith(ns) for ns in namespaces):
                print(f"extension type {t} is not in a declared extensionNamespace")
                errors += 1

    conforms, _, text = shacl_validate(data, shacl_graph=shapes, ont_graph=shapes)
    if not conforms:
        print(text)
        errors += 1
    print("valid" if not errors else f"{errors} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("document")
    parser.add_argument("--context", required=True, help="SPDX JSON-LD context file")
    parser.add_argument("--model", required=True, help="SPDX model (OWL + SHACL) file")
    parser.add_argument("--context-url", help="@context URL the document must use")
    parser.add_argument("--location", action="append", default=[], help="URL=FILE: read URL from a local file")
    sys.exit(main(parser.parse_args()))
