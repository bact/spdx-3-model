SPDX-License-Identifier: Community-Spec-1.0

# packageUrl

## Summary

Provides a place for the SPDX data creator to record the Package-URL
for a software Package.

## Description

A packageUrl property captures a Package-URL (PURL), which is a valid URL and
URI to identify a software package, independently from their ecosystem or
distribution channel, as specified in
[ECMA-427](https://ecma-international.org/publications-and-standards/standards/ecma-427/).

A PURL is composed of seven components:

```text
scheme:type/namespace/name@version?qualifiers#subpath
```

The permitted characters, separators, character encodings, and rules for each
component are defined in Section 5 of ECMA-427.

Components are designed such that they form a hierarchy from the most
significant on the left to the least significant components on the right.

The PURL type component defines the ecosystem-specific structure and meaning
for the other PURL components.

The machine-readable definitions of all registered PURL types
are maintained in the
[PURL Type Definitions](https://github.com/package-url/purl-spec/blob/main/types/README.md).

While the following are valid URL or URI schemes, they shall not be used as
PURL types. They may be used as values within a PURL qualifier:

- Special URL schemes defined in <https://url.spec.whatwg.org/>
  (such as `file://`, `ftp://`, `http://`, and `https://`).
- Version control system (VCS) URLs (such as `git://`, `hg://`, and `svn://`).

## Metadata

- name: packageUrl
- Nature: DataProperty
- Range: xsd:anyURI
