# 5329 - E040 owner-channel numerator pole certificate

## Derivation

For an apparent pole owned by the channel `F_X(E)=0`, the selected
component is written locally as `C_X(E)=N_X(E)/F_X(E)`.  The channel
root is independently refined, `F'_X(E_p)` is derivative-stability
checked, and the analytic numerator is reconstructed on three real
radii from `N_X=F_X C_X`.  The true residue is then

```text
Res[C_X,E_p] = N_X(E_p)/F'_X(E_p).
```

The selector pair, role, orientation, exact mask, high-precision root
and coefficient convergence are required to remain fixed on every fit
sample.  No direct Laurent residue is accepted merely by enlarging its
sampling distance.

## Result

- certified unresolved poles: `30`;
- bounded removable poles: `26`;
- stable material simple poles: `4`;
- maximum removable residue envelope: `9.20935041879e-09`;
- maximum material residue relative spread: `4.17367525234e-07`;
- decision: **E040_OWNER_CHANNEL_26_REMOVABLE_4_MATERIAL_CERTIFIED__RERUN_NODES**;
- validation: **PASS**.

## Interpretation

The 26 `MC04_SP_DM/MC04_P02` direct-Laurent artifacts are bounded
zero-residue cancellations.  The four `P08/MC04_SP_DP` poles are not
removable: their owner-channel residues are material and stable, so the
E040 rerun must subtract them rather than erase them.

## Claim boundary

This checkpoint authorizes replacement of the 30 unresolved E040 pole
classifications only.  The E040 integral, seven-rung regulator ladder,
regulator-zero limit, decay-angle integral, UV coefficient, local GR
and full MTS remain separate gates.
