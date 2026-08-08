# 4257 - Y5 R2FR projector certificate and spectral-gap runner

Packet marker: `PPC4161_PACKET_PROJECTOR_CERTIFICATE_AND_SPECTRAL_GAP_RUNNER_4257`

## Result

4257 makes the coupling/local-GR bottleneck computational:

```text
sigma_0^2 = lambda_min(G^(-1/2) J^T W J G^(-1/2)),
C_HDq = 1/sigma_0.
```

It also audits the projector:

```text
P^2=P,
J P=0,
rank(P)=nullity(J).
```

## Current verdict

The H_q annihilation and Hperp split are signed. The full projector/range and spectral-gap rows are not. Claim remains false.

## Next action

Fill `P8_Y5_R2FR_4257_DQ_GAP_MATRIX_CANDIDATE.csv` from parent/source rows, or attack the eight Dq component zeros directly.
