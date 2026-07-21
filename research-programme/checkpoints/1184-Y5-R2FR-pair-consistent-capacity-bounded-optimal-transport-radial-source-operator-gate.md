# 5168 - Pair-consistent capacity-bounded optimal-transport radial source operator

Marker: `MTS_5168_PAIR_CONSISTENT_OPTIMAL_TRANSPORT_SOURCE_OPERATOR_GATE`.

Date: `2026-07-21`.

## The obstruction proved

Checkpoint 5167 derived a pair-mean radial cooling/freefall clock but retained
homologous donor removal. Assigning the raw cooled shell profile independently
to each antithetic phase is not allowed. If `rbar_i` is the desired pair source,
`a_si` is phase `s`'s actual baryon capacity and
`x_-i=rbar_i+delta_i`, `x_+i=rbar_i-delta_i`, then

```text
max(-rbar_i,rbar_i-a_+i) <= delta_i
                         <= min(a_-i-rbar_i,rbar_i),
sum_i delta_i=0.
```

At every tested resolved partition with two or more radial bins, these bounds
have no zero-sum solution. Only the one-bin, fully homologous endpoint is
feasible. This proves why the direct shell-to-phase map generated artificial
`25 versus 4 Gyr` endpoints: it violated a real phase-capacity obstruction.

## Derived operator

The minimal repair is a constrained one-dimensional transport flow `f_isj`:

```text
min sum_i,s,j f_isj |r_i-r_j|^p/R_edge^p,
sum_s,j f_isj=2 rbar_i,
sum_i,j f_i,-,j=sum_i,j f_i,+,j=M_c,
sum_i f_isj <= a_sj,
f_isj >= 0.
```

`p=1` is primary; `p=2` is a frozen norm comparator. The primary radial
partition has `26` bins, inherited from the checkpoint-5166
resolved clumping scale rather than selected from `q`.

The primary operator requires mean absolute radial transport
`22.110619352735302 kpc` and RMS transport
`48.54166468669157 kpc`. Its projected pair profile
changes by L1 mass fraction `0.48996626692208395`.
Across `(13, 20, 26, 52)` bins the mean absolute displacement range is
`[21.58391328746118, 22.20984793120233]`. The transport is therefore a
finite, resolution-stable physical correction, not an infinitesimal numerical
repair.

## All-time identities

Endpoint transport fractions are lifted through each shell's sourced arrival
time. For every sampled time and all four thermal branches,

```text
x_sj(t)>=0,
x_sj(t)<=a_sj,
Delta M_s,edge(t)=-sum_j x_sj(t)+lambda_s(t)M_c=0,
[lambda_-(t)+lambda_+(t)]/2=lambda_bar(t).
```

The largest pair-time residual is
`2.220446049250313e-16` and the largest capacity
violation is `3.814697265625e-06 Msun`.

## Decision

`RAW_PAIR_RADIAL_REMOVAL_IS_CAPACITY_INFEASIBLE_FOR_SEPARATE_ANTITHETIC_PHASES_BUT_A_MINIMUM_RADIAL_TRANSPORT_OPERATOR_NOW_SATISFIES_BOTH_PHASE_CAPACITIES_BOTH_ENDPOINTS_AND_THE_PAIR_TIME_IDENTITY_WITHOUT_READING_Q`.

The operator is now sufficiently specified for a forward force calculation,
but this checkpoint does not read `q` and makes no galaxy claim. Its radial
transport metric is still a reduced variational matter closure, not a full
radiation-hydrodynamic derivation. The next gate must evolve the `p=1` operator
for all four predeclared clocks and use `p=2` only as a closure-norm robustness
test.

```text
raw independent phase assignment feasible                 = no;
capacity-bounded pair transport solved                     = yes;
phase endpoint mass exact                                  = yes;
pair source supply exact                                   = yes;
all-time pair and phase mass identities                    = yes;
q or rotation target used                                  = no;
forward force response executed                            = no;
local GR/Newton/Maxwell branch modified                    = no;
galaxy or full-MTS claim                                   = false.
```

All `16` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
