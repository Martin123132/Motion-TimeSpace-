# 4290 Y5 R2FR transition Hilbert monopole source lock or first residual bound row

## Purpose

This checkpoint tries to avoid circling the same missing-source issue by forcing a fork:

- prove the transition monopole is the same parent Hilbert source;
- or write the first executable residual bound row.

## Outcome

The proof route fails cleanly, not vaguely.

The unsigned clauses are:

- `Pi_M/H_tau` same-branch glue;
- parent zero for the non-EH monopole `mu_extra_tr`.

Therefore:

```text
Z_source_lock=false.
```

## New Executable Row

The first transition residual bound is:

```text
|epsilon_mu_tr| <= 0.167893843691 * Pi_B_tr * (T_res/tau_L) / |c_Gamma|.
```

At the rough transition anchor this gives:

```text
|epsilon_mu_tr| <= 0.08394692185032419
```

for `Pi_B_tr=0.5000000000287336`, `T_res/tau_L=1`, and `|c_Gamma|=1`.

This is private capacity plumbing only; it must not be used as public evidence.
