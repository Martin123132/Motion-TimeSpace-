# 4946 - QCD TJJ matching theorem and local Maxwell contract

Marker: `MTS_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT_4946`.

Date: `2026-07-13`.

Status: private analytic, source-acquired and source-executed checkpoint. The
QCD photon-curvature problem has been taken to its actual mathematical
boundary. A finite hadronic coefficient cannot be obtained from hadronic
vacuum polarization, electromagnetic form factors, gravitational form factors
or the trace anomaly alone: an allowed finite local `CFF` contact changes the
transverse-traceless `TJJ` response while leaving every one of those lower
observables unchanged. This is proved by an explicit counterterm direction,
not recorded as another unspecified missing input. The identifying
three-point function, its subtracted dispersive representation and a
lattice-ready projector are constructed. Independently, the local Maxwell
action, current, field equation, stress tensor and conservation law are now
derived with one universal higher-derivative calibration coefficient.

## 1. QCD generating functional and identifying observable

Define the renormalized QCD source functional

```text
exp(iW_QCD[g,A])
 =integral Dq DG exp(iS_QCD[q,G;g,A]).
```

The required electromagnetic stress-current-current vertex is

```text
Gamma_TJJ^(mnab)(q,p,k)
 =delta^3 W_QCD/
  [delta g_mn(q) delta A_a(p) delta A_b(k)],

q+p+k=0.
```

The primary TJJ source gives a 13-form-factor representation before Ward and
Bose constraints and a four-form-factor transverse-traceless representation
after the constraints. The relevant low-momentum component is the Weyl
projector `P_C`, normalized by

```text
P_C V_CFF=1,
```

and chosen to annihilate the Maxwell vertex, `RF^2`, `RicciFF` and on-shell
EOM-redundant photon-derivative representatives. Since a local `CFF` vertex
contains two derivatives in curvature and one in each field strength,

```text
c_QCD^r(mu)
 =lim_(epsilon->0) epsilon^-4
  P_C[Gamma_TJJ(epsilon q,epsilon p,epsilon k)
      -Gamma_Maxwell(epsilon q,epsilon p,epsilon k)].
```

This is the precise quantity that checkpoint 4944 could not replace with
free current-quark masses or pointlike hadron anchors.

## 2. Exact lower-observable non-identifiability theorem

Consider two low-energy functionals differing by the finite local term

```text
delta W
 =delta c integral d^4x sqrt(-g)
  C_mnrs F^mn F^rs.
```

This term obeys the declared gauge, diffeomorphism and CP symmetries. The
curved-ChPT sources establish that curvature introduces additional local LECs
which can vanish in flat spacetime while contributing to stress responses;
the mesonic `p^6` source independently establishes external-source contact
terms and finite renormalized LECs.

Now vary the finite deformation against the available lower observables:

```text
flat HVP:
  delta^2(delta W)/delta A delta A |_(g=eta)=0
  because C[eta]=0;

one-current hadron EM form factor:
  delta(delta W)/delta A=0
  because the term is quadratic in F;

one-stress hadron GFF:
  delta(delta W)/delta g |_(A=0)=0
  because F=0;

flat gamma-gamma data:
  delta(delta W)=0
  without a metric/curvature insertion;

dimension-four trace-anomaly coefficient:
  does not fix the independent flat-background Weyl/TT contact;

electromagnetic TJJ:
  delta Gamma_TJJ=delta c V_CFF !=0.
```

Thus arbitrary values of `delta c` reproduce all HVP, one-current EM, one-
stress GFF and flat photon data while predicting different curved-photon
propagation. No combination of those lower data can derive or rigorously
bound `c_QCD^r`. This counterexample also proves that fitting separate EM and
gravitational form factors is insufficient.

## 3. Why a simple spectral integral cannot close it

For a projected invariant `F_C(q^2)`, the low-energy representation has at
least the form

```text
F_C(q^2;mu)
 =c_QCD^r(mu)
  +(q^2/pi) integral_(s0)^infinity ds
    Im F_C(s)/[s(s-q^2-i0)]
  +possible higher subtraction polynomial.
```

The local coefficient is the subtraction constant. A finite contact shift
changes it without changing the spectral discontinuity. Therefore an
unsubtracted relation would itself be an additional UV falloff assumption.
No acquired QCD or chiral source proves that assumption, and the required
transverse-traceless helicity spectral combination is not positive definite.

Consequently

```text
rigorous HVP/GFF spectral bound on c_QCD = false;
zero QCD contact from dispersion             = false;
trace anomaly determines CFF                = false.
```

This is the reason the derivation stops here analytically; adding a finite
number would be a closure assumption.

## 4. Lattice-ready first-principles matching

The coefficient remains calculable from QCD. The acquired lattice source
constructs a correctly normalized conserved energy-momentum tensor using
gradient flow for theories with fermions. It also requires the continuum
limit before the zero-flow-time limit.

A valid computation must evaluate

```text
<T_mn J_EM,a J_EM,b>_connected+disconnected+contacts
```

and pass:

```text
p_a Gamma_TJJ^(mnab)=0,
k_b Gamma_TJJ^(mnab)=0,

q_m Gamma_TJJ^(mnab)
 =independently calculated HVP pinched/contact combination,

Gamma_TJJ^(mnab)(q,p,k)
 =Gamma_TJJ^(mnba)(q,k,p),

P_C V_Maxwell=P_C V_RF2=P_C V_RicciFF=P_C V_EOM=0.
```

The calculation then needs physical quark masses, connected and disconnected
current contractions, finite-volume control, the continuum limit, a valid
flow-time window and conversion into the checkpoint-4944 renormalization
scheme. This is a complete estimator and acceptance contract; no lattice
number is fabricated on this laptop.

## 5. Physical coefficient without double counting

When the QCD result is supplied, the pointlike pion and kaon anchors are
replaced rather than added. The physical coefficient is

```text
c_IR=c_nonQCD+c_QCD^r(mu),
```

where the presently controlled non-QCD interval is

```text
-9.621794773635e-31
 <=c_nonQCD<=
-9.621794073504e-31 m^2.
```

This interval contains the parent, free leptons and the charged-`W` magnitude
envelope. The exact `W` sign is immaterial at the displayed scale but remains
inside the interval.

For sensitivity only,

```text
c_NDA(1 GeV)
 =alpha/(4pi)(hbar c/1 GeV)^2
 =2.26114e-35 m^2.
```

A coefficient `K=425.5` in these units reaches one percent of the lepton
subtotal, and `K=4.2553e4` matches it. Even `(4pi)^2` gives only `0.371%`.
These are diagnostic scales, not a QCD bound; every row is explicitly marked
nonclaim.

## 6. Local Maxwell action and source coupling

The local electromagnetic action is

```text
S_EM
 =integral sqrt(-g)[-F_mn F^mn/4+c_IR C_mnrs F^mn F^rs]
  +integral sqrt(-g) A_m J^m,

J^m=-(1/sqrt(-g)) delta S_matter/delta A_m,
nabla_m J^m=0.
```

Varying `A_n` gives

```text
nabla_m F^mn
 -4c_IR nabla_m(C^mnrs F_rs)
 =J^n,

nabla_[m F_nr]=0.
```

Metric variation gives

```text
T_EM,mn
 =F_ma F_n^a-g_mn F^2/4+c_IR H_CFF,mn,

H_CFF,mn
 =-(2/sqrt(-g)) delta/delta g^mn
   integral sqrt(-g) C_abcd F^ab F^cd.
```

Because both pieces come from one diffeomorphism-invariant action, the same
`c_IR` controls propagation and stress. On the coupled equations,

```text
nabla^m(T_EM,mn+T_matter,mn)=0.
```

No extra energy-exchange closure or arena-dependent stress coefficient is
introduced. On flat spacetime, `C_mnrs=0`, so the Maxwell equation and standard
Maxwell stress are exact for every value of `c_IR`.

This closes the structural Maxwell/EM-stress route. It does not derive `U(1)`
or the visible matter current from motion alone; those remain explicit parent
data, just as checkpoint 4943 states.

## 7. One-datum calibration contract

There are two legitimate routes:

```text
prediction route:
  calculate c_QCD^r from the lattice TJJ estimator;

calibration route:
  fit c_IR once from a robust curved-photon experiment,
  then transfer it without retuning.
```

For every system,

```text
signed Delta v_pol/c
 =K_system(c_nonQCD+c_QCD^r),

K_system=12M_geom/r^3.
```

The generated transfer table supplies all five slopes. The `10^-6` sensitivity
thresholds for `|c_IR|` are approximately

| system | `|c_IR|` producing `10^-6` split |
|---|---:|
| Earth | `4.86e15 m^2` |
| Sun | `1.90e16 m^2` |
| white dwarf | `1.94e10 m^2` |
| neutron star | `69.7 m^2` |
| ten-solar-mass horizon | `145 m^2` |

These numbers design future tests; they are not claims that the compact
linearized formula remains valid for the old large pulsar envelope. A small
measured or lattice coefficient can be transferred; a large value must first
pass the arena's EFT-control gate.

## 8. Claim boundary

```text
HVP/GFF data-only QCD no-go theorem           = proved;
subtracted TJJ dispersion relation            = derived;
finite rigorous QCD spectral bound            = false;
lattice TJJ matching estimator                = defined;
numeric QCD TJJ match                         = false;
non-QCD coefficient interval                  = assembled;
local Maxwell action and field equation       = derived;
Maxwell plus CFF stress and conservation      = derived;
exact flat Maxwell limit                      = derived;
one-coefficient calibration contract          = defined;
general curved-Maxwell precision promotion    = false;
full MTS fixed point                          = false.
```

## 9. Next target

`4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md`

Put the metric pole residue `G_N`, photon normalization/charge, motion gap and
curvature-photon Wilson coefficient into one parent calibration ledger. Derive
the Poisson, geodesic and Lorentz-force residues from the unchanged action,
count the genuinely independent empirical inputs, and prove or reject that no
local arena needs an extra source normalization.

