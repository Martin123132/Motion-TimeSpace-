# 5084 - recoil-source local Cauchy theorem

Marker: `MTS_5084_RECOIL_SOURCE_LOCAL_CAUCHY_THEOREM`.

Checkpoint 5083 generalizes only under explicit analytic guards. At an
isolated cross-additive collision `q0 != 0`, an owned pole from recoil source
`direct:g1` or `direct:g2` has zero global-first, relative-second local
residue when it is isolated from all other direct poles and the recoil
kinematics are regular.

The proof again uses `I=D+S`: source separation removes `S` from the owned
local global cycle, parameter-dependent Cauchy integration makes the direct
residue holomorphic at `q0`, and `1/q` is holomorphic there. This proof does
not include `direct:g3`, which aliases `subtraction:soft`; the old stable
nonzero `g3` examples are therefore counterexamples to 5041 but not to this
corrected theorem.

The historical 5035 run contains 601 stable nonzero cross-source rows and no
counterexample satisfying all corrected guards. Two existing 70-digit `g1`
witnesses and independent `g2` witnesses at `A00` and `A01` pass. For the
new `A01` witness, the residue contracts from about `1.195e-16` to
`1.823e-21` with the expected `2^16` radius scaling.

## Evidence

- Theorem: `source-intake/functional_rg/5084/recoil_source_local_cauchy_theorem.json`
- New witness: `source-intake/functional_rg/5084/g2_A01_arbitrary_precision_witness.json`
- Falsification audit: `source-intake/functional_rg/5084/stable_nonzero_falsification_audit.csv`
- Generator: `scripts/Y5_R2FR_5084_recoil_source_local_cauchy_theorem.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5084_VALIDATION.csv`

The 5077 runner applies this theorem only after every row-level guard passes
and fails hard if a stable nonzero row would be overwritten. The broad 5041
theorem remains quarantined.
