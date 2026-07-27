# 5089 - exact double-zero runner integration smoke

Marker: `MTS_5089_EXACT_DOUBLE_ZERO_RUNNER_INTEGRATION_SMOKE`.

The 5088 guard is integrated into the live 5077 kernel runner only for
`E020__S507603_N0000__A07__primary24`. Outside that exact job, the existing
5085 numerical removable guard remains the fail-closed fallback.

A fresh execution under a new config converges, all residues are stable, both
adjacent chamber guards are exercised, and the numerical limit extension is
not invoked. A second execution resumes from cache successfully.

The integrated and standalone runs reproduce both local collision values and
the event convergence residual exactly. Their final integral differs by
`4.3376e-4` relatively because the production runner installs its
history-invariant breakpoint filter while the standalone 5088 gate did not;
this distinction is recorded rather than hidden.

## Evidence

- Result: `source-intake/functional_rg/5089/exact_double_zero_runner_integration_smoke.json`
- Smoke run: `source-intake/functional_rg/5089/exact_double_zero_runner_integration_smoke/`
- Generator: `scripts/Y5_R2FR_5089_exact_double_zero_runner_integration_smoke.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5089_VALIDATION.csv`

The integration authorizes pilot resumption only; it is not amplitude or MTS
evidence.
