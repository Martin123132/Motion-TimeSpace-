# 4272 - Y5 R2FR parent no-extra-frame signature or c_g/b_dis first bound runner

Packet marker: `PPC4161_PACKET_PARENT_NO_EXTRA_FRAME_SIGNATURE_OR_CG_BDIS_FIRST_BOUND_RUNNER_4272`

## Result

The public no-extra-frame parent signature remains unsigned. I did not promote the private same-frame selector.

Instead, 4272 builds the finite frame-vector runner:

```text
c_g / b_dis / alpha_eff -> PPN/R10/clock/WEP-style bounds
```

with strict refusal of raw `c_g` scoring.

## Why this matters

The local-GR route now has a practical fork:

```text
derive parent no-extra-frame
or
fill scoreable frame-vector inputs
```

No more generic "coframe missing" fog.
