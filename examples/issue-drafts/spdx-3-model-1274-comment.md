SPDX-License-Identifier: Community-Spec-1.0

# Draft comment for spdx/spdx-3-model#1274

Not posted. Issue: "Differentiation between `createdBy` property (3.0) and
"createdBy" relationship type (3.1)". Related finding:
[S-1 in FINDINGS.md](../FINDINGS.md#root-fix-remove-the-collisions-in-the-model).

---

I support renaming the `createdBy` **relationship type** (the vocabulary
entry) and keeping the `createdBy` **property**.

**Why rename the entry, not the property**

- The property has been in Core since 3.0, and every document uses it in
  `CreationInfo`. Renaming it would break every existing document.
- The relationship type is new in 3.1 (added in #1092). It is in neither
  3.0.0 nor 3.0.1, so renaming it before the 3.1 release costs nothing.

**The shared name also breaks the JSON-LD serialization**

The relationship type's values come from a vocabulary. JSON-LD checks the
context's top-level terms before it falls back to that vocabulary. Because
`createdBy` is also a property term, this:

    "relationshipType": "createdBy"

expands to the property IRI `https://spdx.org/rdf/3/terms/Core/createdBy`, not
to `.../Core/RelationshipType/createdBy`. The JSON looks valid, but the RDF
says something else. The same problem already exists for
`profileConformance: "extension"`, and in 3.1-dev for `requirementUID`.

The generator can work around this by mapping the colliding entries
explicitly. However, the workaround keeps those terms from being
`@protected`, which matters if the `@context` is opened up for extensions
(spdx/spdx-spec#1312). Removing the shared name fixes it at the source.

**Suggested name**

A name in the style of the other `...By` relationship types (`performedBy`,
`invokedBy`), for example `authoredBy`, keeps the meaning. The new name must
not be a context term itself: `originatedBy`, for instance, is already a Core
property. It also answers the question in this issue: use the property for who
created the Element, and the relationship type for who created an Action or
DefinedProcess.
