# SPDX-License-Identifier: Apache-2.0
"""Find SHACL shapes that only an engine like pySHACL would apply (finding S-3).

SHACL applies the implicit class target only to a shape that is a SHACL
instance of rdfs:Class. A shape typed owl:Class with no sh:targetClass (or
other target) selects no focus nodes in a spec-conformant engine, unless the
shapes graph states owl:Class rdfs:subClassOf rdfs:Class.

Usage:
    python check_shacl_targets.py SHAPES...

SHAPES can be local paths or URLs, e.g. https://spdx.org/rdf/3.0.1/spdx-model.ttl
Exit code is 1 if any shape has no target that every engine applies.
"""

import sys

import rdflib
from rdflib.namespace import OWL, RDF, RDFS, SH

TARGETS = (SH.targetClass, SH.targetNode, SH.targetSubjectsOf, SH.targetObjectsOf)


def untargeted(g):
    if (OWL.Class, RDFS.subClassOf, RDFS.Class) in g:
        return []
    # A node is a shape if typed sh:NodeShape or if it has constraint parameters.
    shapes = set(g.subjects(RDF.type, SH.NodeShape))
    for param in (SH.property, SH.nodeKind, SH["not"], SH["or"], SH["and"], SH.sparql):
        shapes.update(g.subjects(param, None))
    shapes = {s for s in shapes if isinstance(s, rdflib.URIRef)}
    return sorted(
        s
        for s in shapes
        if (s, RDF.type, OWL.Class) in g
        and (s, RDF.type, RDFS.Class) not in g
        and not any((s, t, None) in g for t in TARGETS)
    )


def main(paths):
    found = 0
    for path in paths:
        g = rdflib.Graph().parse(path)
        shapes = untargeted(g)
        print(f"{path}: {len(shapes)} owl:Class shape(s) with no explicit target")
        for s in shapes:
            print(f"  {s}")
        found += len(shapes)
    return 1 if found else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
