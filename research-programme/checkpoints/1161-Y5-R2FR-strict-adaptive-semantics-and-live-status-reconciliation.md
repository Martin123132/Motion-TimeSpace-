# 5145: Strict adaptive semantics and live-status reconciliation

## Root correction

An adaptive full-remainder row is now converged only when every adaptive order
both reports convergence and has maximum chamber-relative error below the
locked tolerance. The fixed-event gate, kernel status, cache acceptance,
locked-next selection and replay validation all enforce the same condition.

## Reconciled state

All 51 existing full-remainder rows were reconciled against checkpoint 5144.
Forty-nine remain strict passes. The E040/A10 baseline and E020/A10 repaired
row are demoted to `COMPLETED_UNCONVERGED`; their frozen pre-repair witnesses
remain byte-identical. The run is now `{'completed_converged': 50, 'completed_unconverged': 2, 'failed': 0, 'missing': 508}` and the first incomplete
locked row is `E040__S512503_N0000__A10__primary24`.

No tolerance, interval cap or physics parameter changed. The next task is to
localize the exhausted adaptive leaves shared by the A10 pair and derive a
geometric partition repair before rerunning either row.
