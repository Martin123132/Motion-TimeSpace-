# 3118 - No Hidden-Visible Coefficient Hom for Local EM or `b_alpha` Product-Bound Runner under AX1090

Private checkpoint. This target tries the derivation route first, then stages a nonclaim runner for the finite `b_alpha` product branch.

## Verdict

The compact-local EM theorem can be stated cleanly:

```text
Hom(C_hid, Coeff(F_Q^2)) = Const or absent
```

is enough to kill hidden local alpha drift from the Maxwell kinetic coefficient. But the current corpus does **not** yet derive this as a parent theorem. The exact blocker is not ordinary covariance or `U(1)` gauge invariance; those allow:

```text
f(I_hid) F_Q^2.
```

The theorem closes only if one of the following is parent-signed:

1. strict local q-basic parent action/readout: visible EM coefficients factor through `q_parent` or fixed representation data;
2. hidden invariant algebra is trivial in compact local tests;
3. visible operator-domain exhaustion forbids hidden-to-visible coefficient maps;
4. exact hidden shift/sequester symmetry forbids non-derivative `f(I_hid)F_Q^2`;
5. radiative/readout closure preserves the same restriction after reduction.

So the route is not dead, but it is still conditional. Because the no-hom theorem is not parent-signed, this checkpoint also adds a `b_alpha` product-bound runner. The runner deliberately refuses claims until MTS-side `tau`, `beta_source`, `K_X`, source/test legs, and valid bound curves are real.

## Source Register

| source_id | path | role |
|---|---|---|
| 1057 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md` | no-independent-`F_Q^2` theorem attempt and counterterms |
| 1058 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md` | visible operator-domain exhaustion and counterterm prior |
| 1099 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md` | no-extra-`F^2` / alpha owner gate |
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | charge generator, norm and same-current owner |
| 3117 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3117-Y5-R2FR-EM-coupling-owner-no-extra-F2-or-alpha-residual-bound-priority-under-AX1090.md` | alpha-value vs hidden-alpha-residual split |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3118_balpha_product_bound_runner.py` | nonclaim `b_alpha` product-bound runner |
| input | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv` | MTS-side product input template |
| output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3118_BALPHA_PRODUCT_BOUND_RUNNER_OUTPUT.csv` | runner output |

## Theorem Attempt

Let the compact-local visible EM action contain:

```text
S_EM = -1/4 integral sqrt(-g_pub) Z_A(Phi) F_Q^2.
```

Split the parent field space locally as:

```text
Phi = (q, y),
q = q_parent(Phi),
y in C_hid.
```

The target theorem is:

```text
Z_A(Phi) = Zbar_A(q_parent(Phi), theta_rep) + lambda_0
```

with `lambda_0` universal and hidden-independent. Then for every compact local vertical generator `v`:

```text
Dq_parent[v] = 0,
Lie_v theta_rep = 0,
Lie_v lambda_0 = 0,
```

so:

```text
Lie_v Z_A = 0,
b_alpha = -Lie_v ln Z_A + readout/current terms = 0
```

provided readout/current terms are also q-basic.

### Proof if strict q-basic action is parent-signed

If the whole compact local action descends:

```text
S_parent^local = Sbar[q_parent(Phi), A_Q, Psi, theta_rep]
                 + boundary/topological/pure-gauge terms,
```

then a term:

```text
f(y) F_Q^2
```

is not allowed unless `f(y)` is constant on every vertical fibre. Otherwise:

```text
delta_y S_parent contains (partial_y f) F_Q^2,
```

which is a real vertical Euler component, contradicting first-class vertical gauge descent.

Therefore the no-hom theorem is a direct corollary of strict q-basic local action plus readout/radiative closure.

### Why the theorem does not close today

Current files give exact conditional pieces, but not the parent source signature:

```text
visible operator-domain exhaustion = not derived;
no hidden-visible coefficient morphism = not derived;
radiative/readout closure = unsigned;
same-current owner = unsigned.
```

Thus:

```text
Hom(C_hid, Coeff(F_Q^2)) = Const/absent
```

remains a theorem target, not a claim.

## Countermodel

If a hidden invariant survives:

```text
I_hid = I_hid(y),
```

and the visible EM operator domain allows scalar coefficients, then:

```text
S_counter = -1/4 integral sqrt(-g_pub) [Z_0 + epsilon I_hid(y)] F_Q^2.
```

This respects diffeomorphism covariance and visible `U(1)` gauge invariance. It gives:

```text
b_alpha = - Lie_v ln[Z_0 + epsilon I_hid(y)]
        ~= - epsilon Lie_v I_hid / Z_0
```

for small `epsilon`. Therefore no-hom cannot be proved from covariance or `U(1)` alone.

## Radiative and Readout Closure

Even if the bare action is q-basic:

```text
Z_A^bare = Zbar_A(q),
```

the effective/readout coefficient can reopen the channel:

```text
Z_A^eff = Zbar_A(q) + delta lambda_rad(q,y,mu) + delta Z_readout(q,y).
```

So the theorem needs:

```text
Lie_v delta lambda_rad = 0,
Lie_v delta Z_readout = 0.
```

This must be a separate gate. A tree-level no-extra-`F^2` proof is not enough for claim-grade clock/spectral silence.

## Product-Bound Runner Contract

The runner is intentionally conservative:

```text
scripts\Y5_R2FR_3118_balpha_product_bound_runner.py
```

reads:

```text
P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv
P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv
P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv
P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv
```

and writes:

```text
P8_Y5_R2FR_3118_BALPHA_PRODUCT_BOUND_RUNNER_OUTPUT.csv
P8_Y5_R2FR_3118_VALIDATION.csv
```

The runner refuses claim status if any of these are present:

```text
MISSING_ markers,
PLACEHOLDER markers,
non-numeric product values,
valid_for_claim != true,
missing source path,
bound row not source-backed,
R10 valid bound curve absent,
tau/beta/K_X/source-test projection absent.
```

## Runner Result

Current result is expected and healthy:

```text
clock row: source-backed product bound exists, MTS product value missing -> nonclaim
WEP row: target/projection scaffold exists, MTS beta_source/tau missing -> nonclaim
R10 row: product law exists, K_X/beta_s/beta_t/valid bound curve missing -> nonclaim
standalone b_alpha: no standalone bound/value -> nonclaim
```

This is not a failure. It gives a safe harness for future finite `b_alpha` tests after the theorem route has been honestly attempted.

## Decision

| branch | status | next implication |
|---|---|---|
| no-hidden-visible coefficient hom | exact conditional theorem, not parent-signed | keep derivation route open |
| constant `lambda_0 F_Q^2` | calibration debt only if hidden-independent | does not poison local tests |
| hidden `f(I_hid)F_Q^2` | live countermodel | must be forbidden or bounded |
| radiative/readout closure | unsigned | explicit gate before any alpha silence claim |
| `b_alpha` finite runner | implemented nonclaim | ready for real MTS-side inputs later |

## Claim Status

No public alpha, WEP, R10, clock, Maxwell, local-GR, derived-`G`, derived-`alpha`, or unified-field claim follows from 3118.

The internal advance is:

```text
no-hidden-visible coefficient theorem reduced to a strict q-basic/radiative-closure target;
finite b_alpha branch now has a concrete nonclaim runner;
future alpha tests cannot accidentally claim from missing tau/beta/K_X inputs.
```

## Next Target

Write:

```text
3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md
```

Direct target:

1. try to prove that the visible EM current `J_Q` and charge labels are fixed representation/q-basic data;
2. if not, stage `delta_J` as the second-priority finite residual after `b_alpha`;
3. connect `delta_J` to WEP/R10/source-calibration legs without claiming any pass.
