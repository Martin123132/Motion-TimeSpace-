# 4281 - cGamma transport/Bgrad routing zero or profile source pack

Marker: `PPC4161_CGAMMA_TRANSPORT_BGRAD_ROUTING_ZERO_OR_PROFILE_SOURCE_PACK_4281`

Decision: `FINITE_MARGIN_LOCAL_COLLAR_ZERO_DERIVED_TRANSITION_SHELL_REMAINS_PROFILE_OR_QUARANTINE_NONCLAIM`

4281 proves a restricted support-zero branch:

```text
finite-margin W_loc away from transport/B-gradient support
=> R_transport_to_local = R_Bgrad_to_local = 0
=> A_J,eff_private = 0.
```

It also blocks the overclaim:

```text
transition shell has P_loc=1 and fails direct local projection,
so transition support still needs exact cancellation/quarantine or real profile rows.
```
