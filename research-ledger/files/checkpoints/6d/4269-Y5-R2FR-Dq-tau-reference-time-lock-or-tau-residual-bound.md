# 4269 - Y5 R2FR Dq-tau reference-time lock or tau residual bound

Packet marker: `PPC4161_PACKET_DQ_TAU_REFERENCE_TIME_LOCK_OR_TAU_RESIDUAL_4269`

## Result

4269 adopts:

```text
Dq_tau = 0.0,
Dq_tau_C1 = 0.0
```

for the q-basic observed-tau/reference-time branch only.

## Human translation

This says the local clock/source/orbit/readout time used in tests is one parent-selected observed time, chosen before variation and before comparison. If we secretly use one time for source charge, another for clocks, another for orbits, or a private memory time that leaks into clocks, that is not zero; it becomes a residual.

## Why this is progress

4254 had two live Dq holdouts after 4268:

```text
Dq_geom,
Dq_tau.
```

4269 removes the tau leg under a precise branch contract. That leaves the real hard piece: geometry/coframe descent plus the numeric tomography constants.

## Claim firewall

This is private and nonclaim. It does not prove public local GR and does not derive a universal theory of time. It only locks the observed tau row used by local tests.
