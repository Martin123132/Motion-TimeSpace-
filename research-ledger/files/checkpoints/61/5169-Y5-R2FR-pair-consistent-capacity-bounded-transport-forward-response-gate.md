# 5169 - Pair-consistent capacity-bounded transport forward response

Marker: `MTS_5169_PAIR_CONSISTENT_TRANSPORT_FORWARD_RESPONSE_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5168 constructed a radial source operator but deliberately did not
run the response. This gate asks the non-inverted question: when that frozen
operator is replayed on the original particle states, does it improve the
galaxy response without reading the parent `q` target?

## Forward initial-value problem

For source bin `i`, phase `s`, and Lagrangian donor sink bin `j`, the endpoint
flow `f_isj` is the checkpoint-5168 constrained optimum. Its time lift is

```text
Delta M_sj(t)=sum_i f_isj M_i,arrived(t)/M_i,endpoint,
lambda_s(t)=sum_j Delta M_sj(t)/M_c,
Delta M_visible,s(t)=lambda_s(t) M_c.
```

Each donor particle in sink `j` loses the same fraction of its available
baryon mass. The same mass is deposited in the measured visible profile in
that phase, so phase and pair mass identities hold while the inherited central
force remains

```text
a=-G_N M_enclosed(t) r/(r^2+epsilon^2)^(3/2).
```

All runs use the full original antithetic particle states. No compressed state,
response efficiency, `q`, or rotation target enters the transport solution.

## Primary results

- `ISOCHORIC_Z0.1_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: q=`2.2468474728387435`, RMSE=`0.2850806581897878` dex, compatible=`False`
- `ISOCHORIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: q=`2.26699412921067`, RMSE=`0.2822731967466959` dex, compatible=`False`
- `ISOBARIC_Z0.1_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: q=`2.269361831204709`, RMSE=`0.282861104216976` dex, compatible=`False`
- `ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY`: q=`2.234007139940017`, RMSE=`0.27740773926786666` dex, compatible=`False`

The fitted parent interval is
`[1.511977636680018, 2.20499007120595]`; the free baseline
RMSE is `0.42140386547507747 dex`. The closest primary result is
`ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY` with gap
`0.029017068734066953`.

Relative to checkpoint 5167 homologous removal, the four transport shifts in
`q` are `[-0.01446333112386844, 0.03439447274473473, -0.02366366450321289, 0.01661860574851337]` and the RMSE shifts are
`[0.017918598130747976, 0.017914784813923557, 0.01945869496635555, 0.01782353193640357]`.
For the selected branch, where checkpoint 5167 also ran the full particle
state, the matched shifts are `Delta q=0.01720705206218609`
and `Delta RMSE=0.018081789772517787` dex.

## Frozen controls

The checkpoint-5167 nearest branch, isobaric `Z=0.3 Zsun`, was selected using
the previous checkpoint's `q` only for numerical controls and was declared
before this response was read. It did not define the transport operator or any
primary physics branch. The results are:

- `TIME_REFINEMENT`: q=`2.2358570186820326`
- `NORM_CONTROL`: q=`2.2338814558909474`
- `RESOLUTION_CONTROL_N13`: q=`2.236200096911821`
- `RESOLUTION_CONTROL_N52`: q=`2.2298452601092236`

The maximum selected-control displacement from its primary `q` is
`0.0041618798307934135`. The operator uses mean radial
transport `22.110619352735302 kpc` and no
control is refitted to improve the score.

## Decision

`FROZEN_PAIR_CONSISTENT_TRANSPORT_DOES_NOT_CLOSE_THE_PARENT_RESPONSE_GATE_SO_VISIBLE_ASSEMBLY_IS_RETAINED_AS_A_BOUNDED_SOURCE_HISTORY_AND_PARENT_COLLECTIVE_STRESS_TAKES_PRIORITY`.

This checkpoint is an empirical gate on a reduced source closure, not a claim
that optimal transport has been derived from the parent field action. It does
not modify or validate the local GR/Newton/Maxwell branch. A favorable response
would justify deriving this operator from stress-energy and angular-momentum
transport; an unfavorable response would bound visible assembly and return
priority to the collective-stress/parent-coupling route.

```text
checkpoint-5168 operator replayed forward             = yes;
all four physical clocks run                           = yes;
full antithetic particle states used                   = yes;
phase endpoint mass conserved                          = yes;
q used to define or fit operator                       = no;
local GR/Newton/Maxwell branch modified                = no;
galaxy or full-MTS claim                               = false.
```

All `20` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
