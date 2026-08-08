# 5331 - E040 adaptive-divisor controller integration smoke

## Derived result

The matrix-resolvent proposal is not the object implemented by E040 and is
rejected.  The applicable local theorem is analytic division:

```text
N(E,x) = F(E,x) Q(E,x) + r(x),
r(x) = N(E_p(x),x),
Res[C(E,x) dE,E_p(x)] = r(x)/partial_E F(E_p(x),x).
```

The zero/nonzero residue class is invariant under every nonsingular analytic
energy reparametrization.  A finite coordinate sample does not prove a family
identity, so each unseen adaptive coordinate must run the divisor test.

Checkpoint 5330 applies that test to all 30 previously unresolved E040 poles:

```text
removable bounded-zero = 21;
stable material        = 9;
maximum removable envelope = 5.56243897158e-9;
maximum material spread    = 4.14071207473e-5.
```

All validation gates pass without changing the `1e-8` removable ceiling.

## Controller integration

The 5327 controller now consumes the validated 5330 rows and, crucially, runs
the same classifier for any unresolved pole whose adaptive coordinate is not
in the 5330 cache.  Runtime roots, samples, fits and certificates are persisted
under `source-intake/functional_rg/5327/E040/adaptive-divisor-runtime`.

The original 26 failed descendants reran successfully: `26/26` accepted with
zero unresolved poles.  The subsequent one-hour outer resume reached 59 nodes
before its safe pause.  It exposed 26 earlier coordinates that also required
the runtime path.  Their first runtime attempt failed only because the
controller's six-argument component evaluator had been passed directly to the
four-argument divisor interface; no residue samples were evaluated.

That adapter defect is fixed by a dedicated full component evaluator retaining
the selector, mask, law, orientation, high-precision root and coefficient
audit.  A forced unseen-coordinate smoke at `P01_P01S01_Q04_N01`,
`MC04_SP_DM/MC04_P02`, now gives

```text
classification             = removable bounded-zero;
certified residue envelope = 5.55058585178e-9;
maximum fit residual       = 1.83789152038e-5;
all divisor controls       = true.
```

This is a real runtime evaluation, not a node exception.

## Integrity repair

The protected formal workbench initially differed from its inventory only by
82 generated `.pyc` files.  All 8,760 baseline files were present and
byte-identical.  Removing only those generated caches restored the exact
protected digest

```text
0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f.
```

No formal source file and no GitHub repository was changed.

## Exact resume point

The final evaluator-adapter edit changes the 5327 source hash.  Before another
claim-bearing run:

1. rerun checkpoint 5330 so its source-current hash binds the final 5327 code;
2. rerun the current failed E040 shards with the corrected runtime evaluator;
3. resume the outer controller from its safe checkpoint;
4. aggregate and validate the finite `epsilon=0.04` rung;
5. only then execute checkpoint 5328's regulator-zero gate.

No finite-rung, regulator-zero, decay-angle, UV, local-GR or full-MTS claim is
made by checkpoint 5331.
