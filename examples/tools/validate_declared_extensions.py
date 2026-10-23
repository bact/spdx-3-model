# SPDX-License-Identifier: Apache-2.0
"""Validate a document that declares its extensions with ExtensionDefinition.

Prototype of the consumer behavior proposed in finding M-1
(https://github.com/bact/spdx-3-model/tree/extension-definition): for each
ExtensionDefinition in the document,

1. fetch the definition from its locationHint (or from a local file given
   with --location URL=FILE),
2. verify it against its verifiedUsing hashes,
3. check that every class and property IRI in the document that is not
   SPDX's is in a declared extensionNamespace (ending with / or #),

then validate the document with SHACL against the SPDX model shapes plus the
declared definitions, with a positive check that every extension value is an
Extension (finding M-3). A definition that is not verified by a supported
hash is not used, and is an error.

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
import rdflib.util
from pyshacl import validate as shacl_validate
from rdflib.namespace import RDF, SH

# SPDX HashAlgorithm entries that hashlib can compute
HASH_ALGORITHMS = {
    "md5": ("md5", None),
    "sha1": ("sha1", None),
    "sha224": ("sha224", None),
    "sha256": ("sha256", None),
    "sha384": ("sha384", None),
    "sha512": ("sha512", None),
    "sha3_224": ("sha3_224", None),
    "sha3_256": ("sha3_256", None),
    "sha3_384": ("sha3_384", None),
    "sha3_512": ("sha3_512", None),
    "blake2b256": ("blake2b", 32),
    "blake2b384": ("blake2b", 48),
    "blake2b512": ("blake2b", 64),
}

# Namespaces that are not extension terms
STANDARD = (
    str(RDF),
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/2002/07/owl#",
)


def load_bytes(location, locations):
    if location in locations:
        with open(locations[location], "rb") as f:
            return f.read()
    with urllib.request.urlopen(location, timeout=30) as f:
        return f.read()


def load_context(path):
    with open(path, encoding="utf-8") as f:
        context = json.load(f)["@context"]
    if isinstance(context, list):
        merged = {}
        for item in context:
            if isinstance(item, dict):
                merged.update(item)
        context = merged
    return context


def digest(algorithm, content):
    name, size = HASH_ALGORITHMS[algorithm]
    if size:
        return hashlib.new(name, content, digest_size=size).hexdigest()
    return hashlib.new(name, content).hexdigest()


def main(args):
    context = load_context(args.context)
    with open(args.document, encoding="utf-8") as f:
        doc = json.load(f)
    if args.context_url and doc.get("@context") != args.context_url:
        sys.exit(f"document @context is not {args.context_url}")
    doc["@context"] = context

    data = rdflib.Graph().parse(data=json.dumps(doc), format="json-ld")
    model = rdflib.Graph().parse(args.model)
    # The "spdx" prefix of the context is the SPDX terms namespace
    spdx = context.get("spdx")
    terms = spdx.get("@id") if isinstance(spdx, dict) else spdx
    if not terms:
        sys.exit("context has no spdx prefix")
    core, ext = terms + "Core/", terms + "Extension/"

    locations = dict(item.split("=", 1) for item in args.location)
    shapes = rdflib.Graph() + model
    errors = 0

    namespaces = []
    for definition in data.objects(None, rdflib.URIRef(core + "extensionDefinition")):
        namespace = data.value(definition, rdflib.URIRef(ext + "extensionNamespace"))
        if namespace is None:
            print("ExtensionDefinition without extensionNamespace")
            errors += 1
            continue
        namespace = str(namespace)
        if not namespace.endswith(("/", "#")):
            print(f"{namespace}: extensionNamespace does not end with / or #")
            errors += 1
        namespaces.append(namespace)
        location = data.value(definition, rdflib.URIRef(core + "locationHint"))
        if location is None:
            print(f"{namespace}: no locationHint, definition not loaded")
            errors += 1
            continue
        try:
            content = load_bytes(str(location), locations)
        except OSError as e:
            print(f"{namespace}: cannot retrieve {location}: {e}")
            errors += 1
            continue
        verified = False
        for method in data.objects(definition, rdflib.URIRef(core + "verifiedUsing")):
            algorithm = str(data.value(method, rdflib.URIRef(core + "algorithm"))).rsplit("/", 1)[-1]
            expected = str(data.value(method, rdflib.URIRef(core + "hashValue"))).lower()
            if algorithm not in HASH_ALGORITHMS:
                print(f"{namespace}: hash algorithm {algorithm} not supported here")
                continue
            actual = digest(algorithm, content)
            if actual != expected:
                print(f"{namespace}: {algorithm} mismatch for {location}: expected {expected}, got {actual}")
                errors += 1
            else:
                print(f"{namespace}: {location} verified ({algorithm})")
                verified = True
        if not verified:
            print(f"{namespace}: definition not verified, not used")
            errors += 1
            continue
        shapes.parse(data=content, format=rdflib.util.guess_format(str(location)) or "turtle")

    # Every class and property IRI outside SPDX and the standard vocabularies
    # must be in a declared namespace (the longest matching one applies)
    used = {str(o) for o in data.objects(None, RDF.type)} | {str(p) for p in data.predicates()}
    for iri in sorted(used):
        if iri.startswith(terms) or iri.startswith(STANDARD):
            continue
        if not any(iri.startswith(ns) for ns in namespaces):
            print(f"{iri} is not in a declared extensionNamespace")
            errors += 1

    # Every extension value must be an Extension (positive check, as in M-3),
    # which also catches a definition written for another SPDX version
    check = rdflib.BNode()
    prop = rdflib.BNode()
    shapes.add((check, RDF.type, SH.NodeShape))
    shapes.add((check, SH.targetSubjectsOf, rdflib.URIRef(core + "extension")))
    shapes.add((check, SH.property, prop))
    shapes.add((prop, SH.path, rdflib.URIRef(core + "extension")))
    shapes.add((prop, SH["class"], rdflib.URIRef(ext + "Extension")))

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
