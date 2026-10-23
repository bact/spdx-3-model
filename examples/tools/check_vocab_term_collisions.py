# SPDX-License-Identifier: Apache-2.0
"""Find vocabulary entries that a SPDX 3 JSON-LD context expands to the wrong IRI.

For every vocabulary-valued property in the context (an object property whose
range is a vocabulary class), expand each entry of the vocabulary with a JSON-LD processor
and compare the result with the expected IRI. A mismatch happens when the
entry name is also a term in the context (JSON-LD resolves terms before
applying "@vocab").

Usage:
    python check_vocab_term_collisions.py CONTEXT.jsonld MODEL.ttl

CONTEXT and MODEL can be local paths or URLs, e.g.
    https://spdx.org/rdf/3.0.1/spdx-context.jsonld
    https://spdx.org/rdf/3.0.1/spdx-model.ttl

Exit code is 1 if any collision is found. Requires rdflib.
"""

import json
import sys
import urllib.request

import rdflib
from rdflib import OWL, RDF, RDFS, URIRef


def load_json(location):
    if "://" in location:
        with urllib.request.urlopen(location) as f:
            return json.load(f)
    with open(location, encoding="utf-8") as f:
        return json.load(f)


def term_kind(ctx, model, term):
    value = ctx[term]
    iri = value["@id"] if isinstance(value, dict) else value
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


def main(context_location, model_location):
    ctx = load_json(context_location)["@context"]
    model = rdflib.Graph().parse(model_location)
    individuals = {str(s) for s in model.subjects(RDF.type, OWL.NamedIndividual)}

    # A vocabulary-valued property is an object property whose range is a
    # class with named individuals (its entries). Find them from the model,
    # so that contexts with or without a scoped "@vocab" can be checked.
    vocab_props = {}
    for name, value in ctx.items():
        if not isinstance(value, dict) or "@id" not in value:
            continue
        for rng in model.objects(URIRef(value["@id"]), RDFS.range):
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
        expanded = rdflib.Graph().parse(data=json.dumps(doc), format="json-ld")
        got = {str(s): str(o) for s, _, o in expanded}
        for n, (entry, name) in enumerate(zip(entries, names)):
            actual = got.get(f"urn:check:{n}")
            if actual != entry:
                kind = term_kind(ctx, model, name)[0] if name in ctx else "?"
                collisions.append((prop, name, entry, actual, kind))

    print(f"Checked {checked} entries of {len(vocab_props)} vocabulary properties.")
    for prop, entry, expected, actual, kind in collisions:
        print(f'COLLISION {prop}: "{entry}"')
        print(f"  expected: {expected}")
        print(f"  actual:   {actual} ({kind})")
    print(f"{len(collisions)} collision(s).")
    return 1 if collisions else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
