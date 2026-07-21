# 5167 - Radial entropy cooling, freefall transfer and forward-response gate

Marker: `MTS_5167_RADIAL_ENTROPY_COOLING_FREEFALL_TRANSFER_GATE`.

Date: `2026-07-21`.

## Why this calculation

Checkpoint 5166 replaced the arbitrary galaxy assembly duration with a real
CIE luminosity, but its one global coordinate cooled half the source too early.
Both predeclared branches improved the profile while missing the parent `q`
interval. This checkpoint removes the approximation that failed instead of
retuning its duration.

## Radial derivation

Each inherited hot-baryon shell now obeys the checkpoint-5166 entropy equation

```text
rho de_th/dt=-C n_H^2 Lambda(n_H,T,Z).
```

Two standard thermodynamic projections are carried together:

```text
t_cool,V=integral rho d[3kT/(2 mu m_p)]/[C n_H^2 Lambda],
t_cool,P=integral rho(T) d[5kT/(2 mu m_p)]/[C n_H(T)^2 Lambda],
n_H(T)T=constant on the isobaric branch.
```

The temperature integral runs from the sourced fixed-edge virial temperature
`1314274.0487669532 K` to the predeclared atomic floor
`10000.0 K`. The same Cloudy/Grackle CIE table supplies `Lambda` and
`mu(T,n_H)` at every integration point. The resolved checkpoint-5166 clumping
`C=1.5385341412037419` is fixed before any response is read.

After reaching the floor, each shell receives the same calibrated-`G_N`
Newtonian arrival bound

```text
t_arr(r)=t_cool(r)+pi sqrt[r^3/(G_N M_tot(<r))]/(2 sqrt(2)).
```

Shells are ranked by `t_arr` until their mass exactly equals the measured
condensed endpoint. Their cumulative pair-mean arrival distribution defines
`lambda_arr(t)`. It drives the checkpoint-5164 per-phase identity:

```text
m_gi(t)=m_pi-lambda_arr(t) Delta m_phase d_i,
N_d Delta m_phase=M_c(Redge),
M_cond(<r,t)=lambda_arr(t) M_c,obs(<r).
```

This avoids assigning the pair-mean shell ranking separately to antithetic
phases with deliberately different halo masses. The clock is radial and
source-derived; donor removal remains the already-controlled homologous
checkpoint-5164 projection. No response efficiency, duration fit, metallicity
inversion or arena-specific gravitational coefficient is introduced.

## Forward results

The four branches were declared as the Cartesian product of isochoric/isobaric
cooling and `Z={0.1,0.3} Zsun` before `q` was evaluated:

```text
ISOCHORIC_Z0.1_RADIAL_COOLING_FREEFALL: T=6.1687579867177185 Gyr, q=2.261310803962612, RMSE=0.2671620600590398 dex, v2 ratio=0.3891114160440698
ISOCHORIC_Z0.3_RADIAL_COOLING_FREEFALL: T=3.6215880802909113 Gyr, q=2.2325996564659354, RMSE=0.2643584119327723 dex, v2 ratio=0.3956845144551674
ISOBARIC_Z0.1_RADIAL_COOLING_FREEFALL: T=4.852653732169362 Gyr, q=2.293025495707922, RMSE=0.2634024092506205 dex, v2 ratio=0.39535748557947414
ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL: T=2.6663381340429857 Gyr, q=2.2173885341915036, RMSE=0.2595842073314631 dex, v2 ratio=0.4033561123062301
```

The inherited parent interval is
`1.511977636680018 .. 2.20499007120595` and the free
baseline RMSE is `0.42140386547507747 dex`. All four near-boundary
branches are repeated at doubled time resolution. Their refined values and
primary/refined differences are `{'ISOCHORIC_Z0.1_RADIAL_COOLING_FREEFALL': 2.261121428524268, 'ISOCHORIC_Z0.3_RADIAL_COOLING_FREEFALL': 2.24551025779569, 'ISOBARIC_Z0.1_RADIAL_COOLING_FREEFALL': 2.2947321954941886, 'ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL': 2.210775108908433}` and
`{'ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL': 0.00661342528307074, 'ISOCHORIC_Z0.1_RADIAL_COOLING_FREEFALL': 0.0001893754383441859, 'ISOBARIC_Z0.1_RADIAL_COOLING_FREEFALL': 0.0017066997862666966, 'ISOCHORIC_Z0.3_RADIAL_COOLING_FREEFALL': 0.012910601329754634}`. A branch is called numerically
compatible only when its primary/refined interval intersects the parent band;
no single favorable discretization is promoted by itself. The closest branch,
`ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL`, is also repeated with every inherited
particle because its primary distance from the band is smaller than the
checkpoint-5164 particle-resolution envelope. That value is
`2.216800087877831` with
`|Delta q|=0.0005884463136727192`. The closest controlled
point is `ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_TIME_REFINEMENT` at `q=2.210775108908433`, only
`0.0057850377024828425` above the parent band.

## Decision

`RADIAL_ENTROPY_COOLING_AND_FREEFALL_REMOVES_MOST_OF_THE_GLOBAL_CLOCK_SLOPE_ERROR_BUT_ALL_REFINED_POINT_ESTIMATES_REMAIN_NARROWLY_ABOVE_THE_PARENT_Q_BAND`.

This is still not a full radiation-hydrodynamic derivation. Isochoric and
isobaric shell laws are controlled brackets, the radial arrival distribution
drives a homologous donor transfer, the observed condensed shape grows self-
similarly, feedback and angular-
momentum transport are absent, and the UGC09133 hot metallicity remains
unmeasured. The checkpoint tests whether removing homologous timing moves the
same theory in the required direction without fitting the response.

```text
local entropy cooling times derived from real table       = yes;
Newtonian shell freefall derived                           = yes;
pair-mean radial arrival clock derived                     = yes;
checkpoint-5164 homologous donor removal mass-conserving   = yes;
shell rank assigned separately to antithetic phases        = no;
four branches fixed before q                               = yes;
full radiation hydrodynamics                               = no;
local GR/Newton/Maxwell branch modified                    = no;
galaxy or full-MTS claim                                   = false.
```

All `21` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
