# 4081 - Source Coupling WEP Theorem Or Eotvos Bound

- Timestamp: `2026-07-02T03:14:49+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `SOURCE_COUPLING_WEP_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED_MICROSCOPE_EOTVOS_BOUND_SOURCED`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Source-Coupling Theorem

If all ordinary matter sees one observed coframe:

```text
S_m = sum_A S_A[psi_A, e_obs; m_A, q_A, ...]
partial_Phi m_A = partial_D m_A = partial_source m_A = 0
```

then variation with respect to that same `e_obs` defines one Hilbert source:

```text
T_a^mu := e_obs^-1 delta S_m / delta e_obs^a_mu
```

and the same-frame Ward identity gives conserved stress in the same geometry. In the compact test-body monopole limit, free fall is composition independent.

So the WEP/source-coupling theorem is exact, but conditional.

## Why It Is Not Promoted

The current corpus still marks these as unsigned:

```text
q(Phi) -> e_obs descent
matter functor parent signature
species constants quotient/superselection owner
same clock/photon/orbit/source frame
EM charge/current normalization
variation order before orbital calibration
```

So current MTS does not yet claim universal source coupling.

## Eotvos Bound

MICROSCOPE gives:

```text
eta(Ti,Pt) = [-1.5e-15 +/- 2.3e-15(stat) +/- 1.5e-15(syst)]
combined sigma = 2.746e-15
one-sigma absolute envelope = 4.246e-15
```

This becomes:

```text
epsilon_WEP_source_coupling_Eotvos <= 4.246e-15
```

as a finite residual scale, not a theory pass.

## Runner Update

The runner now has finite scales for:

```text
Cassini gamma / reciprocal lock
alpha_1 preferred-frame leakage
Gdot/G drift
CODATA G calibration
MICROSCOPE WEP/source coupling
```

and a finite torsion scale with normalization pending.

Still open:

```text
spatial metric owner
theta parent
B^A derivation core
EM Hodge / Maxwell source coupling
torsion normalization map
```

## Decision

```text
same-Hilbert-source theorem = exact conditional
current source-coupling claim = false
MICROSCOPE Eotvos bound = sourced residual scale
```

## Sources

- MICROSCOPE Collaboration, `MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle`, DOI `10.1103/PhysRevLett.129.121102`, arXiv `2209.15487`.

## Next

`4082` should attack Maxwell/EM stress:

```text
same e_obs Hodge/current theorem
```

or source finite light-cone / birefringence / EM-Hodge residual bounds.
