# Event subtraction: exact partition-local assembly and bound types

Private assembly derivation, 2026-09-07. No historical certificate is edited.

## Why this matters for the new E06 calculation

The first seeded E06 result has zero `active_material_branch_count`, despite
its source event being owned by B04. Inspection of the actual parent explains
the distinction: `active_material_branches` in
`scripts/Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py` selects the
AWAY-support segments by atlas/term. The event principal pole is separately
owned, as stated in the executable-seam section of
`5456-Y5-R2FR-D4-outer-parent-leaf-transplant-smoke.md`.

Zero in that column therefore does NOT prove zero event residue. Nor may a
raw outer-amplitude certificate silently be relabelled as a bound on its
event-subtracted remainder. The following identity supplies an exact way to
use the raw certificate without requiring that relabelling.

## 1. Keep the established parent identity

For fixed source parameters and the existing prescribed contour, write

```text
delta=E-p, Q(delta)=delta F(delta), rho=Q(0),
F=rho/delta+G, G=[Q(delta)-Q(0)]/delta.
```

This is the interface identity already derived in
`5450-Y5-R2FR-D4-event-endpoint-Cauchy-subtraction-and-correlated-probe.md`.
The pole p and residue rho are independent of the energy-path parameter,
but remain functions of the other parent variables. Charts must represent
the same normalized coefficient; unrelated residues cannot be substituted.

## 2. Subtract only where the inner certificate is used

Choose a disjoint assignment of the path to outer intervals O and connected
inner intervals I_j=[a_j,b_j]. With continuous logarithms along each prescribed
inner path, direct integration gives

```text
integral_path F dE
 = integral_O F dE
   + sum_j integral_Ij G dE
   + rho sum_j [Log_path(delta(b_j))-Log_path(delta(a_j))].
```

Nothing about this identity assumes a small residue or zero coupling.
It follows by substituting F=G+rho/delta on each inner interval only.
Adding rho times the logarithm over the FULL path on the right instead would
double-count its outer contribution. The alternative full-path subtraction
is also exact, but then the outer integrand must be G, not F.

If an outer G bound is specifically wanted, the triangle inequality gives
`|G|<=|F|+M_rho/d_min` on a domain where a sourced M_rho and positive gap
d_min are valid. This is a different, explicitly augmented certificate.
The partition-local identity avoids demanding residues at outer-only source
parameters where no inner subtraction is required.

## 3. The overlap controls artificial switching logs

The existing geometry uses R_Q=1e-5, r_inner=0.75 R_Q and
r_outer=0.50 R_Q. At an internal boundary shared by a closed inner and
outer box, both certificates apply, hence

```text
r_outer <= |delta_switch| <= r_inner.
```

An inner component whose two endpoints are such internal switches therefore
has log-modulus difference at most log(r_inner/r_outer)=log(1.5).
For a component made of s straight segments, none crossing the pole, its
continuous argument variation is at most s*pi. A valid conservative bound is

```text
|Delta Log_path delta| <= sqrt[log(1.5)^2+(s*pi)^2].
```

The winding/continuous-argument prescription is essential: principal logs
of two endpoints alone erase a possible 2*pi*i winding. Actual contour
endpoints approaching the pole are NOT artificial switches. Their singular
endpoint logarithms remain with the existing H-log/endpoint-integration
owner; the annulus bound is not assigned to them.

On each inner leaf the existing Cauchy estimate remains
`|G|<=M_Q/(R_Q-r_inner)`. The same Q certificate bounds |rho| wherever its
source-variable domain applies. The full assembly must retain these domain
bindings, rather than use an event label alone as proof of coverage.

## 4. Preserve what kind of integral was bounded

Distinguish two legitimate but different certificates:

```text
U_abs(B) >= integral_B |F| dmu,
U_int(B) >= |integral_B F dmu|.
```

A pointwise supremum times absolute path measure supplies U_abs. It remains
an upper bound after restricting to a subdomain or a weight between zero
and one. A U_int certificate alone does not: F(x)=exp(2*pi*i*x) integrates
to zero on [0,1], but its integral on [0,1/2] is i/pi.

Consequently the partition-local identity can use a bound on the exact
outer integration block it owns, or a restriction-safe U_abs certificate.
It cannot divide a signed whole-block integral bound by a leaf count or
area. Sums of nested certificates inherit U_abs only when their terminal
certificates have that property; otherwise their exact integration domain
must be retained. Parameter epsilon is not silently averaged.

The new seeded E06 record uses `POINTWISE_SUPREMUM`; its displayed integral
bound has the first, restriction-safe form. Historical path-integral methods
must be checked against their implementations before assigning that same
type during final assembly. Domain coverage counts do not by themselves
prove an independent signed-integral bound on every source leaf.

## Consequence and remaining execution

Raw outer bounds, inner-G bounds and logs restricted to the inner intervals
now have an explicit exact assembly identity. This resolves the logical
ownership choice; it does not assert that the full numerical assembly has
already been performed. Global W3 still requires the actual disjoint source
assignment, matching Q/residue domains, correctly typed integral bounds,
endpoint logarithms and the prescribed continuation/winding. No R10, PPN,
local-GR or full-MTS claim is promoted here.

## Executed controls and saved frontier

`scripts/D4_partition_local_assembly_checks_20260907.py` compiled in memory
and ran alone on 2026-09-07 at 14:27 BST, after batch1 had exited. All 17
checks passed. The analytic-control assembly error is 4.51544e-11; using the
deliberately wrong full-path logarithm with raw outer pieces gives error
0.786020. Independent winding quadrature agrees with the continuous-log
sum, while principal endpoint logs fail the winding negative control.
These are implementation/identity controls, not evaluations of the full
parent event integral.

Result: `source-intake/functional_rg/5515/assembly-identities-initial/result.json`,
SHA `f6a432b5a0ef9c4a8625a26ea981f584da4d0202e354cb9065b7a75e15faa8ec`.
Executed script SHA
`3bfc4c1cd5a0ce6ec7206ba3366d93f7dba8f8691e96c0e2d90af3558d285a5f`.
The result records its source hashes; both physical claim flags remain false.

The separate fresh-E06 batch finished with nine accepted boxes and 209
pending, zero unresolved, and 21/21 validation checks. Records 5--7 use
`V53_EXACT_UNIFORM_T_LEAF_UNION_SUM`; record 8 uses
`V54_EXACT_UNIFORM_T_LEAF_UNION_SUM`, and record 9 uses
`V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`. The inspected v53 aggregator in
`scripts/Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py`
sums its children, but that label alone does not record their terminal
integration methods. None of these aggregate labels by itself proves that
the terminal bounds were absolute-integral bounds. Retain each certificate's exact integration domain;
do not infer arbitrary restriction safety from this aggregate label. For
future assembly, retain terminal methods and domains during evaluation
instead of attempting to recover them from a compressed aggregate later.
No old numerical certificate or historical source file is changed here.
