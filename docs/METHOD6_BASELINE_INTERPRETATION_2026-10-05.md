# METHOD-6 baseline interpretation — 2026-10-05

## Scope

The frozen METHOD-6 summary reports a **structural advantage of 0.1587 versus the strongest tested baseline**.

That number is a valid comparison against the baseline implementations used in the preserved experiment. It should not be interpreted as an isolated estimate of the value of the MEES search procedure alone.

## Structural asymmetry

METHOD-6 is explicitly designed for a monotone/factorizable minimal-condition problem class and exploits that known structure.

The preserved random-sampling and active-learning baselines use different structural assumptions and fit predictive models over configurations. They were not given an equivalent factorized search representation.

Therefore the comparison combines at least two things:

1. the MEES search procedure;
2. the advantage of matching the known factorized structure of the tested problem class.

A baseline supplied with the same factorization could reduce or change the reported efficiency advantage.

## Boundary metric

The reported zero boundary MAE is exact for the evaluated discretized phase cells. It does not by itself demonstrate economical inference of an unobserved continuous boundary: METHOD-6 queries the complete guaranteed-valid full-binary phase grid before fitting the boundary.

## Supported claim

The defensible claim is:

> On the tested monotone/factorizable problem class, the preserved METHOD-6 implementation outperformed the specific preserved baseline implementations under the reported budget and metrics.

The repository does not establish that MEES is generally superior to equally informed structured baselines.
