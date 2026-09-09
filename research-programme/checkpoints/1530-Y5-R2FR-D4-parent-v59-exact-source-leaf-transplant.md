# 5514: Exact source-leaf transplant of the completed parent-v59 cuboid

Date: 2026-09-07. Private checkpoint. No GitHub action.

## Result

Checkpoint 5513's completed E07/U051 right-connector region now certifies
its **39,732 original outer source records**, through 1,540 source fibers.
The earlier E08/U060 certificate and its 810 records are preserved.
Combined coverage is **40,542 / 606,990** outer source records, in
**2 / 21,065** cuboids. There are 566,448 records in 21,063 cuboids still
requiring parent bounds. No parent amplitude was numerically reevaluated.

The source-specific transplant passes **27/27** checks. The new records
are counted only after a bijection back to the original 5451 CSV, exact
domain containment, matching owner/term/path and positive source-geometry
margins have been verified. This is not a representative-margin transfer.

## Exact restriction argument

Let C be the certified closed parent cuboid and C=union A_i its accepted
finite cover. The 218 accepted A_i are independently checked as contained
in C, pairwise interior-disjoint, with exactly equal total volume in
binary-rational arithmetic. Since their finite union is closed, equal
volume plus containment/disjoint interiors also covers C's boundary:
a missing interior point would have an open positive-volume neighbourhood,
and the union contains the closure of C's interior.

For each original source leaf L assigned to C, the new runner verifies
L is a subset of its recorded fiber, which is a subset of C, with the
same event, branch owner, mapped cell, term, primary surface, path segment
and fixed imaginary-regulator interval. Thus every point of L is already
covered by the existing parent certificate. No assumption about another
owner, neighbouring cell or helicity sector is made.

Positive denominator, relative-root, selected-global-root and Jacobian
lower bounds restrict to L. The minimum of the accepted lower bounds is
carried downward by one binary floating-point step. For the nonnegative
absolute-integral bound, each accepted upper is carried upward before
the exact rational sum is rounded upward again. This is a deliberately
conservative bound; it is not divided by the source count, averaged over
epsilon, or rescaled by a subdomain's volume as if it were a pointwise
density. The existing proofs, rather than fresh representative samples,
supply the input enclosures.

## Overlapping regulator fibers: preserved discrepancy and repair

The initial 5514 attempt incorrectly asked the source fibers to be
interior-disjoint. They are not: the endpoint regulator boxes overlap
the adjacent regulator bins. The first attempt therefore failed, and its
failure.json, source manifest and executed script remain in the initial/
directory. This is not a failed parent bound or permission to drop leaves.

The corrected implementation evaluates the actual union: sweep the exact
epsilon endpoints, then the exact x endpoints, merging t intervals in
each resulting slab. Union volumes use Fraction.from_float on the saved
binary endpoints, with no epsilon tolerance. The E07 fibers cover C
exactly through 12 epsilon slabs, with the overlapping volume explicitly
retained in exact_coverage_audit.json. The 19 E08 fibers cover their
cuboid through four slabs without overlap.

This distinction is essential: unique source-record identities do not
imply disjoint parameter domains. Membership counts refer to records;
the integral bound is an enclosure, not a sum claiming that the regulator
cover is disjoint. Negative controls reject a missing slab, a duplicated
partition box and a one-ULP escape. Another control verifies an overlapping
union while recording its multiplicity excess rather than erasing it.

## Executed evidence

Implementation:
scripts/Y5_R2FR_5514_D4_parent_v59_exact_source_leaf_transplant.py

Validated output directory:
source-intake/functional_rg/5514/overlap-aware/

- D4_exact_source_leaf_transplant_result.json
- D4_combined_outer_cuboid_certificates.csv
- D4_certified_outer_source_leaf_map.csv
- D4_certified_outer_fiber_audit.csv
- D4_outer_coverage_frontier.csv
- exact_coverage_audit.json
- P8_Y5_BRR5513_5514_VALIDATION.csv
- source_register.csv, manifest.json, executed-script.py, completion.marker

The original source map is
source-intake/functional_rg/5451/D4_event_endpoint_xt_overlap_cover.csv.
The ordinal in the new map is a one-based DATA-RECORD ordinal, not a
physical text-line number and not a newly invented leaf identifier.
Each row carries that source file's SHA256 and its exact domain/owner.
All 606,990 outer records are scanned; only verified certified members
receive a true per-source-leaf parent-enclosure flag.

The 5467 fiber manifest and 5468 cuboid/membership tables are reconstructed
through their recorded signatures. The 5513, 5468, 5469 and 5467 historical
source registers have respectively 146, 6, 11 and 9 rows; all hashes agree.
The final source closure contains 178 unique directly or transitively
checked files. The actual count is also recorded in the result source map.

Result SHA:
380b09d07810d0c0276667686aaee586ef745914d9749fef8decfb4938669abe.

Executed script SHA:
ace8bd7ffa7a123f90649c58c5f7b9e81623cd4f155b4a8bac13a53d9872bf96.

Runtime: approximately 20.3 seconds, one logical core / BelowNormal.
The main 5513 state remains
7ab2c0b74444f4bfd3d828c0dcf36409fd771d4963ef55012fdbe734e7c2c6e6.
The 8,760-file workbench size/mtime/path fingerprint is unchanged. No
original source, historical certificate, Python cache or GitHub content
was modified.

## Next region and claim boundary

The next highest-priority uncertified cuboid is
E06__U047__RIGHT_CONNECTOR__CUBOID__3024145e0000449b,
with 39,732 source records in 1,540 fibers. It is owned by B04 and
MC04_SP_DP, unlike the completed B02 / MC04_SM_DM region. Similar widths
are not a license to copy the certificate or its denominator margins.
Any reuse requires a proved parent-expression transport with exact
bindings; otherwise use a fresh, source-scoped parent evaluation.

Full outer-parent enclosure, event-local W3, the regulator limit,
all-operator local GR and full MTS remain unclaimed. The independently
validated O4 material-response calculation is a separate physical
companion and is neither counted nor reused as a D4 certificate.

