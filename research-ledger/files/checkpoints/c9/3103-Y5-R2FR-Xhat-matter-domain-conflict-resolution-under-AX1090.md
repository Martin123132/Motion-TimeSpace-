# 3103 - Y5 R2FR Xhat matter-domain conflict resolution under AX1090

**Purpose:** continue the `3102` branch properly. The task is not to say “these couplings are missing”; it is to decide what the parent action allows. This checkpoint resolves the direct `Xhat` matter/constant/source conflicts into a parent-domain rule.

## Inputs Used

- `3102` proposes quotient-descended ordinary matter and `NoSourceOnlySpeciesSlot`.
- `1046` lists shadow-frame, constant, marker, and source-weight countermodels.
- `1048` sharpens the EM/mass/clock forbidden-vertex problem.
- `1338` sharpens `NoSourceOnlySpeciesSlot`.
- `1418` shows why a single action-scale/current owner is needed for source weights.

## Parent Matter Domain Rule

Adopt the following as the preferred local-GR branch:

```text
Q_obs := P_parent / ~
q : P_parent -> Q_obs
v_X in ker(Dq)
e_pub = e_pub(q(Phi))

S_matter =
  sum_A S_A[
    Psi_A,
    e_pub(q(Phi)),
    omega[e_pub],
    theta_A(q(Phi), representation_A)
  ]
```

with one parent action measure/current owner:

```text
mu_matter = mu_obs(q(Phi))
hbar_parent = universal
T_total := delta S_matter / delta e_pub
```

and no morphism:

```text
SpeciesLabel -> Coeff_active_source
```

This is the `NoSourceOnlySpeciesSlot` closure: species labels may select representation data, masses/charges inside `theta_A`, and internal quantum numbers, but not an active gravitational source multiplier.

## Conflict Resolution Table

| conflict | forbidden in quotient-matter branch | if not forbidden |
|---|---|---|
| `A_A(Xhat)e_pub` conformal frame | `A_A` must factor through `q`, so `Lie_v ln A_A=0`; hence `c_g=b_conf=0` | retain `c_g/b_conf` with PPN/R10/WEP projections |
| `B_A(Xhat)` disformal frame | no independent disformal matter-frame slot | retain `b_dis` in PPN/clock/preferred-frame residual vector |
| `f_X(Xhat)F^2` or `alpha_EM(Xhat)` | EM gauge kinetic norm is quotient/topological/representation-owned | retain `b_alpha` for clocks, spectra, WEP, EM binding |
| `m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat)` | matter spectrum and dimensionless ratios are quotient-owned or representation-superselected | retain `b_mA, b_mu, b_nuc` for WEP/clocks/R10 |
| `clock_i(Xhat)` | clock ratios derive from quotient-owned constants and matter spectrum | retain `b_clock_i` |
| `material_marker_A(Xhat)` | material labels are discrete representation/source preparation data, not smooth `Xhat` fields | retain `b_marker` |
| `S_matter=sum_A w_A S_A` | one parent action measure/current owner; no source-only species slot | retain `Delta_w_A/qbar_source_weight` |
| `S_source=sum_A kappa_A J_A` | active source is the Hilbert/coframe variation of the same matter action | retain `delta_kappa_A/current_rescaling` |

## Resulting Zero Lemma

If:

```text
v_X in ker(Dq)
S_matter = sum_A S_A[Psi_A,e_pub(q(Phi)),omega[e_pub],theta_A(q(Phi),representation_A)]
NoSourceOnlySpeciesSlot
single parent action measure/current owner
```

then every ordinary-matter vertical derivative vanishes except explicitly retained residual fields:

```text
delta_X e_pub = 0
delta_X theta_A = 0
delta_X mu_matter = 0
delta_X hbar_parent = 0
delta_X S_matter = 0
```

So the local ordinary-matter source side has:

```text
c_g = b_conf = b_dis = b_alpha = b_mA = b_clock_i = b_marker = Delta_w_A = delta_kappa_A = 0
```

inside the quotient-matter branch.

## Why This Is An Extension, Not A Missing Ledger

This adds a real parent-action grammar:

```text
Allowed ordinary matter arguments:
  observed quotient geometry,
  quotient-owned constants,
  fixed representation labels,
  ordinary matter fields.

Forbidden hidden arguments:
  representative Xhat,
  shadow frames,
  scalar gauge-kinetic vertices,
  Xhat-dependent mass/Yukawa/binding/clock vertices,
  material Xhat markers,
  active source-only species weights.
```

The rule is deliberately strict. It says MTS recovers the ordinary local matter side of GR only if ordinary matter is a functor of the public quotient geometry and fixed representation data. If any direct `Xhat` dependency is required by the theory, that dependency is not “almost GR”; it is a finite residual coefficient and must be tested.

## Current Claim Status

This is now a coherent proposed parent-action extension. It is not yet a public claim that the entire existing corpus already obeys it.

What has improved:

- the `c_g` problem is no longer an unowned missing coefficient;
- the zero route has an explicit admissible-domain rule;
- the main countermodels are either forbidden by the rule or retained as named residuals;
- source-only weights are no longer ignored.

What remains:

- verify no core MTS principle requires direct `Xhat` matter/constant/source dependence;
- integrate this matter-domain rule with the left-hand field equation;
- prove the geometric side reduces to Einstein/Newton form or retain a geometric residual vector.

## Next Best Step

Move from the right-hand matter/source side to the left-hand field equation:

```text
3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md
```

The test is:

```text
Does the quotient/public geometry action reduce to an Einstein-Hilbert/Newton operator plus controlled residuals when ordinary matter is restricted by the 3103 domain rule?
```

If yes, the local-GR branch becomes serious. If no, the theory remains a residual-modified gravity framework rather than a GR-reduction framework.
