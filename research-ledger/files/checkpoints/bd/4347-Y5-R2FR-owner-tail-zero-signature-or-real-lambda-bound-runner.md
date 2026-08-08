# 4347 Y5-R2FR owner-tail zero signature or real lambda bound runner

Marker: `PPC4161_OWNER_TAIL_ZERO_SIGNATURE_OR_REAL_LAMBDA_BOUND_RUNNER_4347`

Decision: `OWNER_TAIL_ZERO_THEOREM_DERIVED_SIGNATURE_GAP_OPEN_REAL_BOUND_RUNNER_READY_NONCLAIM`

## Result

4347 derives the exact owner-tail zero signature and keeps the real-bound fallback honest.

```text
constraint=0, Lambda=0, B_RI=0, I_RI=0 => Y_owner_a=0
|Y_a| <= |Pi_RI|C_Lambda|R_Lambda|/lambda_RI + |Pi_BRI||B_RI| + |Pi_I||I_RI|
```

This is progress, but not a claim: the physical positive-gap/domain row for `lambda_RI`, the boundary certificate, the no-incoming certificate and the projection constants are still required.

## Handoff

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4348-Y5-R2FR-lambda-RI-positive-domain-or-bound-input-pack.md | Can the physical static collar/domain sign lambda_RI>0, or must the owner-tail branch use a finite real denominator row? | derive Z_RI,min>0, lambda_1(D_RI)>0, M_RI,min^2-Eta_RI not too negative, fixed self-adjoint domain and no zero mode | source numeric/symbolic lower-bound rows for lambda_RI plus R_Lambda/B_RI/I_RI/projection rows and run the reduced bound |
