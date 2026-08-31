SPDX-License-Identifier: Community-Spec-1.0

# marginOfError

## Summary

Expression of the uncertainty, precision, or confidence interval associated
with an Observation.

## Description

The `marginOfError` property indicates the statistical certainty or error
bounds with a value.

As calculation methodologies frequently rely on proxy data or probabilistic
models, this property can be used to explicitly declare the known variance of
the measurement or estimation event (for example, "+/- 5%", "95% CI: 10-15").

## Metadata

- name: marginOfError
- Nature: DataProperty
- Range: xsd:string
