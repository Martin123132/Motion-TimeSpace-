# 4085 - Source-Stable PPN Vector Gamma Beta Preferred Frame Gate

- Timestamp: `2026-07-02T03:49:09+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `SOURCE_STABLE_PPN_VECTOR_DERIVED_CONDITIONAL_WITH_REAL_BOUNDS_LOCAL_GR_STILL_PARENT_UNSIGNED`
- Public local-GR claim: `false`
- GitHub action: `false`

## Result

4084 gave the conditional Newton/Poisson coefficient. 4085 pushes one rung higher: the same source denominator is now carried into the PPN vector.

The fixed potential is:

```text
U = G_ref M_H / r
M_H = int rho_H dV_obs
Delta_orb = GM_orb - G_ref M_H
```

So gamma, beta and the preferred-frame/conservation terms cannot be won by redefining the mass from an orbital readout.

## Conditional PPN Theorem

If the parent branch gives:

```text
EH/EC observed metric operator
same observed coframe/readout for g_00 and g_ij
same Hilbert source denominator through O(U^2)
no extra R11/q_loc/projector spatial stress
no independent local vector/domain/coframe/memory marker
Bianchi-closed total Hilbert stress/source current
```

then:

```text
gamma - 1 = 0
beta - 1 = 0
alpha1 = alpha2 = alpha3 = 0
xi = 0
zeta1 = zeta2 = zeta3 = 0
Gdot/G = 0
```

This is a real forward move: the PPN target is no longer vague. The theorem has exact antecedents and a componentwise empirical scorecard.

## Real Bound Rows Added

The 4085 bound table now includes:

```text
|gamma-1| <= 2.3e-5
|beta-1| <= 8.0e-5
|alpha1| <= 1.0e-4, with stronger companion row 4.0e-5
|alpha2| <= 2.0e-9
|alpha3| <= 4.0e-20
|xi| <= 4.0e-9
|zeta1| <= 2.0e-2
|zeta2| <= 4.0e-5
|zeta3| <= 1.0e-8
|Gdot/G| <= 1.3e-12 yr^-1 staged conservative envelope
```

`zeta4` is explicitly not treated as an independent bound in the selected Will Table 4 convention.

## What Improved

This checkpoint closes the “just circling missingness” failure mode for PPN: the missing clauses are now theorem antecedents with hard consequences. The next job is not to list them again; it is to prove the parent action enforces them or compute the residual vector.

## What Remains Unsigned

```text
parent EH/EC operator signature
same-frame observed coframe/readout map
Pi_M/H_tau/Hilbert source denominator equality through O(U^2)
no-extra R11/q_loc/projector spatial stress
preferred-frame/domain/memory silence
Bianchi/source-current closure
constant local coupling/Gdot branch
```

## Decision

```text
source-stable PPN theorem = exact conditional
empirical PPN bounds = source-backed
local GR claim = still false
next gate = parent EH operator signature or non-EH/R11 projection
```

## Sources

- Clifford M. Will, *The Confrontation between General Relativity and Experiment*, Living Reviews in Relativity, Table 4.
- Bertotti, Iess and Tortora, *A test of general relativity using radio links with the Cassini spacecraft*, Nature 425, 374-376, DOI `10.1038/nature01997`.

## Next

```text
4086-Y5-R2FR-parent-EH-operator-signature-or-nonEH-R11-projection.md
```

That is the clean route of attack: either prove the parent really gives the EH same-source branch, or force the extra MTS operators to show their PPN-size residuals in the open.
