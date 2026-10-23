SPDX-License-Identifier: Community-Spec-1.0

# Tools for checking examples and the model

Scripts used to find and confirm the findings in
[`../FINDINGS.md`](../FINDINGS.md). They are meant to be rerun when the model,
the generators or the tools change, and on new examples.

## Setup

```shell
python3 -m venv .venv
.venv/bin/pip install rdflib pyld pyshacl spdx3-validate
npm install --prefix .node jsonld          # only for --processor jsonld-js
```

For the round-trip probe, also install
[spdx-python-model](https://github.com/spdx/spdx-python-model)
(or run it from a checkout with `PYTHONPATH=src`).

## Scripts

### `validate_example.py`: validate an example

Checks every document of an example with spdx3-validate (against the SPDX
model) and with pySHACL (against the example's own `*.ttl` shapes), and
compares the results with the example's `expected.json`.

```shell
.venv/bin/python validate_example.py ../Extension/SyntheticData
```

Exit code 1 if a result differs from `expected.json`.

### `check_vocab_term_collisions.py`: find mis-expanded vocabulary values

Expands every vocabulary entry with a JSON-LD processor and reports values
that do not expand to their vocabulary IRI (finding S-1).

```shell
.venv/bin/python check_vocab_term_collisions.py \
  https://spdx.org/rdf/3.0.1/spdx-context.jsonld \
  https://spdx.org/rdf/3.0.1/spdx-model.ttl
.venv/bin/python check_vocab_term_collisions.py --processor pyld CONTEXT MODEL
.venv/bin/python check_vocab_term_collisions.py --processor jsonld-js --node-modules .node CONTEXT MODEL
```

Run it with all three processors: they should agree. A difference between
processors points to a processor bug (such as T-3 in rdflib).

### `check_shacl_targets.py`: find shapes only pySHACL applies

Lists class shapes with no explicit target, which select no focus nodes in a
spec-conformant SHACL engine (finding S-3).

```shell
.venv/bin/python check_shacl_targets.py https://spdx.org/rdf/3.0.1/spdx-model.ttl
```

### `roundtrip_spdx_python_model.py`: read and write with spdx-python-model

Reads each document, writes it back, and reports whether the extension data
survived (finding T-1).

```shell
.venv/bin/python roundtrip_spdx_python_model.py --out /tmp/rt ../Extension/SyntheticData/documents/*.json
```

## Recipes

### Generate a 3.1-dev context and model from this repository

With [spec-parser](https://github.com/spdx/spec-parser):

```shell
python3 path/to/spec-parser/main.py -r -R /tmp/spdx31 -f ../../model
```

With [specmd](https://github.com/bact/specmd):

```shell
python3 path/to/specmd/main.py -r -R /tmp/spdx31-specmd -f ../../model
```

Then check `/tmp/spdx31/spdx-context.jsonld` with `/tmp/spdx31/spdx-model.ttl`
using `check_vocab_term_collisions.py`.

### Test with SPDX tools-java

Download the `tools-java-<version>.zip` release from
<https://github.com/spdx/tools-java/releases>, unzip it, and run:

```shell
java -jar tools-java-<version>-jar-with-dependencies.jar Verify FILE
java -jar tools-java-<version>-jar-with-dependencies.jar Convert FILE OUT.spdx3.json JSONLD JSONLD
```

Then run `spdx3-validate -j OUT.spdx3.json` and compare the `extension`
arrays of `FILE` and `OUT.spdx3.json`.

### rdflib protected-term repro

The minimal repro for T-3 is in
[`../issue-drafts/rdflib-protected-term-override.md`](../issue-drafts/rdflib-protected-term-override.md).
Save its JSON as a file and parse it with rdflib, pyld and jsonld.js.
