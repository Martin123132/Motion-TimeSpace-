# 5144: Strict adaptive-status audit and witness freeze

## Finding

All `51` existing full-remainder rows were reclassified using the
actual adaptive criterion rather than their stored status label. `49`
pass. Exactly two rows are false-positive `COMPLETED_CONVERGED` labels:

- `E040__S512503_N0000__A10__primary24`: error
  `0.0001646982643542806`.
- `E020__S512503_N0000__A10__primary24`: error
  `0.00021516344483054253`.

Both exceed the unchanged `5e-5` tolerance and exhaust the same adaptive
interval budget. The older E040 baseline therefore fails the same test. This
supports a shared quadrature/status defect, not an MTS-only adverse result.

## Discipline

Every mismatched live job and kernel is frozen byte-for-byte before repair;
the 5143 gate, result, status, validation and console log are also frozen. This
checkpoint does not mutate the live run. Next, correct convergence semantics,
demote both rows fail-closed and localize the exhausted adaptive leaves before
rerunning either row. No tolerance or physics parameter is changed, and the
formalization hash remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
