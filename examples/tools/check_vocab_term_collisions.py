# SPDX-License-Identifier: Apache-2.0
"""Find vocabulary entries that a SPDX 3 JSON-LD context expands to the wrong IRI.

For every vocabulary-valued property in the context (an object property whose
range is a vocabulary class), expand each entry of the vocabulary with a
JSON-LD processor and compare the result with the expected IRI. A mismatch
happens when the entry name is also a term in the context (JSON-LD resolves
terms before applying "@vocab"), or when the processor does not follow the
JSON-LD 1.1 algorithms.

Usage:
    python check_vocab_term_collisions.py [--processor NAME] CONTEXT MODEL

CONTEXT and MODEL can be local paths or URLs, e.g.
    https://spdx.org/rdf/3.0.1/spdx-context.jsonld
    https://spdx.org/rdf/3.0.1/spdx-model.ttl

Processors:
    rdflib     (default) requires rdflib
    pyld       requires pyld
    jsonld-js  requires node and the "jsonld" npm package; pass the directory
               containing node_modules with --node-modules

Exit code is 1 if any collision is found, 2 if the processor fails. Requires
rdflib in all cases (to read the model).
"""

import argparse
import json
import subprocess
import sys
import urllib.request

import rdflib
from rdflib import OWL, RDF, RDFS, URIRef

JSONLD_JS = """
const jsonld = require("jsonld");
let input = "";
process.stdin.on("data", (d) => (input += d));
process.stdin.on("end", async () => {
  process.stdout.write(JSON.stringify(await jsonld.expand(JSON.parse(input))));
});
"""


def load_json(location):
    if "://" in location:
        with urllib.request.urlopen(location) as f:
            return json.load(f)
    with open(location, encoding="utf-8") as f:
        return json.load(f)


def load_context(location):
    """Load a context document and merge an array @context into one map."""
    ctx = load_json(location)["@context"]
    if not isinstance(ctx, list):
        return ctx
    merged = {}
    for item in ctx:
        merged.update(load_json(item)["@context"] if isinstance(item, str) else item)
    return merged


def term_iri(ctx, value):
    """Return the IRI a term maps to, expanding a compact IRI (prefix:suffix)."""
    iri = value.get("@id") if isinstance(value, dict) else value
    if not isinstance(iri, str):
        return None
    prefix, sep, suffix = iri.partition(":")
    if sep and not suffix.startswith("//") and prefix in ctx:
        base = term_iri(ctx, ctx[prefix])
        if base:
            return base + suffix
    return iri


def term_kind(ctx, model, term):
    iri = term_iri(ctx, ctx[term])
    if iri is None:
        return "other", None
    node = URIRef(iri)
    if (node, RDF.type, OWL.ObjectProperty) in model or (
        node,
        RDF.type,
        OWL.DatatypeProperty,
    ) in model:
        return "property", iri
    if (node, RDF.type, OWL.Class) in model:
        return "class", iri
    if (node, RDF.type, OWL.NamedIndividual) in model:
        return "individual", iri
    return "other", iri


def values_from_expanded(expanded):
    """Map each node id to its object IRI (or literal) in expanded JSON-LD.

    Each test node has a single value, so there is one object per node.
    """
    got = {}
    for node in expanded:
        for key, values in node.items():
            if key.startswith("@"):
                continue
            for v in values:
                got[node["@id"]] = v.get("@id", v.get("@value"))
    return got


def expand_rdflib(doc, _args):
    graph = rdflib.Graph().parse(data=json.dumps(doc), format="json-ld")
    return {str(s): str(o) for s, _, o in graph}


def expand_pyld(doc, _args):
    from pyld import jsonld

    return values_from_expanded(jsonld.expand(doc))


def expand_jsonld_js(doc, args):
    result = subprocess.run(
        ["node", "-e", JSONLD_JS],
        input=json.dumps(doc),
        capture_output=True,
        text=True,
        check=True,
        cwd=args.node_modules,
    )
    return values_from_expanded(json.loads(result.stdout))


EXPANDERS = {"rdflib": expand_rdflib, "pyld": expand_pyld, "jsonld-js": expand_jsonld_js}


def main(args):
    ctx = load_context(args.context)
    model = rdflib.Graph().parse(args.model)
    individuals = {str(s) for s in model.subjects(RDF.type, OWL.NamedIndividual)}
    expand = EXPANDERS[args.processor]

    # A vocabulary-valued property is an object property whose range is a
    # class with named individuals (its entries). Find them from the model,
    # so that contexts with or without a scoped "@vocab" can be checked.
    vocab_props = {}
    for name, value in ctx.items():
        iri = term_iri(ctx, value) if isinstance(value, dict) else None
        if not iri:
            continue
        for rng in model.objects(URIRef(iri), RDFS.range):
            entries = sorted(str(i) for i in model.subjects(RDF.type, rng) if str(i) in individuals)
            if entries:
                vocab_props[name] = entries

    checked = 0
    collisions = []
    for prop, entries in sorted(vocab_props.items()):
        names = [e.rsplit("/", 1)[1] for e in entries]
        checked += len(entries)
        doc = {
            "@context": ctx,
            "@graph": [{"@id": f"urn:check:{n}", prop: e} for n, e in enumerate(names)],
        }
        try:
            got = expand(doc, args)
        except Exception as e:  # noqa: BLE001 - a processor failure is not a collision
            print(f"{args.processor} failed on {prop}: {type(e).__name__}: {e}", file=sys.stderr)
            return 2
        for n, (entry, name) in enumerate(zip(entries, names)):
            actual = got.get(f"urn:check:{n}")
            if actual != entry:
                kind = term_kind(ctx, model, name)[0] if name in ctx else "?"
                collisions.append((prop, name, entry, actual, kind))

    print(f"Checked {checked} entries of {len(vocab_props)} vocabulary properties with {args.processor}.")
    scoped = {n for n, v in ctx.items() if isinstance(v, dict) and "@vocab" in v.get("@context", {})}
    if scoped - vocab_props.keys():
        print(f"WARNING: scoped @vocab terms not checked: {', '.join(sorted(scoped - vocab_props.keys()))}")
    for prop, entry, expected, actual, kind in collisions:
        print(f'COLLISION {prop}: "{entry}"')
        print(f"  expected: {expected}")
        print(f"  actual:   {actual} ({kind})")
    print(f"{len(collisions)} collision(s).")
    return 1 if collisions else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("context", help="JSON-LD context (path or URL)")
    parser.add_argument("model", help="SPDX model in Turtle (path or URL)")
    parser.add_argument("--processor", choices=sorted(EXPANDERS), default="rdflib")
    parser.add_argument("--node-modules", default=".", help="directory containing node_modules/jsonld (for jsonld-js)")
    sys.exit(main(parser.parse_args()))
